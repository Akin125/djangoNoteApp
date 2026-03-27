# Django Note App - Docker Setup Guide

This guide explains how to containerize and run your Django Note App using Docker and Docker Compose.

## Prerequisites

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)
- Git (optional, for version control)

## Quick Start

### 1. Clone or Download the Project

```bash
cd djangoNoteApp
```

### 2. Set Up Environment Variables

Copy the example environment file and customize it:

```bash
cp .env.example .env
```

Edit `.env` and update the following (if needed):
- `SECRET_KEY`: Use a strong secret key for production
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Add your domain names or IP addresses
- `DB_PASSWORD`: Set a strong database password

### 3. Build and Run Containers

Build the Docker image:

```bash
docker-compose build
```

Start the containers:

```bash
docker-compose up -d
```

The application will be available at `http://localhost:8000`

### 4. Create a Superuser (for Django Admin)

```bash
docker-compose exec web python manage.py createsuperuser
```

Follow the prompts to create an admin account. Then access Django admin at:
- URL: `http://localhost:8000/admin`
- Username: your chosen username
- Password: your chosen password

### 5. View Logs

```bash
docker-compose logs -f web
```

To see database logs:

```bash
docker-compose logs -f db
```

## Common Docker Compose Commands

### Start Containers
```bash
docker-compose up -d
```

### Stop Containers
```bash
docker-compose down
```

### Rebuild Containers
```bash
docker-compose down
docker-compose build
docker-compose up -d
```

### View Running Containers
```bash
docker-compose ps
```

### Run Django Commands
```bash
# Make migrations
docker-compose exec web python manage.py makemigrations

# Apply migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Run tests
docker-compose exec web python manage.py test

# Access Django shell
docker-compose exec web python manage.py shell
```

### View Database
```bash
# Connect to PostgreSQL
docker-compose exec db psql -U noteuser -d djangoNoteApp
```

## Project Structure

```
djangoNoteApp/
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Multi-container orchestration
├── .dockerignore          # Files/folders to ignore in Docker
├── .env.example           # Example environment variables
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── djangoNoteApp/         # Django project folder
│   ├── __init__.py
│   ├── settings.py        # Django settings
│   ├── urls.py           # URL configuration
│   ├── asgi.py           # ASGI application
│   └── wsgi.py           # WSGI application (for Gunicorn)
└── [apps]/                # Your Django apps
```

## Services

### Web Service
- Built from Dockerfile
- Runs Gunicorn WSGI server
- Exposes port 8000
- Volumes for code hot-reload and static files
- Environment variables from .env file

### Database Service
- PostgreSQL 15 Alpine image
- Exposes port 5432
- Persistent volume for data
- Health checks enabled

## Volumes

- `postgres_data`: PostgreSQL database persistence
- `static_volume`: Django static files
- `media_volume`: User-uploaded media files

## Networking

Services communicate through the `noteapp_network` bridge network. The web service connects to the database using the hostname `db`.

## Production Considerations

For production deployment:

1. **Security**
   - Change `SECRET_KEY` in `.env` to a strong, random value
   - Set `DEBUG=False`
   - Use a proper secret management system
   - Update `ALLOWED_HOSTS` with your domain

2. **Database**
   - Use managed database services (AWS RDS, Google Cloud SQL, etc.)
   - Enable database backups
   - Set strong passwords

3. **Static Files**
   - Use cloud storage (AWS S3, Google Cloud Storage) for static files
   - Use a CDN for better performance

4. **Reverse Proxy**
   - Use Nginx or Apache as a reverse proxy in front of Gunicorn
   - Enable HTTPS/SSL

5. **Monitoring**
   - Set up logging and monitoring
   - Use health check endpoints

## Troubleshooting

### Port Already in Use
If port 8000 or 5432 is already in use:

```bash
# Change port in docker-compose.yml
# Change "8000:8000" to "8001:8000" for example
```

### Database Connection Error
Check database logs:
```bash
docker-compose logs db
```

Ensure database is healthy:
```bash
docker-compose ps
```

### Static Files Not Loading
Collect static files:
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Permission Denied Errors
The containers run as a non-root user. Ensure proper file permissions:
```bash
docker-compose exec web chmod +x manage.py
```

## Cleanup

Remove all containers, networks, and volumes:

```bash
docker-compose down -v
```

Remove Docker images:

```bash
docker rmi djangonoteapp-web
```

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django Deployment Documentation](https://docs.djangoproject.com/en/stable/howto/deployment/)
- [Gunicorn Documentation](https://gunicorn.org/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres/)

## Support

For issues or questions:
1. Check Docker and Docker Compose installation
2. Review error logs with `docker-compose logs`
3. Verify environment variables in `.env` file
4. Ensure ports 8000 and 5432 are not blocked by firewall

---

Happy containerizing! 🐳

