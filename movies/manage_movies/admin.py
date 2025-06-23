from datetime import date

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html

from .models import Author, Film, Genre, Rating

# ——— Inlines —————————————————————————————————————————————————————————————————


class FilmInline(admin.TabularInline):
    """
    Inline for displaying films related to an author in the Author admin.
    """

    model = Film.authors.through
    extra = 0
    verbose_name = "Film"
    verbose_name_plural = "Films"
    show_change_link = True


class RatingInline(GenericTabularInline):
    """
    Inline for displaying ratings related to a film in the Film admin.
    """

    model = Rating
    fields = ("spectator", "score", "comment")
    readonly_fields = ("created_at",)
    extra = 0
    show_change_link = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        film_type = ContentType.objects.get_for_model(Film)
        return qs.filter(content_type=film_type)


class AuthorInline(admin.TabularInline):
    model = Film.authors.through
    extra = 0
    verbose_name = "Author"
    verbose_name_plural = "Authors"
    show_change_link = True


# ——— Filters ————————————————————————————————————————————————————————————————


class HasFilmsFilter(admin.SimpleListFilter):
    """
    Admin interface for Film model.
    """

    title = "With films"
    parameter_name = "has_films"

    def lookups(self, request, model_admin):
        return (
            ("yes", "With at least one film"),
            ("no", "No film"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(films__isnull=False).distinct()
        if self.value() == "no":
            return queryset.filter(films__isnull=True)
        return queryset


# ——— Admin Classes —————————————————————————————————————————————————————


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin interface for Author model.
    """

    list_display = ("name", "age", "gender", "is_alive_display")
    search_fields = ("name",)
    list_filter = (HasFilmsFilter,)
    inlines = [FilmInline]

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
        """Display a checkmark if alive, cross if deceased."""
        if obj.death_date is None:
            return format_html("<span>✅</span>")
        return format_html("<span>❌</span>")

    is_alive_display.short_description = "Alive Status"
    is_alive_display.admin_order_field = "death_date"


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    """Admin interface for Film model."""

    list_display = (
        "title",
        "release_date",
        "rating",
        "status",
        "show_revenue_in_millions",
    )
    search_fields = ("title", "description")
    list_filter = ("created_at", "rating", "status")
    date_hierarchy = "created_at"
    inlines = [AuthorInline, RatingInline]
    exclude = ("authors",)

    def show_revenue_in_millions(self, obj):
        """Format the box office revenue in millions of dollars."""
        if obj.box_office:
            return f"${obj.box_office / 1_000_000:.2f}M"
        return "N/A"

    show_revenue_in_millions.short_description = "Box Office (M$)"


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """
    Admin interface for Genre model.
    """

    list_display = ("name", "tmdb_id")
    search_fields = ("name",)
    list_filter = ("tmdb_id",)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = (
        "spectator",
        "score",
        "comment",
        "target",
        "created_at",
    )
    search_fields = ("spectator__username", "comment")
    list_filter = ("score", "content_type")

    def target(self, obj):
        """
        Display the title of the film or name of the author being rated.
        """
        if isinstance(obj.content_object, Film):
            return obj.content_object.title
        elif isinstance(obj.content_object, Author):
            return obj.content_object.name
        return str(obj.content_object)

    target.short_description = "Noté"
    target.admin_order_field = "content_type"
