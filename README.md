# Django Note App

A simple yet powerful Django application for creating and managing notes with a RESTful API, user authentication, and Docker support.

## 🎯 Features

- ✅ Create, read, update, and delete notes
- ✅ User authentication with JWT tokens
- ✅ RESTful API with Django REST Framework
- ✅ Admin panel for easy note management
- ✅ SQLite/PostgreSQL database support
- ✅ Docker & Docker Compose containerization
- ✅ Environment variable configuration with python-decouple
- ✅ Production-ready with Gunicorn

## 📚 Tech Stack

- **Backend:** Django 6.0+
- **API:** Django REST Framework
- **Authentication:** JWT (djangorestframework-simplejwt)
- **Database:** SQLite (development) / PostgreSQL (production)
- **Web Server:** Gunicorn
- **Containerization:** Docker & Docker Compose
- **Python:** 3.12

## 📋 Prerequisites

- Python 3.12+
- pip
- PostgreSQL (optional, for production)
- Docker & Docker Compose (for containerized deployment)
- Git

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/djangoNoteApp.git
cd djangoNoteApp
```

### 2. Create Virtual Environment

```bash
python -m venv djangoNoteAppenv
```

**Activate Virtual Environment:**

- **Windows:**
  ```bash
  djangoNoteAppenv\Scripts\activate
  ```
- **macOS/Linux:**
  ```bash
  source djangoNoteAppenv/bin/activate
  ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory with the following variables:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Run Migrations

```bash
cd NoteApp
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 7. Run Development Server

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

- Admin Panel: `http://localhost:8000/admin/`

## 🐳 Docker Setup

### Build and Run with Docker Compose

```bash
docker-compose up --build
```

The application will run on `http://localhost:8000`

To stop the containers:

```bash
docker-compose down
```

To run migrations in Docker:

```bash
docker-compose exec web python manage.py migrate
```

To create a superuser in Docker:

```bash
docker-compose exec web python manage.py createsuperuser
```

## 📁 Project Structure

```
djangoNoteApp/
├── NoteApp/
│   ├── NoteApp/           # Main project configuration
│   │   ├── settings.py    # Django settings
│   │   ├── urls.py        # URL routing
│   │   ├── wsgi.py        # WSGI configuration
│   │   └── asgi.py        # ASGI configuration
│   ├── notes/             # Notes application
│   │   ├── models.py      # Note model definition
│   │   ├── views.py       # API views
│   │   ├── admin.py       # Admin panel configuration
│   │   └── migrations/    # Database migrations
│   └── manage.py          # Django management script
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
└── README.md              # This file
```

## 📦 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/admin/` | GET | Django admin panel |

### Note Model

```python
class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## 🔐 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Debug mode (False in production) | False |
| `SECRET_KEY` | Django secret key | - |
| `DATABASE_URL` | Database connection string | sqlite:///db.sqlite3 |
| `ALLOWED_HOSTS` | Allowed host names | localhost,127.0.0.1 |

## 🛠️ Development Commands

```bash
# Run development server
python manage.py runserver

# Run migrations
python manage.py migrate

# Create migrations for changes
python manage.py makemigrations

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic
```

## 📦 Dependencies

- **Django** (>=4.3) - Web framework
- **djangorestframework** - REST API framework
- **djangorestframework-simplejwt** - JWT authentication
- **psycopg2-binary** - PostgreSQL database adapter
- **gunicorn** (>=20.1.0) - Production WSGI server
- **python-decouple** (>=3.8) - Environment variable management

## 🚢 Production Deployment

### Using Gunicorn

```bash
gunicorn NoteApp.wsgi:application --bind 0.0.0.0:8000
```

### Using Docker

Build the image:

```bash
docker build -t django-note-app .
```

Run the container:

```bash
docker run -p 8000:8000 django-note-app
```

## 📝 Important Security Notes

⚠️ **Before production deployment:**

1. Change `SECRET_KEY` in settings.py
2. Set `DEBUG=False`
3. Configure `ALLOWED_HOSTS` with your domain
4. Use environment variables for sensitive data
5. Set up HTTPS
6. Update CORS settings if using a separate frontend

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Support

For support, email your-email@example.com or open an issue on GitHub.

## 🔗 Useful Links

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [Docker Documentation](https://docs.docker.com/)

---

**Last Updated:** March 2026
