# Django Note App - Docker Setup

## Quick Start

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Run the App

1. **Build and start containers:**
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

### Database access
```bash
docker-compose exec db psql -U admin -d djangonoteapp
```

## File Descriptions

- `Dockerfile` - Container image configuration
- `docker-compose.yml` - Multi-container orchestration
- `.dockerignore` - Files to exclude from Docker build
- `.env.example` - Environment variables template

## Troubleshooting

**Port already in use:**
Edit `docker-compose.yml` and change port mappings

**Database connection error:**
```bash
docker-compose down -v
docker-compose up -d --build
```

**View all containers:**
```bash
docker-compose ps
```

