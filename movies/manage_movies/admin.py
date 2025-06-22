from datetime import date

from django.contrib import admin
from django.utils.html import format_html

from .models import Author, Film, Genre, Spectator

# Register your models here.


@admin.register(Spectator)
class SpectatorAdmin(admin.ModelAdmin):
    """
    Admin interface for Spectator model.
    """

    list_display = ("username", "first_name", "last_name", "email", "bio")
    search_fields = ("username", "first_name", "last_name", "email")
    list_filter = ("is_staff", "is_active")


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    """
    Admin interface for Film model.
    """

    list_display = (
        "title",
        "release_date",
        "rating",
        "show_revenue_in_millions",
        "author",
        "status",
    )
    search_fields = ("title", "description")
    list_filter = ("release_date", "rating")

    def show_revenue_in_millions(self, obj):
        """Format the box office revenue in millions."""
        if obj.box_office:
            return f"${obj.box_office / 1_000_000:.2f}M"
        return "N/A"


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin interface for Author model.
    """

    list_display = ("name", "age", "gender", "is_alive_display")
    search_fields = ("name",)
    list_filter = ()

    def age(self, obj):
        """Calculate the age of the author based on their birth date."""
        if obj.birth_date:
            today = date.today()
            return (
                today.year
                - obj.birth_date.year
                - (
                    (today.month, today.day)
                    < (obj.birth_date.month, obj.birth_date.day)
                )
            )
        return "-"

    age.short_description = "Age"

    def is_alive_display(self, obj):
        if obj.death_date is None:
            return format_html("<span>✅</span>")
        else:
            return format_html("<span>❌</span>")

    is_alive_display.short_description = "Alive Status"
    is_alive_display.admin_order_field = "death_date"


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """
    Admin interface for Genre model.
    """

    list_display = ("name", "tmdb_id")
    search_fields = ("name",)
    list_filter = ("tmdb_id",)
