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

    class Meta:
        model = Film
        fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for Author model.
    """

    class Meta:
        model = Author
        fields = "__all__"


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
