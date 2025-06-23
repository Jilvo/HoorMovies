import json
from pathlib import Path

import pytest
import requests
from manage_movies.services.tmdb_client import TMDbClient


class DummyResponse:
    def __init__(self, json_data, status=200):
        self._json = json_data
        self.status_code = status

    def raise_for_status(self):
        """Raise an HTTPError if status is not 200."""
        if self.status_code != 200:
            raise requests.HTTPError(f"Status {self.status_code}")

    def json(self):
        """Return the mocked JSON payload."""
        return self._json


TEST_DIR = Path(__file__).parent
MOCKS = TEST_DIR / "mocks"


@pytest.fixture
def client():
    """Provide a TMDbClient instance with a dummy API key."""
    return TMDbClient(api_key="dummy_key")


def _load_mock(name: str):
    """Load a JSON mock from the mocks directory."""
    with open(MOCKS / name) as f:
        return json.load(f)


def test_fetch_upcoming_movies(monkeypatch, client):
    """Test that upcoming movies are fetched correctly with pagination."""
    upcoming_mock = _load_mock("upcoming_movies.json")

    def fake_get(url, params):
        assert "movie/upcoming" in url
        assert params["page"] == 2
        assert params["api_key"] == "dummy_key"
        return DummyResponse(upcoming_mock)

    monkeypatch.setattr(requests, "get", fake_get)

    movies = client.fetch_upcoming_movies(page=2)
    assert movies == upcoming_mock["results"]


def test_fetch_popular_and_upcoming_movies(monkeypatch, client):
    """Test merging and deduplicating popular and upcoming movies."""
    pop = [{"id": 1}, {"id": 2}]
    upc = [{"id": 2}, {"id": 3}]
    monkeypatch.setattr(client, "fetch_popular_movies", lambda page: pop)
    monkeypatch.setattr(client, "fetch_upcoming_movies", lambda page: upc)

    merged = client.fetch_popular_and_upcoming_movies(page=1)
    ids = sorted(m["id"] for m in merged)
    assert ids == [1, 2, 3]


def test_fetch_movie_details(monkeypatch, client):
    """Test fetching detailed movie information by ID."""
    details_mock = _load_mock("movie_details.json")

    def fake_get(url, params):
        assert f"movie/{123}" in url
        return DummyResponse(details_mock)

    monkeypatch.setattr(requests, "get", fake_get)

    details = client.fetch_movie_details(movie_id=123)
    assert details == details_mock


def test_fetch_movie_director(monkeypatch, client):
    """Test fetching the director from movie credits."""
    credits_mock = _load_mock("movie_credits.json")

    def fake_get(url, params):
        assert f"movie/{456}/credits" in url
        return DummyResponse(credits_mock)

    monkeypatch.setattr(requests, "get", fake_get)

    director = client.fetch_movie_director(movie_id=456)
    assert director is not None
    assert director["job"] == "Director"

    monkeypatch.setattr(
        requests, "get", lambda url, params: DummyResponse({"crew": []})
    )
    assert client.fetch_movie_director(movie_id=456) is None


def test_fetch_director_details(monkeypatch, client):
    """Test fetching detailed director information by person ID."""
    director_mock = _load_mock("director_details.json")

    def fake_get(url, params):
        assert f"person/{99}" in url
        return DummyResponse(director_mock)

    monkeypatch.setattr(requests, "get", fake_get)

    info = client.fetch_director_details(director_id=99)
    assert info["id"] == 99
    assert "name" in info


def test_fetch_all_popular(client, monkeypatch):
    """Test iterating over multiple pages of popular movies."""
    pages = {1: [{"id": 1}], 2: [{"id": 2}]}
    monkeypatch.setattr(client, "fetch_popular_movies", lambda page: pages[page])

    all_ids = [m["id"] for m in client.fetch_all_popular(max_pages=2)]
    assert all_ids == [1, 2]


def test_fetch_movie_genres(monkeypatch, client):
    """Test fetching the list of movie genres."""
    genres_mock = _load_mock("genres.json")

    def fake_get(url, params):
        assert "genre/movie/list" in url
        return DummyResponse(genres_mock)

    monkeypatch.setattr(requests, "get", fake_get)

    genres = client.fetch_movie_genres()
    assert genres == genres_mock["genres"]
