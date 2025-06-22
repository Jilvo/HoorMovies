import os

import requests
from django.conf import settings


class TMDbClient:

    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self, api_key=None):
        self.api_key = os.getenv("TMDB_API_KEY")

    def _get(self, path, **params):
        params["api_key"] = self.api_key
        resp = requests.get(f"{self.BASE_URL}/{path}", params=params)
        resp.raise_for_status()
        return resp.json()

    def fetch_popular_movies(self, page=1):
        data = self._get("movie/popular", page=page)
        return data.get("results", [])

    def fetch_all_popular(self, max_pages=5):
        for page in range(1, max_pages + 1):
            yield from self.fetch_popular_movies(page=page)

    def fetch_movie_genres(self):
        data = self._get("genre/movie/list")
        return data.get("genres", [])
