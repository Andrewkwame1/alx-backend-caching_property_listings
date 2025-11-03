# ALX Backend Caching - Property Listings

This project demonstrates multi-level caching in a Django application using Redis and containerized services (PostgreSQL and Redis) via Docker Compose.

Services
- web: Django application (runs migrations on start and serves on port 8000)
- postgres: PostgreSQL database
- redis: Redis cache

Quick start (requires Docker & Docker Compose):

PowerShell

```powershell
# build and start services
docker compose up -d --build

# view logs
docker compose logs -f web

# stop services
docker compose down
```

Access the app
- Property list (JSON): http://127.0.0.1:8000/properties/

Notes
- Django is configured to connect to `postgres:5432` and `redis:6379` when running inside the `web` container.
- If you prefer running Django on the host (not inside Docker), set DATABASES HOST to `localhost` and port to the host-mapped Postgres port (currently 5433) and update CACHES location accordingly.

Requirements
- See `requirements.txt` for Python dependencies.

Assessment checklist
- Property model present: `properties/models.py`
- View-level caching implemented: `properties/views.py` with `@cache_page(60*15)`
- Low-level caching and metrics: `properties/utils.py`
- Cache invalidation via signals: `properties/signals.py`
- Docker Compose for Postgres and Redis: `docker-compose.yml`
- Dockerfile and `web` service added to run the Django app in Docker
