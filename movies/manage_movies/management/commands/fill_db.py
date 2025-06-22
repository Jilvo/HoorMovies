from django.core.management.base import BaseCommand
from manage_movies.models import Author, Film, Genre

from movies.manage_movies.services.tmdb import TMDbClient


class Command(BaseCommand):
    help = "Fill the database with sample data"

    def handle(self, *args, **kwargs):
        tmdb_client = TMDbClient()
        # Clear existing data
        Film.objects.all().delete()
        Author.objects.all().delete()
        Genre.objects.all().delete()

        # Create Genres
        for genre_data in tmdb_client.fetch_movie_genres():
            genre, created = Genre.objects.get_or_create(
                name=genre_data["name"], tmdb_id=genre_data["id"]
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created genre: {genre.name}"))
        # Create Movies
        # Create Actors

        self.stdout.write(self.style.SUCCESS("Database filled with sample data"))
