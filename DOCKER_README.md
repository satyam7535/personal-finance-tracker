# 🐳 Docker Setup for Finance Tracker

This guide explains how to run the Finance Tracker application using Docker and Docker Compose.

## Prerequisites

- **Docker**: Version 20.10 or higher ([Install Docker](https://docs.docker.com/get-docker/))
- **Docker Compose**: Version 2.0 or higher (included with Docker Desktop)

Verify installation:
```bash
docker --version
docker-compose --version
```

## Quick Start

### 1. Clone and Navigate to Project
```bash
cd c:\Users\DELL\Desktop\Assignment\FJ-BE-R2-Satyam-Keshari-IIIT-Pune
```

### 2. Configure Environment Variables

Create a `.env` file from the example:
```bash
cp .env.example .env
```

**Required Configuration** (edit `.env`):
```env
SECRET_KEY=your-long-random-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# Database (Docker Configuration)
DB_NAME=finance_tracker
DB_USER=postgres
DB_PASSWORD=secure-password-here
DB_HOST=db
DB_PORT=5432
```

> **Important**: Change `DB_PASSWORD` and `SECRET_KEY` to secure values!

### 3. Build and Start Services

Build the Docker images:
```bash
docker-compose build
```

Start all services (database + web app):
```bash
docker-compose up -d
```

### 4. Access the Application

Open your browser and navigate to:
- **Application**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

## Common Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Web service only
docker-compose logs -f web

# Database service only
docker-compose logs -f db
```

### Check Service Status
```bash
docker-compose ps
```

### Stop Services
```bash
# Stop but keep data
docker-compose stop

# Stop and remove containers (data persists in volumes)
docker-compose down

# Stop and remove everything including data
docker-compose down -v
```

### Restart Services
```bash
docker-compose restart
```

### Run Django Management Commands

```bash
# Create superuser
docker-compose exec web python manage.py createsuperuser

# Run migrations
docker-compose exec web python manage.py migrate

# Collect static files
docker-compose exec web python manage.py collectstatic

# Open Django shell
docker-compose exec web python manage.py shell

# Access database shell
docker-compose exec web python manage.py dbshell
```

### Execute Commands in Container
```bash
# Open bash shell in web container
docker-compose exec web bash

# Connect directly to PostgreSQL
docker-compose exec db psql -U postgres -d finance_tracker
```

## Architecture

The Docker setup consists of two services:

### 1. Database Service (`db`)
- **Image**: PostgreSQL 15 Alpine
- **Port**: 5432
- **Volume**: `postgres_data` (persists database across restarts)
- **Health Check**: Ensures database is ready before web service starts

### 2. Web Service (`web`)
- **Base**: Python 3.11 Slim
- **Port**: 8000
- **Server**: Gunicorn with 4 workers
- **Dependencies**: Automatically waits for database to be healthy
- **Volumes**:
  - `./media` - Uploaded receipts and files
  - `./staticfiles` - Collected static files
  - Source code (for development hot-reload)

## Environment Variables

### Required
| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `your-secret-key-123` |
| `DB_PASSWORD` | PostgreSQL password | `secure-password` |

### Optional
| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `False` |
| `ALLOWED_HOSTS` | Comma-separated hosts | `localhost,127.0.0.1` |
| `DB_NAME` | Database name | `finance_tracker` |
| `DB_USER` | Database user | `postgres` |
| `DB_HOST` | Database host | `db` |
| `DB_PORT` | Database port | `5432` |
| `GEMINI_API_KEY` | Google Gemini API key | - |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `RESEND_API_KEY` | Resend email API key | - |

## Development vs Production

### Development Mode (Current Setup)
- Source code mounted as volumes (changes reflect immediately)
- `DEBUG=True`
- Console email backend
- SQLite alternative available

### Production Recommendations
1. **Remove volume mounts** for source code in `docker-compose.yml`
2. **Set** `DEBUG=False`
3. **Use strong passwords** for database
4. **Configure proper email backend** (Resend API)
5. **Set ALLOWED_HOSTS** to your domain
6. **Use environment secrets** management
7. **Enable HTTPS** with reverse proxy (nginx)

## Troubleshooting

### Port Already in Use
If port 8000 or 5432 is already in use:
```bash
# Check what's using the port
netstat -ano | findstr :8000

# Change ports in docker-compose.yml
ports:
  - "8001:8000"  # Changed from 8000:8000
```

### Database Connection Issues
```bash
# Check database is healthy
docker-compose ps

# View database logs
docker-compose logs db

# Restart services
docker-compose restart
```

### Permission Issues (Linux/Mac)
```bash
# Fix media/static directory permissions
sudo chown -R $USER:$USER media staticfiles
```

### Reset Database
```bash
# Stop services and remove volumes
docker-compose down -v

# Start fresh
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate
```

### View Real-Time Logs
```bash
docker-compose logs -f --tail=100
```

## File Structure

```
finance_tracker/
├── Dockerfile                 # Container image definition
├── docker-compose.yml         # Multi-container orchestration
├── docker-entrypoint.sh       # Startup script
├── .dockerignore             # Files excluded from image
├── .env                      # Environment variables (create from .env.example)
├── .env.example              # Template for environment variables
├── requirements.txt          # Python dependencies
├── manage.py                 # Django management
├── build.sh                  # Production build script
└── DOCKER_README.md          # This file
```

## Production Deployment

For production deployment:

1. **Build optimized image**:
   ```bash
   docker build -t finance-tracker:latest .
   ```

2. **Use Docker secrets** for sensitive data
3. **Set up reverse proxy** (nginx/Traefik)
4. **Configure SSL/TLS** certificates
5. **Use managed PostgreSQL** service (recommended)
6. **Set up monitoring** and logging
7. **Configure automated backups**

## Support

For issues or questions:
- Check application logs: `docker-compose logs -f web`
- Check database logs: `docker-compose logs -f db`
- Review Django settings: `finance_tracker/settings.py`
- Verify environment variables: `.env` file

## License

This Docker configuration is part of the Finance Tracker project.
