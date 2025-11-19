# ⚽ Premier League Match Predictor

<div align="center">

![Premier League](https://img.shields.io/badge/Premier%20League-Predictor-38003c?style=for-the-badge&logo=premier-league)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-15-000000?style=for-the-badge&logo=next.js&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)

**AI-powered Premier League match outcome predictions using machine learning**

[Features](#-features) • [Tech Stack](#-tech-stack) • [Quick Start](#-quick-start) • [Usage](#-usage) • [API Documentation](#-api-documentation) • [Contributing](#-contributing)

</div>

---

## 📖 About

Premier League Match Predictor is a full-stack web application that uses machine learning to predict the outcomes of Premier League football matches. Built with a Random Forest Classifier, the system analyzes historical match data including goals, possession, shots, and other performance metrics to provide accurate win/draw/loss predictions with confidence scores.

### 🎯 Key Highlights

- **🤖 Machine Learning**: Random Forest algorithm trained on historical Premier League data
- **📊 Real-time Predictions**: Get instant match outcome predictions with probability scores
- **📈 Team Statistics**: Comprehensive team performance metrics and recent form analysis
- **🎨 Modern UI**: Beautiful, responsive interface built with Next.js and Tailwind CSS
- **🔄 RESTful API**: Well-documented Django REST Framework API
- **🐳 Docker Ready**: Easy deployment with Docker and Docker Compose

---

## ✨ Features

### 🔮 Match Prediction
- Predict match outcomes (Win/Draw/Loss) with confidence scores
- View probability distributions for all possible outcomes
- Historical prediction tracking and accuracy metrics

### 📊 Team Analytics
- Comprehensive team statistics (wins, losses, draws, goals)
- Recent form visualization (last 5 matches)
- Win rate and goal differential analysis
- Head-to-head comparisons

### 🤖 Model Performance
- View ML model accuracy, precision, recall, and F1 scores
- Track model improvements over time
- Retrain model with latest data
- Feature importance analysis

### 🎨 User Interface
- Clean, intuitive tabbed interface
- Mobile-responsive design
- Real-time data loading with smooth animations
- Error handling with user-friendly messages

---

## 🛠 Tech Stack

### Backend
- **Django 5.2** - Python web framework
- **Django REST Framework 3.16** - RESTful API
- **PostgreSQL** - Primary database
- **Scikit-learn 1.7** - Machine learning
- **Pandas 2.3** - Data manipulation
- **NumPy 2.3** - Numerical computing

### Frontend
- **Next.js 15** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **React Hooks** - State management

### DevOps
- **Docker & Docker Compose** - Containerization
- **pgAdmin** - Database management
- **Git** - Version control

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 16+ (or use Docker)
- Git

### Option 1: Docker Setup (Recommended)

**1. Clone the repository:**
```bash
git clone https://github.com/yourusername/PLWebsite.git
cd PLWebsite
```

**2. Start PostgreSQL with Docker:**
```bash
docker-compose up -d postgres
```

**3. Set up the Django backend:**
```bash
cd pl_predictor_backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py import_csv_data ../matches.csv
python manage.py runserver
```

**4. Set up the Next.js frontend:**
```bash
cd ../pl_predictor_frontend
npm install
npm run dev
```

**5. Access the application:**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/
- **pgAdmin**: http://localhost:5050

### Option 2: Full Docker Setup

Run the entire stack with Docker Compose:

```bash
docker-compose -f docker-compose.dev.yml up --build
```

All services will start automatically.

---

## 📚 Usage

### Making Predictions

1. Navigate to the **Predict** tab
2. Select the home team and away team from the dropdowns
3. Choose the match date and venue (Home/Away)
4. Click **Predict Match** to get results

### Viewing Team Statistics

1. Go to the **Teams** tab
2. Select a team from the dropdown
3. View comprehensive statistics including:
   - Match record (W/D/L)
   - Goals for/against
   - Recent form
   - Win rate

### Model Performance

1. Navigate to the **Model** tab
2. View current model metrics
3. Click **Train Model** to retrain with latest data
4. Track performance improvements over time

---

## 🔌 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Endpoints

#### Teams
```http
GET /api/teams/
GET /api/teams/{id}/
GET /api/teams/{id}/stats/
```

#### Matches
```http
GET /api/matches/
GET /api/matches/{id}/
```

#### Predictions
```http
POST /api/predict/
GET /api/predictions/
GET /api/predictions/{id}/
```

**Example Prediction Request:**
```json
{
  "team_id": 1,
  "opponent_id": 2,
  "venue": "H",
  "match_date": "2025-11-01"
}
```

**Example Response:**
```json
{
  "id": 1,
  "team": "Arsenal",
  "opponent": "Chelsea",
  "venue": "H",
  "match_date": "2025-11-01",
  "predicted_result": "W",
  "win_probability": 0.65,
  "draw_probability": 0.20,
  "loss_probability": 0.15,
  "confidence": 0.65,
  "created_at": "2025-10-30T10:30:00Z"
}
```

#### Model
```http
POST /api/model/train/
GET /api/model/info/
GET /api/model/performance/
```

---

## 📁 Project Structure

```
PLWebsite/
├── pl_predictor_backend/          # Django backend
│   ├── predictions/               # Main app
│   │   ├── models.py             # Database models
│   │   ├── serializers.py        # DRF serializers
│   │   ├── views.py              # API views
│   │   ├── ml_service.py         # ML prediction logic
│   │   └── management/           # Custom commands
│   ├── pl_predictor_backend/     # Project settings
│   ├── requirements.txt          # Python dependencies
│   └── Dockerfile                # Backend Docker image
│
├── pl_predictor_frontend/         # Next.js frontend
│   ├── src/
│   │   ├── app/                  # Next.js app directory
│   │   ├── components/           # React components
│   │   │   ├── PredictionForm.tsx
│   │   │   ├── PredictionCard.tsx
│   │   │   ├── TeamStats.tsx
│   │   │   └── ModelPerformance.tsx
│   │   └── lib/                  # Utilities
│   │       ├── api.ts            # API client
│   │       └── utils.ts          # Helper functions
│   ├── package.json              # Node dependencies
│   └── Dockerfile                # Frontend Docker image
│
├── matches.csv                    # Historical match data
├── docker-compose.yml             # PostgreSQL + pgAdmin
├── docker-compose.dev.yml         # Full stack setup
└── README.md                      # This file
```

---

## 🔧 Configuration

### Environment Variables

**Backend** (`pl_predictor_backend/.env`):
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://postgres:password@localhost:5432/pl_predictor
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Frontend** (`pl_predictor_frontend/.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### Database Configuration

The application uses PostgreSQL. Connection details:
- **Host**: localhost (or `db` in Docker)
- **Port**: 5432
- **Database**: pl_predictor
- **User**: postgres
- **Password**: password

---

## 🧪 Testing

### Backend Tests
```bash
cd pl_predictor_backend
python manage.py test
```

### Frontend Tests
```bash
cd pl_predictor_frontend
npm test
```

---

## 📊 Machine Learning Model

### Algorithm
- **Model**: Random Forest Classifier
- **Features**: 
  - Goals for/against
  - Possession percentage
  - Shots and shots on target
  - Deep passes completed
  - Expected goals (xG)
  - Home/Away venue
  - Recent form (rolling averages)

### Training
The model is trained on historical Premier League match data with features engineered from:
- Team statistics
- Rolling performance averages
- Venue-specific metrics
- Head-to-head history

### Performance Metrics
- **Accuracy**: ~65-70%
- **Precision**: ~68%
- **Recall**: ~65%
- **F1 Score**: ~66%

---

## 🐳 Docker Services

### PostgreSQL
- **Port**: 5432
- **Credentials**: postgres/password
- **Database**: pl_predictor

### pgAdmin
- **Port**: 5050
- **Email**: admin@admin.com
- **Password**: admin
- **Purpose**: Database management UI

### Django (Dev)
- **Port**: 8000
- **Auto-reload**: Enabled
- **Volume mounted**: Yes

### Next.js (Dev)
- **Port**: 3000
- **Hot reload**: Enabled
- **Volume mounted**: Yes

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 for Python code
- Use TypeScript for all frontend code
- Write tests for new features
- Update documentation as needed
- Keep commits atomic and meaningful

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

---

## 🙏 Acknowledgments

- Premier League for providing match data
- Scikit-learn for the machine learning framework
- Django and Next.js communities for excellent documentation
- All contributors who help improve this project

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/PLWebsite/issues) page
2. Create a new issue with detailed information
3. Join our community discussions

---

## 🗺 Roadmap

- [ ] Add more ML algorithms (XGBoost, Neural Networks)
- [ ] Implement player-specific predictions
- [ ] Add live score integration
- [ ] Create mobile app (React Native)
- [ ] Add user authentication and saved predictions
- [ ] Implement betting odds comparison
- [ ] Add multi-league support
- [ ] Create prediction history dashboard
- [ ] Implement A/B testing for model improvements
- [ ] Add real-time match commentary

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ and ⚽

</div>
