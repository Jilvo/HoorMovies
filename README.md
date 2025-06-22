# HoorMovies

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python)](https://www.python.org/)
![Django](https://img.shields.io/badge/django-5.2.3-darkgreen?logo=django)
[![Postgres](https://img.shields.io/badge/Postgres-%23316192.svg?logo=postgresql&logoColor=white)](#)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff)](#)

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
- (Optional) [Poetry](https://python-poetry.org/) for local Python dependency management  

---

## Environment Variables

Create a file named `.env` in the project root with at least:

```dotenv
DJANGO_SECRET_KEY=your-secret-key
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
   docker-compose up --build -d
   ```
PostgreSQL and Django services will start
API available at http://localhost:8000/api/

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
| POST   | `/api/auth/register/` | Register a new spectator           |
| POST   | `/api/auth/login/`    | Obtain JWT access & refresh tokens |
| POST   | `/api/auth/logout/`   | Blacklist a refresh token (logout) |
| POST   | `/api/token/refresh/` | Refresh the access token           |
| POST   | `/api/token/verify/`  | Verify token validity              |


### Authors
| Method | Endpoint             | Description                                    |
| ------ | -------------------- | ---------------------------------------------- |
| GET    | `/api/authors/`      | List all authors                               |
| GET    | `/api/authors/{id}/` | Retrieve a single author                       |
| POST   | `/api/authors/`      | Create a new author (protected)                |
| PUT    | `/api/authors/{id}/` | Update an author (protected)                   |
| PATCH  | `/api/authors/{id}/` | Partial update (protected)                     |
| DELETE | `/api/authors/{id}/` | Delete only if no films associated (protected) |

### Films
| Method | Endpoint                      | Description                                          |
| ------ | ----------------------------- | ---------------------------------------------------- |
| GET    | `/api/films/`                 | List all films                                       |
| GET    | `/api/films/?status={status}` | Filter by status (planned, released, archived, etc.) |
| GET    | `/api/films/?rating={rating}` | Filter by rating (bad, average, good, excellent)     |
| GET    | `/api/films/{id}/`            | Retrieve a single film                               |
| POST   | `/api/films/`                 | Create a new film (protected)                        |
| PUT    | `/api/films/{id}/`            | Replace a film (protected)                           |
| PATCH  | `/api/films/{id}/`            | Partial update (protected)                           |
| DELETE | `/api/films/{id}/`            | Delete a film (protected)                            |
| POST   | `/api/films/{id}/archive/`    | Archive a film (status → archived) (protected)       |

### Spectators
| Method | Endpoint                | Description                    |
| ------ | ----------------------- | ------------------------------ |
| GET    | `/api/spectators/`      | List all spectators            |
| GET    | `/api/spectators/{id}/` | Retrieve a spectator           |
| POST   | `/api/spectators/`      | Create a spectator (protected) |
| PUT    | `/api/spectators/{id}/` | Update a spectator (protected) |
| PATCH  | `/api/spectators/{id}/` | Partial update (protected)     |
| DELETE | `/api/spectators/{id}/` | Delete a spectator (protected) |

### Favorites
| Method | Endpoint                           | Description                            |
| ------ | ---------------------------------- | -------------------------------------- |
| GET    | `/api/favorites/`                  | List your favorite films (protected)   |
| POST   | `/api/favorites/{film_id}/add/`    | Add film to favorites (protected)      |
| POST   | `/api/favorites/{film_id}/remove/` | Remove film from favorites (protected) |


## Notes
Anonymous users can perform read-only (GET) operations on authors and films.

Use the DRF browsable API and login at http://localhost:8000/api-auth/login/ if you prefer session-based auth in the browser.

The Django admin interface is at http://localhost:8000/admin/.