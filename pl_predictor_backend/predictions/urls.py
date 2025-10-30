from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'predictions'

urlpatterns = [
    # Teams
    path('teams/', views.TeamListView.as_view(), name='team-list'),
    path('teams/<int:pk>/', views.TeamDetailView.as_view(), name='team-detail'),
    path('teams/<int:team_id>/stats/', views.team_stats, name='team-stats'),
    
    # Matches
    path('matches/', views.MatchListView.as_view(), name='match-list'),
    path('matches/<int:pk>/', views.MatchDetailView.as_view(), name='match-detail'),
    path('matches/upcoming/', views.upcoming_matches, name='upcoming-matches'),
    
    # Predictions
    path('predictions/', views.PredictionListView.as_view(), name='prediction-list'),
    path('predictions/<int:pk>/', views.PredictionDetailView.as_view(), name='prediction-detail'),
    path('predict/', views.PredictMatchView.as_view(), name='predict-match'),
    
    # Model management
    path('model/train/', views.train_model, name='train-model'),
    path('model/info/', views.model_info, name='model-info'),
    path('model/performance/', views.ModelPerformanceListView.as_view(), name='model-performance'),
]
