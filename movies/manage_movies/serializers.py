from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from .models import Author, Film, Rating, Spectator


class SpectatorSerializer(serializers.ModelSerializer):
    """
    Serializer for Spectator model.
    """

    class Meta:
        model = Spectator
        fields = ["id", "username", "first_name", "last_name", "email", "bio", "avatar"]


class FilmSerializer(serializers.ModelSerializer):
    """
    Serializer for Film model.
    """

    author_name = serializers.CharField(source="author.name", read_only=True)

    class Meta:
        model = Film
        fields = [
            "id",
            "title",
            "release_date",
            "status",
            "description",
            "author_name",
        ]


class FilmDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Film model (all fields).
    """

    author = serializers.StringRelatedField()

    class Meta:
        model = Film
        fields = "__all__"


class AuthorDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Author model (all fields).
    """

    films = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="title",
    )

    class Meta:
        model = Author
        fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for Author model.
    """

    movies_list = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="title", source="films"
    )

    class Meta:
        model = Author
        fields = ["id", "name", "birth_date", "biography", "movies_list"]


class RatingSerializer(serializers.ModelSerializer):
    """Serializer for Rating model.
    This serializer allows posting ratings for films and authors."""

    content_type = serializers.SlugRelatedField(
        slug_field="model",
        queryset=ContentType.objects.filter(model__in=["film", "author"]),
    )

    class Meta:
        model = Rating
        fields = [
            "id",
            "content_type",
            "object_id",
            "score",
            "comment",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
