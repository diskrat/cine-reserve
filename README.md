# cine-reserve

Simple Django REST API for listing movies, sessions, and reserving/purchasing tickets.

## Requirements

- Python 3.12+
- Poetry
- PostgreSQL (local or via Docker)

## Quick start (local)

```bash
poetry install --only main
poetry run python manage.py migrate
poetry run python manage.py runserver 0.0.0.0:8000
```

## Docker

```bash
docker compose up --build -d
```

## API routes

- GET `/movies/`
- GET `/movies/<movie_id>/sessions/`
- GET `/sessions/<session_id>/tickets/`
- POST `/tickets/<ticket_id>/reserve/`
- POST `/tickets/<ticket_id>/purchase/`