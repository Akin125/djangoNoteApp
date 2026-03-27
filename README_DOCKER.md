# Django Note App - Docker Setup (SQLite)

## Quick Start

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Run the App

1. **Build and start container:**
```bash
docker-compose up -d --build
```

2. **Create superuser (admin):**
```bash
docker-compose exec web python manage.py createsuperuser
```

3. **Access the app:**
- App: http://localhost:8000
- Admin: http://localhost:8000/admin

## Useful Commands

### Start containers
```bash
docker-compose up -d
```

### Stop containers
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f web
```

### Run Django commands
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py shell
docker-compose exec web python manage.py test
```

## File Descriptions

- `Dockerfile` - Container image configuration
- `docker-compose.yml` - Container orchestration (single web service with SQLite)
- `.dockerignore` - Files to exclude from Docker build

## Notes

- SQLite database file (`db.sqlite3`) is stored in the container and persists across restarts
- Using Django development server for simplicity
- Database is included in the volume mount so changes persist

