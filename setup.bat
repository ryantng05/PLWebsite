@echo off
REM Premier League Predictor Setup Script for Windows
echo 🏆 Setting up Premier League Predictor with Docker PostgreSQL...

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

echo ✅ Docker and Docker Compose are installed

REM Start PostgreSQL with Docker
echo 🐘 Starting PostgreSQL database with Docker...
docker-compose up -d postgres

REM Wait for PostgreSQL to be ready
echo ⏳ Waiting for PostgreSQL to be ready...
:wait_for_postgres
docker-compose exec postgres pg_isready -U postgres >nul 2>&1
if %errorlevel% neq 0 (
    echo Waiting for PostgreSQL...
    timeout /t 2 /nobreak >nul
    goto wait_for_postgres
)

echo ✅ PostgreSQL is ready!

REM Set up Django backend
echo 🐍 Setting up Django backend...
cd pl_predictor_backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Install Python dependencies
echo 📥 Installing Python dependencies...
pip install -r requirements.txt

REM Run Django migrations
echo 🗄️ Running Django migrations...
python manage.py makemigrations
python manage.py migrate

REM Import CSV data
echo 📊 Importing match data from CSV...
python manage.py import_csv_data ..\matches.csv

REM Create superuser (optional)
echo 👤 Creating Django superuser...
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')"

echo ✅ Django backend setup complete!

REM Set up Next.js frontend
echo ⚛️ Setting up Next.js frontend...
cd ..\pl_predictor_frontend

REM Install Node.js dependencies
echo 📦 Installing Node.js dependencies...
npm install

echo ✅ Frontend setup complete!

echo.
echo 🎉 Setup complete! Here's how to run the application:
echo.
echo 1. Start PostgreSQL (if not already running):
echo    docker-compose up -d postgres
echo.
echo 2. Start Django backend:
echo    cd pl_predictor_backend
echo    venv\Scripts\activate
echo    python manage.py runserver
echo.
echo 3. Start Next.js frontend (in a new terminal):
echo    cd pl_predictor_frontend
echo    npm run dev
echo.
echo 4. Access the application:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:8000/api/
echo    Django Admin: http://localhost:8000/admin/
echo    pgAdmin: http://localhost:5050 (admin@example.com / admin)
echo.
echo 🐘 PostgreSQL is running in Docker on port 5432
echo 📊 Database: pl_predictor
echo 👤 Username: postgres
echo 🔑 Password: password
echo.
pause


