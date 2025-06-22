from rest_framework import viewsets
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from .models import Spectator
from .serializers import SpectatorSerializer


class SpectatorViewSet(viewsets.ModelViewSet):
    """
    Registration and profile management for spectators.
    """

    queryset = Spectator.objects.all()
    serializer_class = SpectatorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "post", "patch", "delete"]
