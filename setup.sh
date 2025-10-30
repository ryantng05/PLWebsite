#!/bin/bash

# Premier League Predictor Setup Script
echo "🏆 Setting up Premier League Predictor with Docker PostgreSQL..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Start PostgreSQL with Docker
echo "🐘 Starting PostgreSQL database with Docker..."
docker-compose up -d postgres

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
until docker-compose exec postgres pg_isready -U postgres; do
    echo "Waiting for PostgreSQL..."
    sleep 2
done

echo "✅ PostgreSQL is ready!"

# Set up Django backend
echo "🐍 Setting up Django backend..."

cd pl_predictor_backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate 2>/dev/null || venv\Scripts\activate 2>/dev/null

# Install Python dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Run Django migrations
echo "🗄️ Running Django migrations..."
python manage.py makemigrations
python manage.py migrate

# Import CSV data
echo "📊 Importing match data from CSV..."
python manage.py import_csv_data ../matches.csv

# Create superuser (optional)
echo "👤 Creating Django superuser..."
python manage.py createsuperuser --noinput --username admin --email admin@example.com || echo "Superuser already exists"

echo "✅ Django backend setup complete!"

# Set up Next.js frontend
echo "⚛️ Setting up Next.js frontend..."

cd ../pl_predictor_frontend

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

echo "✅ Frontend setup complete!"

echo ""
echo "🎉 Setup complete! Here's how to run the application:"
echo ""
echo "1. Start PostgreSQL (if not already running):"
echo "   docker-compose up -d postgres"
echo ""
echo "2. Start Django backend:"
echo "   cd pl_predictor_backend"
echo "   source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
echo "   python manage.py runserver"
echo ""
echo "3. Start Next.js frontend (in a new terminal):"
echo "   cd pl_predictor_frontend"
echo "   npm run dev"
echo ""
echo "4. Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000/api/"
echo "   Django Admin: http://localhost:8000/admin/"
echo "   pgAdmin: http://localhost:5050 (admin@example.com / admin)"
echo ""
echo "🐘 PostgreSQL is running in Docker on port 5432"
echo "📊 Database: pl_predictor"
echo "👤 Username: postgres"
echo "🔑 Password: password"


