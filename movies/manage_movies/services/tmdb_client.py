import os
from typing import Any, Dict, Generator, List, Optional

import requests


class TMDbClient:
    """
    Client for interacting with The Movie Database (TMDb) API.
    Provides methods to fetch movies, directors, and genres.
    """

    def __init__(self, api_key: Optional[str] = None) -> None:
        """Initialize the TMDbClient."""
        self.BASE_URL = "https://api.themoviedb.org/3"
        self.api_key = api_key or os.getenv("TMDB_API_KEY")

    def _get(self, path: str, **params: Any) -> Dict[str, Any]:
        """Internal method to perform a GET request to the TMDb API."""
        params["api_key"] = self.api_key
        resp = requests.get(f"{self.BASE_URL}/{path}", params=params)
        resp.raise_for_status()
        return resp.json()

    def fetch_popular_movies(self, page: int = 1) -> List[Dict[str, Any]]:
        """Fetch a list of popular movies."""
        return self._get("movie/popular", page=page).get("results", [])

    def fetch_upcoming_movies(self, page: int = 1) -> List[Dict[str, Any]]:
        """Fetch a list of upcoming movies."""
        return self._get("movie/upcoming", page=page).get("results", [])

    def fetch_popular_and_upcoming_movies(self, page: int = 1) -> List[Dict[str, Any]]:
        """Fetch and merge popular and upcoming movies for a given page.
        Removes duplicates based on movie ID."""
        popular = self.fetch_popular_movies(page=page)
        upcoming = self.fetch_upcoming_movies(page=page)
        movies = {movie["id"]: movie for movie in popular}
        for movie in upcoming:
            movies[movie["id"]] = movie
        return list(movies.values())

    def fetch_movie_details(self, movie_id: int) -> Dict[str, Any]:
        """Fetch detailed information about a movie."""
        return self._get(f"movie/{movie_id}")

    def fetch_movie_directors(self, movie_id: int) -> Optional[Dict[str, Any]]:
        """Fetch the directors of a movie."""
        credits = self._get(f"movie/{movie_id}/credits")
        directors = [c for c in credits.get("crew", []) if c["job"] == "Director"]
        return directors if directors else None

    def fetch_director_details(self, director_id: int) -> Dict[str, Any]:
        """Fetch detailed information about a director."""
        return self._get(f"person/{director_id}")

    def fetch_all_popular(
        self, max_pages: int = 5
    ) -> Generator[Dict[str, Any], None, None]:
        """Yield all popular movies up to a maximum number of pages."""
        for page in range(1, max_pages + 1):
            yield from self.fetch_popular_movies(page=page)

    def fetch_movie_genres(self) -> List[Dict[str, Any]]:
        """Fetch the list of movie genres."""
        return self._get("genre/movie/list").get("genres", [])
