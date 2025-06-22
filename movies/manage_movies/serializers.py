from rest_framework import serializers

from .models import Spectator


class SpectatorSerializer(serializers.ModelSerializer):
    """
    Serializer for Spectator model.
    """

    class Meta:
        model = Spectator
        fields = ["id", "username", "first_name", "last_name", "email", "bio", "avatar"]
