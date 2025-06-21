lint:
    black . && isort .


docker-up:
    docker compose up -d
docker-down:
    docker compose down