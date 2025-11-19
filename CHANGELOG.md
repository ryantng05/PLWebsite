# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Add more ML algorithms (XGBoost, Neural Networks)
- Implement player-specific predictions
- Add live score integration
- Create mobile app
- Add user authentication

## [1.0.0] - 2025-10-30

### Added
- Initial release of Premier League Match Predictor
- Django REST API backend with PostgreSQL database
- Next.js frontend with TypeScript and Tailwind CSS
- Random Forest machine learning model for match predictions
- Team statistics and analytics dashboard
- Model performance tracking and retraining capability
- Docker and Docker Compose support for easy deployment
- pgAdmin integration for database management
- Comprehensive API documentation
- Import CSV data management command
- Responsive mobile-friendly UI
- Real-time prediction with probability scores
- Recent form visualization for teams
- Win/Draw/Loss probability distributions
- Confidence scoring for predictions

### Features

#### Backend
- RESTful API with Django REST Framework 3.16
- PostgreSQL database with full schema
- Machine learning prediction service
- Team and match data models
- Custom management commands for data import
- CORS support for frontend integration
- Pagination support for all list endpoints
- Error handling and validation

#### Frontend
- Modern React 18 with Next.js 15
- TypeScript for type safety
- Tailwind CSS for responsive design
- Tabbed interface (Predict, Teams, Model)
- Dynamic team selection dropdowns
- Real-time API integration
- Loading states and error handling
- Prediction history tracking
- Team statistics visualization
- Model performance dashboard

#### Machine Learning
- Random Forest Classifier implementation
- Feature engineering from match data
- Rolling averages for team form
- Venue-specific predictions (Home/Away)
- ~65-70% prediction accuracy
- Performance metrics tracking

#### DevOps
- Docker support for all services
- Docker Compose for orchestration
- Development and production configurations
- Automated database initialization
- Volume persistence for data
- Environment variable configuration

### Technical Details

#### Dependencies
**Backend:**
- Django 5.2.7
- djangorestframework 3.16.1
- django-cors-headers 4.9.0
- psycopg2-binary 2.9.11
- pandas 2.3.3
- scikit-learn 1.7.2
- numpy 2.3.3

**Frontend:**
- Next.js 15.1.4
- React 19.0.0
- TypeScript 5.7.3
- Tailwind CSS 4.0.1
- Axios 1.7.9

#### Database Schema
- Teams table with statistics
- Matches table with full match data
- Predictions table for tracking
- Model Performance table for metrics

### Security
- Environment variable configuration
- CORS restrictions
- SQL injection prevention through ORM
- Input validation on all endpoints
- Secure password hashing for admin

### Documentation
- Comprehensive README.md
- API endpoint documentation
- Docker setup guide
- Contributing guidelines
- Code of conduct
- MIT License

### Known Issues
- Model needs periodic retraining with new data
- Initial load may be slow for large datasets
- No authentication system yet (planned for v2.0)

## [0.1.0] - 2025-10-29

### Added
- Initial project setup
- Basic Django backend structure
- PostgreSQL database configuration
- CSV data import functionality
- Machine learning model prototype

---

## Version History

- **1.0.0** - Full production release with complete features
- **0.1.0** - Initial development version

## Upgrade Guide

### From 0.1.0 to 1.0.0

1. Update dependencies:
   ```bash
   cd pl_predictor_backend
   pip install -r requirements.txt --upgrade
   
   cd ../pl_predictor_frontend
   npm install
   ```

2. Run migrations:
   ```bash
   python manage.py migrate
   ```

3. Import new data format:
   ```bash
   python manage.py import_csv_data ../matches.csv
   ```

4. Retrain model:
   ```bash
   # Through API:
   curl -X POST http://localhost:8000/api/model/train/
   ```

## Support

For issues, questions, or contributions, please visit:
- [GitHub Issues](https://github.com/yourusername/PLWebsite/issues)
- [Discussions](https://github.com/yourusername/PLWebsite/discussions)

---

**Note**: This changelog follows semantic versioning. Each version number follows the format MAJOR.MINOR.PATCH where:
- MAJOR: Incompatible API changes
- MINOR: New functionality in a backwards compatible manner
- PATCH: Backwards compatible bug fixes

