from rest_framework import serializers

from .models import Author, Film, Spectator


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
