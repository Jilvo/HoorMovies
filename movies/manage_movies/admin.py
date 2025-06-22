from django.contrib import admin

from .models import Author, Film, Spectator

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

    list_display = ("title", "release_date", "rating")
    search_fields = ("title", "description")
    list_filter = ("release_date", "rating")


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin interface for Author model.
    """

    list_display = ("birth_date",)
    search_fields = ("birth_date",)
    list_filter = ()
