from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Author(models.Model):
    class GenderChoices(models.TextChoices):
        NOT_SPECIFIED = "0", "Not specified"
        FEMALE = "1", "Female"
        MALE = "2", "Male"
        NON_BINARY = "3", "Non-binary"

    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    biography = models.TextField(blank=True)
    name = models.CharField(max_length=255, blank=False, default="")
    place_of_birth = models.CharField(max_length=255, null=True, default="Unknown")
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
        default=GenderChoices.NOT_SPECIFIED,
    )
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name


class Spectator(AbstractUser):
    class Meta:
        verbose_name = "Spectator"
        verbose_name_plural = "Spectators"

    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="spectator_avatars/", null=True, blank=True)
    favorites = models.ManyToManyField(
        "Film", related_name="favorited_by", blank=True, verbose_name="Films favoris"
    )

    def __str__(self):
        return self.get_full_name() or self.username


class Film(models.Model):
    class RatingChoices(models.TextChoices):
        BAD = "Bad", "Bad"
        AVERAGE = "Average", "Average"
        GOOD = "Good", "Good"
        EXCELLENT = "Excellent", "Excellent"

    class StatusChoices(models.TextChoices):
        PLANNED = "Planned", "Planned"
        POST_PROD = "Post Production", "Post Production"
        RELEASED = "Released", "Released"

    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    adult = models.BooleanField(default=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="films")
    rating = models.CharField(
        max_length=10, choices=RatingChoices.choices, default=RatingChoices.GOOD
    )
    status = models.CharField(
        max_length=15, choices=StatusChoices.choices, default=StatusChoices.PLANNED
    )
    budget = models.IntegerField(null=True, blank=True)
    box_office = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name


class Rating(models.Model):
    """Model representing a rating given by a spectator to a film."""

    spectator = models.ForeignKey(
        Spectator,
        on_delete=models.CASCADE,
        related_name="ratings",
        verbose_name="Spectator",
    )
    film = models.ForeignKey(
        Film, on_delete=models.CASCADE, related_name="ratings", verbose_name="Film"
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Note (1–5)",
    )
    comment = models.TextField(blank=True, verbose_name="Comment")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update date")

    class Meta:
        unique_together = ("spectator", "film")
        ordering = ["-created_at"]
        verbose_name = "Notation"
        verbose_name_plural = "Notations"

    def __str__(self):
        return f"{self.spectator.username} – {self.score}/5 on « {self.film.title} »"
