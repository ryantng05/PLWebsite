# Docker Setup Guide for Premier League Predictor

This guide explains how to run the Premier League Predictor application using Docker for PostgreSQL and optional full containerization.

## 🐳 Docker Options

### Option 1: PostgreSQL Only (Recommended for Development)
Run only PostgreSQL in Docker while keeping Django and Next.js running locally.

### Option 2: Full Docker Setup
Run the entire application stack in Docker containers.

## 🚀 Quick Start - PostgreSQL Only

### 1. Start PostgreSQL Database

```bash
# Start PostgreSQL container
docker-compose up -d postgres

# Check if it's running
docker-compose ps
```

### 2. Set Up Django Backend (Local)

```bash
cd pl_predictor_backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Import CSV data
python manage.py import_csv_data ../matches.csv

# Start Django server
python manage.py runserver
```

### 3. Set Up Next.js Frontend (Local)

```bash
cd pl_predictor_frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## 🐳 Full Docker Setup

### Start Everything with Docker

```bash
# Start all services
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop all services
docker-compose -f docker-compose.dev.yml down
```

### Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/
- **pgAdmin**: http://localhost:5050

## 🗄️ Database Management

### Using pgAdmin (Web Interface)

1. Open http://localhost:5050
2. Login with:
   - Email: `admin@example.com`
   - Password: `admin`
3. Add new server:
   - Host: `postgres` (or `localhost` if accessing from host)
   - Port: `5432`
   - Username: `postgres`
   - Password: `password`

### Using Command Line

```bash
# Connect to PostgreSQL container
docker-compose exec postgres psql -U postgres -d pl_predictor

# Run SQL commands
\dt  # List tables
\q   # Quit
```

## 📊 Data Management

### Import CSV Data

```bash
# If running Django locally
cd pl_predictor_backend
python manage.py import_csv_data ../matches.csv

# If running in Docker
docker-compose exec backend python manage.py import_csv_data matches.csv
```

### Reset Database

```bash
# Stop containers
docker-compose down

# Remove volume (this will delete all data!)
docker volume rm plwebsite_postgres_data

# Start fresh
docker-compose up -d postgres
```

## 🔧 Development Commands

### Database Operations

```bash
# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Access Django shell
docker-compose exec backend python manage.py shell
```

### Container Management

```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs postgres
docker-compose logs backend
docker-compose logs frontend

# Restart a service
docker-compose restart postgres

# Execute commands in container
docker-compose exec backend bash
docker-compose exec postgres bash
```

## 🐛 Troubleshooting

### PostgreSQL Connection Issues

```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check PostgreSQL logs
docker-compose logs postgres

# Test connection
docker-compose exec postgres pg_isready -U postgres
```

### Port Conflicts

If you have port conflicts, modify the ports in `docker-compose.yml`:

```yaml
services:
  postgres:
    ports:
      - "5433:5432"  # Change 5432 to 5433
```

Then update Django settings:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pl_predictor',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5433',  # Updated port
    }
}
```

### Reset Everything

```bash
# Stop and remove all containers
docker-compose down

# Remove all volumes (WARNING: This deletes all data!)
docker volume prune

# Remove all images
docker image prune -a

# Start fresh
docker-compose up -d postgres
```

## 📁 File Structure

```
PLWebsite/
├── docker-compose.yml          # PostgreSQL only
├── docker-compose.dev.yml      # Full stack
├── init-db/                    # Database initialization
├── pl_predictor_backend/
│   ├── Dockerfile
│   └── .dockerignore
├── pl_predictor_frontend/
│   ├── Dockerfile
│   └── .dockerignore
├── setup.sh                    # Linux/macOS setup script
├── setup.bat                   # Windows setup script
└── matches.csv                 # Sample data
```

## 🔐 Environment Variables

### Backend Environment Variables

Create a `.env` file in `pl_predictor_backend/`:

```env
DEBUG=1
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://postgres:password@localhost:5432/pl_predictor
```

### Frontend Environment Variables

Create a `.env.local` file in `pl_predictor_frontend/`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## 🚀 Production Deployment

For production, use separate Docker Compose files:

```bash
# Production setup
docker-compose -f docker-compose.prod.yml up -d
```

## 📝 Notes

- The PostgreSQL data is persisted in a Docker volume
- pgAdmin provides a web interface for database management
- All services are configured with health checks
- The setup scripts automate the entire process
- Docker containers restart automatically unless stopped

## 🆘 Getting Help

If you encounter issues:

1. Check Docker is running: `docker --version`
2. Check container logs: `docker-compose logs`
3. Verify ports are available: `netstat -tulpn | grep :5432`
4. Reset containers: `docker-compose down && docker-compose up -d`







