FROM python:3.12-slim

ENV POETRY_VERSION=2.1.3 \
	POETRY_VIRTUALENVS_CREATE=false \
	POETRY_NO_INTERACTION=1

WORKDIR /app

RUN apt-get update \
	&& apt-get install -y --no-install-recommends libpq5 \
	&& rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 cine_reserve.wsgi:application"]
