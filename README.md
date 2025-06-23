# HoorMovies

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python)](https://www.python.org/)
![Django](https://img.shields.io/badge/django-5.2.3-darkgreen?logo=django)
[![Postgres](https://img.shields.io/badge/Postgres-%23316192.svg?logo=postgresql&logoColor=white)](#)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff)](#)
[![CI](https://github.com/Jilvo/HoorMovies/actions/workflows/github-actions.yml/badge.svg)](https://github.com/Jilvo/HoorMovies/actions/workflows/github-actions.yml)

A Django + Django REST Framework application for managing movies, authors and spectators, containerized with Docker Compose.

---

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Environment Variables](#environment-variables)
- [Installation & Startup](#installation--startup)
  - [Clone the Repository](#clone-the-repository)
  - [Configure .env](#configure-env)
  - [Build & Run with Docker Compose](#build--run-with-docker-compose)
  - [Optional: Run Locally without Docker](#optional-run-locally-without-docker)
- [Running Tests](#running-tests)
- [Creating a Superuser](#creating-a-superuser)
- [API Endpoints](#api-endpoints)
  - [Authentication & JWT](#authentication--jwt)
  - [Authors](#authors)
  - [Films](#films)
  - [Spectators](#spectators)
  - [Favorites](#favorites)
  - [Ratings](#ratings)
- [Notes](#notes)

---

## Overview

HoorMovies provides:

- A **Django Admin** interface with full CRUD and advanced filters  
- A **REST API** for authors, films, spectators, ratings and favorites  
- **JWT authentication** for protected operations  
- Dockerized services for easy deployment  

---

## Prerequisites

- [Docker](https://www.docker.com/get-started) & [Docker Compose](https://docs.docker.com/compose/install/)  

---

## Environment Variables

Create a file named `.env` in the project root with at least:

```dotenv
DJANGO_SECRET_KEY=your-secret-key
POSTGRES_DB=""
POSTGRES_USER=""
POSTGRES_PASSWORD=""
POSTGRES_HOST=""
POSTGRES_PORT=""
```

## Installation & Startup

### Clone the Repository
   ```bash
   git clone https://github.com/Jilvo/HoorMovies.git
   cd HoorMovies
   ```
### Configure .env
Copy the example or create your own:
   ```bash
   cp .env.example .env
   # or manually create .env following the format above
   ```

### Build & Run with Docker Compose
   ```bash
   chmod +x scripts/init_cinema.sh
   docker-compose up --build -d
   ```
PostgreSQL and Django services will start
API available at http://localhost:8000/

### Optional: Run Locally without Docker
   ```bash
   cd movies
   poetry install
   poetry run python manage.py migrate
   poetry run python manage.py runserver
   ```

## Running Tests
   ```bash
   cd movies
   poetry run pytest
   ```
### Coverage
   ```bash
   poetry run pytest \
  --cov=. \
  --cov-report=term \
  --cov-report=term-missing

   ```

## Creating a Superuser
From inside the Docker container or locally:
   ```bash
   python manage.py createsuperuser \
   --username admin \
   --password admin
   ```

## API Endpoints
All responses are JSON. Protected endpoints require:

Authorization: Bearer <ACCESS_TOKEN> header

OR DRF session login at /api-auth/login/ + cookie

### Authentication & JWT
| Method | Endpoint              | Description                        |
| ------ | --------------------- | ---------------------------------- |
| POST   | `/auth/register/` | Register a new spectator           |
| POST   | `/auth/login/`    | Obtain JWT access & refresh tokens |
| POST   | `/auth/logout/`   | Blacklist a refresh token (logout) |
| POST   | `/auth/token/refresh/` | Refresh the access token           |
| POST   | `/auth/token/verify/`  | Verify token validity              |


### Authors
| Method | Endpoint             | Description                                    |
| ------ | -------------------- | ---------------------------------------------- |
| GET    | `/authors/`          | List all authors                               |
| GET    | `/authors/{id}/`     | Retrieve a single author                       |
| POST   | `/authors/`          | Create a new author (protected)                |
| PUT    | `/authors/{id}/`     | Update an author (protected)                   |
| PATCH  | `/authors/{id}/`     | Partial update (protected)                     |
| DELETE | `/authors/{id}/`     | Delete only if no films associated (protected) |

### Films
| Method | Endpoint                      | Description                                          |
| ------ | ----------------------------- | ---------------------------------------------------- |
| GET    | `/films/`                 | List all films                                       |
| GET    | `/films/?status={status}` | Filter by status (planned, released, archived, etc.) |
| GET    | `/films/?rating={rating}` | Filter by rating (bad, average, good, excellent)     |
| GET    | `/films/?source={source}` | Filter by source (admin,tmdb)     |
| GET    | `/films/{id}/`            | Retrieve a single film                               |
| POST   | `/films/`                 | Create a new film (protected)                        |
| PUT    | `/films/{id}/`            | Replace a film (protected)                           |
| PATCH  | `/films/{id}/`            | Partial update (protected)                           |
| DELETE | `/films/{id}/`            | Delete a film (protected)                            |
| POST   | `/films/{id}/archive/`    | Archive a film (status → archived) (protected)       |

### Spectators
| Method | Endpoint                | Description                    |
| ------ | ----------------------- | ------------------------------ |
| GET    | `/spectators/`      | List all spectators            |
| GET    | `/spectators/{id}/` | Retrieve a spectator           |
| POST   | `/spectators/`      | Create a spectator (protected) |
| PUT    | `/spectators/{id}/` | Update a spectator (protected) |
| PATCH  | `/spectators/{id}/` | Partial update (protected)     |
| DELETE | `/spectators/{id}/` | Delete a spectator (protected) |

### Favorites
| Method | Endpoint                           | Description                            |
| ------ | ---------------------------------- | -------------------------------------- |
| GET    | `/favorites/`                  | List your favorite films (protected)   |
| POST   | `/favorites/{film_id}/add/`    | Add film to favorites (protected)      |
| POST   | `/favorites/{film_id}/remove/` | Remove film from favorites (protected) |

### Ratings

| Method | Endpoint                  | Description                                                     |
| ------ | ------------------------- | --------------------------------------------------------------- |
| GET    | `/ratings/`           | List all ratings (requires authentication)                      |
| GET    | `/ratings/{id}/`      | Retrieve a single rating by its ID                              |
| POST   | `/ratings/`           | Create or update a rating for a "film" or an "author" (upserts)     |
| PUT    | `/ratings/{id}/`      | Replace an existing rating                                      |
| PATCH  | `/ratings/{id}/`      | Partially update an existing rating                             |
| DELETE | `/ratings/{id}/`      | Delete a rating                                                 |

When you `POST` to `/ratings/`, if you’ve already rated the same target (same spectator, content_type & object_id), your rating will be updated; otherwise a new one is created.

#### Example: Rate a Film
   ```bash
   curl -X POST http://localhost:8000/ratings/ \
   -H "Authorization: Bearer <ACCESS_TOKEN>" \
   -H "Content-Type: application/json" \
   -d '{
      "content_type": "film", 
      "object_id": 42,
      "score": 5,
      "comment": "Un chef-d’œuvre !"
   }'
   ```

## Notes
Anonymous users can perform read-only (GET) operations on authors and films.

Use the DRF browsable API and login at http://localhost:8000/api-auth/login/ if you prefer session-based auth in the browser.

The Django admin interface is at http://localhost:8000/admin/.