from rest_framework.routers import DefaultRouter

from .views import (AuthorViewSet, FavoriteViewSet, FilmViewSet, RatingViewSet,
                    SpectatorViewSet)

router = DefaultRouter()
router.register(r"authors", AuthorViewSet, basename="author")
router.register(r"films", FilmViewSet, basename="film")
router.register(r"spectators", SpectatorViewSet, basename="spectator")
router.register(r"favorites", FavoriteViewSet, basename="favorite")
router.register(r"ratings", RatingViewSet, basename="rating")

urlpatterns = router.urls
