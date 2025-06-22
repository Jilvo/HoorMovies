from accounts.models import Spectator
from django.contrib import admin


class FavoriteInline(admin.TabularInline):
    """Inline in the Spectator admin for related favorites."""

    model = Spectator.favorites.through
    extra = 0
    verbose_name = "Favori"
    verbose_name_plural = "Favoris"


@admin.register(Spectator)
class SpectatorAdmin(admin.ModelAdmin):
    """Admin interface for Spectator model."""

    list_display = ("username", "first_name", "last_name", "email", "bio")
    search_fields = ("username", "first_name", "last_name", "email")
    list_filter = ("is_staff", "is_active")
    inlines = [FavoriteInline]
