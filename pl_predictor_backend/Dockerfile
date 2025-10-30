FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        gcc \
        python3-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Create a script to run the application
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
echo "Waiting for PostgreSQL..."\n\
while ! pg_isready -h postgres -p 5432 -U postgres; do\n\
  sleep 1\n\
done\n\
\n\
echo "PostgreSQL is ready!"\n\
\n\
echo "Running migrations..."\n\
python manage.py migrate\n\
\n\
echo "Importing CSV data..."\n\
python manage.py import_csv_data matches.csv || echo "CSV import failed or already imported"\n\
\n\
echo "Starting Django development server..."\n\
python manage.py runserver 0.0.0.0:8000\n\
' > /app/start.sh && chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"]


