from django.core.management.base import BaseCommand
from manage_movies.models import Author, Film, Genre
from manage_movies.services.tmdb_client import TMDbClient
from manage_movies.utils.utils import format_date


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
        for movie_data in tmdb_client.fetch_popular_and_upcoming_movies():
            directors = tmdb_client.fetch_movie_directors(movie_data["id"])
            if not directors:
                self.stdout.write(
                    self.style.WARNING(
                        f"No director found for movie: {movie_data['title']}"
                    )
                )
                continue
            authors = []
            for director_data in directors:
                author_details = tmdb_client.fetch_director_details(director_data["id"])
                author, created = Author.objects.get_or_create(
                    name=author_details["name"],
                    birth_date=format_date(author_details.get("birthday")),
                    death_date=format_date(author_details.get("deathday")),
                    biography=author_details.get("biography", ""),
                    place_of_birth=author_details.get("place_of_birth", None),
                    gender=author_details.get(
                        "gender", Author.GenderChoices.NOT_SPECIFIED
                    ),
                    tmdb_id=director_data["id"],
                )
                authors.append(author)
            movie_detais = tmdb_client.fetch_movie_details(movie_data["id"])
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created author: {author.name}"))
            if movie_data.get("vote_average", 0) < 5:
                rating = Film.RatingChoices.BAD
            elif movie_data.get("vote_average", 0) < 7:
                rating = Film.RatingChoices.AVERAGE
            elif movie_data.get("vote_average", 0) < 8:
                rating = Film.RatingChoices.GOOD
            else:
                rating = Film.RatingChoices.EXCELLENT
            film, created = Film.objects.get_or_create(
                title=movie_data["title"],
                description=movie_data.get("overview", ""),
                release_date=movie_data.get("release_date"),
                adult=movie_data.get("adult", False),
                rating=rating,
                status=movie_detais.get("status", Film.StatusChoices.PLANNED),
                budget=movie_detais.get("budget", None),
                box_office=movie_detais.get("revenue", None),
                tmdb_id=movie_data.get("id", None),
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created film: {film.title}"))
            else:
                self.stdout.write(
                    self.style.WARNING(f"Film already exists: {film.title}")
                )
            film.authors.set(authors)
            genre_objs = [
                Genre.objects.get(tmdb_id=genre_id)
                for genre_id in movie_data.get("genre_ids", [])
            ]
            film.genres.set(genre_objs)

        self.stdout.write(self.style.SUCCESS("Database filled with sample data"))
