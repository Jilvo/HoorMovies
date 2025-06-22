# HoorMovies


## Contents

- **Backend**: Django REST Framework API, managed with Poetry.
- **Docker**: Docker Compose configuration to run both services together.


## Prerequisites

- Docker & Docker Compose installed.

## Quick Start with Docker Compose

1. Clone the repository:
   ```bash
   git clone https://github.com/Jilvo/HoorMovies.git
   cd <repository-directory>
   ```

2. From the root of the project (where `docker-compose.yml` is located), run:

   ```bash
   docker compose up --build
   ```

- API will be available at http://localhost:8000/api/

3. Run tests:
   ```bash
   cd movies && poetry run pytest
   ```

4. Create SuperUser:
   ```bash
   python manage.py create_superuser \
      --username admin \
      --password admin
   ```

5.You can filter movie by status:
```http://127.0.0.1:8000/api/films/?rating=good&status={status}
```


6.List favorites:
http://127.0.0.1:8000/api/favorites/
http://127.0.0.1:8000/api/favorites/{id}/add/
http://127.0.0.1:8000/api/favorites/{id}/remove/