from django.contrib.auth.models import AbstractUser
from django.db import models


class Author(models.Model):
    birth_date = models.DateField(null=True, blank=True)


class Spectator(AbstractUser):
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="spectator_avatars/", null=True, blank=True)

    def __str__(self):
        return self.get_full_name() or self.username


class Film(models.Model):
    class RatingChoices(models.TextChoices):
        BAD = "bad", "Bad"
        AVERAGE = "average", "Average"
        GOOD = "good", "Good"
        EXCELLENT = "excellent", "Excellent"

    class StatusChoices(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"

    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="films")
    rating = models.CharField(
        max_length=10, choices=RatingChoices.choices, default=RatingChoices.GOOD
    )
    status = models.CharField(
        max_length=10, choices=StatusChoices.choices, default=StatusChoices.DRAFT
    )
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    box_office = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name
