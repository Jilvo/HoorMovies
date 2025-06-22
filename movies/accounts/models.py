from django.contrib.auth.models import AbstractUser
from django.db import models


class Spectator(AbstractUser):
    class Meta:
        verbose_name = "Spectator"
        verbose_name_plural = "Spectators"

    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="spectator_avatars/", null=True, blank=True)
    favorites = models.ManyToManyField(
        "manage_movies.Film",
        related_name="favorited_by",
        blank=True,
        verbose_name="Films favoris",
    )

    def __str__(self):
        return self.get_full_name() or self.username
