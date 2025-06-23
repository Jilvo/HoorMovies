from django.db.models import Count
from django.utils.dateparse import parse_date
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .models import Author, Film, Rating, Spectator
from .serializers import (AuthorDetailSerializer, AuthorSerializer,
                          FilmDetailSerializer, FilmSerializer,
                          RatingSerializer, SpectatorSerializer)


class SpectatorViewSet(viewsets.ModelViewSet):
    """
    Registration and profile management for spectators.
    """

    queryset = Spectator.objects.all()
    serializer_class = SpectatorSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]


class FilmViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing films.
    """

    queryset = Film.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FilmDetailSerializer
        return FilmSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        date_filters = [
            ("created_at_after", "created_at__date__gte"),
            ("created_at_before", "created_at__date__lte"),
            ("release_date_after", "release_date__gte"),
            ("release_date_before", "release_date__lte"),
        ]
        for param, lookup in date_filters:
            value = params.get(param)
            if value:
                parsed = parse_date(value)
                if parsed:
                    qs = qs.filter(**{lookup: parsed})
        rating = params.get("rating")
        if rating in {choice.value for choice in Film.RatingChoices}:
            qs = qs.filter(rating=rating)

        status = params.get("status")
        if status in {choice.value for choice in Film.StatusChoices}:
            qs = qs.filter(status=status)
        source = self.request.query_params.get("source")
        if source == "admin":
            qs = qs.filter(tmdb_id__isnull=True)
        elif source == "tmdb":
            qs = qs.filter(tmdb_id__isnull=False)
        return qs

    @action(detail=True, methods=["post"], url_path="archive")
    def archive(self, request, pk=None):
        """
        Archive a film by setting its archived field to True.
        """
        try:
            film = self.get_object()
            film.archived = True
            film.save()
            return Response({"detail": "Film archived successfully."}, status=200)
        except Film.DoesNotExist:
            return Response({"detail": "Film not found."}, status=404)


class AuthorViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing authors.
    """

    queryset = Author.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AuthorDetailSerializer
        return AuthorSerializer

    def get_permissions(self):
        """Determine permissions based on the action being performed."""
        if self.action == "destroy":
            return [IsAuthenticated()]
        return [IsAuthenticatedOrReadOnly()]

    def get_queryset(self):
        """Retrieve authors with optional filtering by film count and source."""
        qs = Author.objects.annotate(film_count=Count("films"))
        has = self.request.query_params.get("has_films")
        if has is not None:
            val = has.lower()
            if val in ("true", "1"):
                qs = qs.filter(film_count__gt=0)
            elif val in ("false", "0"):
                qs = qs.filter(film_count__exact=0)
        source = self.request.query_params.get("source")
        if source == "admin":
            qs = qs.filter(tmdb_id__isnull=True)
        elif source == "tmdb":
            qs = qs.filter(tmdb_id__isnull=False)
        return qs

    def destroy(self, request, *args, **kwargs):
        """Override destroy to prevent deletion if the author has associated films."""
        author = self.get_object()
        if author.films.exists():
            return Response(
                {"detail": "Cannot delete author with associated films."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)


class FavoriteViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        favorites = request.user.favorites.all()
        serializer = FilmSerializer(favorites, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def add(self, request, pk=None):
        """Add a film to the user's favorites."""
        try:
            film = Film.objects.get(pk=pk)
            request.user.favorites.add(film)
            return Response({"detail": "Movie added to favorites"}, status=200)
        except Film.DoesNotExist:
            return Response({"detail": "Can't find Movie"}, status=404)

    @action(detail=True, methods=["post"])
    def remove(self, request, pk=None):
        try:
            film = Film.objects.get(pk=pk)
            request.user.favorites.remove(film)
            return Response({"detail": "Movie deleted from favorites"}, status=200)
        except Film.DoesNotExist:
            return Response({"detail": "Can't find Movie"}, status=404)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = request.user
        ct = data["content_type"]
        oid = data["object_id"]
        score = data["score"]
        comment = data.get("comment", "")

        rating, created = Rating.objects.update_or_create(
            spectator=user,
            content_type=ct,
            object_id=oid,
            defaults={"score": score, "comment": comment},
        )

        out_serializer = self.get_serializer(rating)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(out_serializer.data, status=status_code)
