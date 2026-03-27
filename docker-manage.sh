#!/bin/bash

# Django Note App Docker Management Script
# Usage: ./docker-manage.sh [command]

set -e

PROJECT_NAME="djangonoteapp"
WEB_SERVICE="web"
DB_SERVICE="db"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

show_help() {
    cat << EOF
Django Note App Docker Management Script

Usage: ./docker-manage.sh [command]

Commands:
  build               Build Docker images
  up                  Start all containers in background
  down                Stop and remove containers
  logs                View logs from all services
  logs-web            View logs from web service
  logs-db             View logs from database service
  shell               Access Django shell
  migrate             Run database migrations
  makemigrations      Create migration files
  createsuperuser     Create Django superuser
  collectstatic       Collect static files
  test                Run tests
  bash                Access web container bash shell
  ps                  Show running containers
  clean               Remove all containers and volumes
  restart             Restart all containers
  prod-up             Start with Nginx (production setup)
  help                Show this help message

Examples:
  ./docker-manage.sh build
  ./docker-manage.sh up
  ./docker-manage.sh migrate
  ./docker-manage.sh logs-web
EOF
}

case "$1" in
    build)
        print_info "Building Docker images..."
        docker-compose build
        ;;

    up)
        print_info "Starting containers..."
        docker-compose up -d
        print_info "Containers started! Access app at http://localhost:8000"
        ;;

    down)
        print_info "Stopping containers..."
        docker-compose down
        ;;

    logs)
        docker-compose logs -f
        ;;

    logs-web)
        docker-compose logs -f web
        ;;

    logs-db)
        docker-compose logs -f db
        ;;

    shell)
        print_info "Starting Django shell..."
        docker-compose exec web python manage.py shell
        ;;

    migrate)
        print_info "Running migrations..."
        docker-compose exec web python manage.py migrate
        ;;

    makemigrations)
        print_info "Creating migrations..."
        docker-compose exec web python manage.py makemigrations
        ;;

    createsuperuser)
        print_info "Creating superuser..."
        docker-compose exec web python manage.py createsuperuser
        ;;

    collectstatic)
        print_info "Collecting static files..."
        docker-compose exec web python manage.py collectstatic --noinput
        ;;

    test)
        print_info "Running tests..."
        docker-compose exec web python manage.py test
        ;;

    bash)
        print_info "Opening bash shell in web container..."
        docker-compose exec web bash
        ;;

    ps)
        print_info "Running containers:"
        docker-compose ps
        ;;

    clean)
        print_warning "This will remove all containers and volumes!"
        read -p "Are you sure? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker-compose down -v
            print_info "Cleanup complete"
        else
            print_info "Cleanup cancelled"
        fi
        ;;

    restart)
        print_info "Restarting containers..."
        docker-compose restart
        ;;

    prod-up)
        print_info "Starting containers with Nginx (Production)..."
        docker-compose -f docker-compose.prod.yml up -d
        print_info "Application running with Nginx at http://localhost"
        ;;

    help|"")
        show_help
        ;;

    *)
        print_error "Unknown command: $1"
        echo "Run './docker-manage.sh help' for usage information"
        exit 1
        ;;
esac

