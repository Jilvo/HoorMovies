from django.db.models import Count
from django.utils.dateparse import parse_date
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .models import Author, Film, Rating, Spectator
from .serializers import AuthorSerializer, FilmSerializer, SpectatorSerializer


class SpectatorViewSet(viewsets.ModelViewSet):
    """
    Registration and profile management for spectators.
    """

    queryset = Spectator.objects.all()
    serializer_class = SpectatorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "post", "patch", "delete"]


class FilmViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing films.
    """

    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]

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

        return qs


class AuthorViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing authors.
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        qs = Author.objects.annotate(film_count=Count("films"))
        has = self.request.query_params.get("has_films")
        if has is not None:
            val = has.lower()
            if val in ("true", "1"):
                qs = qs.filter(film_count__gt=0)
            elif val in ("false", "0"):
                qs = qs.filter(film_count__exact=0)
        return qs


class FavoriteViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def list(self, request):
        favorites = request.user.favorites.all()
        serializer = FilmSerializer(favorites, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def add(self, request, pk=None):
        try:
            film = Film.objects.get(pk=pk)
            request.user.favorites.add(film)
            return Response({"detail": "Film ajouté aux favoris."}, status=200)
        except Film.DoesNotExist:
            return Response({"detail": "Film introuvable."}, status=404)

    @action(detail=True, methods=["post"])
    def remove(self, request, pk=None):
        try:
            film = Film.objects.get(pk=pk)
            request.user.favorites.remove(film)
            return Response({"detail": "Film retiré des favoris."}, status=200)
        except Film.DoesNotExist:
            return Response({"detail": "Film introuvable."}, status=404)
