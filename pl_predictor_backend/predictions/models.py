from django.db import models
from django.utils import timezone


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Match(models.Model):
    RESULT_CHOICES = [
        ('W', 'Win'),
        ('D', 'Draw'),
        ('L', 'Loss'),
    ]
    
    VENUE_CHOICES = [
        ('H', 'Home'),
        ('A', 'Away'),
    ]
    
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches')
    opponent = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='opponent_matches')
    date = models.DateTimeField()
    time = models.TimeField()
    venue = models.CharField(max_length=1, choices=VENUE_CHOICES)
    result = models.CharField(max_length=1, choices=RESULT_CHOICES)
    
    # Match statistics
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)
    shots = models.IntegerField(default=0)
    shots_on_target = models.IntegerField(default=0)
    distance = models.FloatField(default=0.0)
    free_kicks = models.IntegerField(default=0)
    penalties = models.IntegerField(default=0)
    penalty_attempts = models.IntegerField(default=0)
    
    # Computed fields for ML
    home_away = models.IntegerField(default=0)  # 1 for home, 0 for away
    opponent_code = models.IntegerField(default=0)
    hour = models.IntegerField(default=0)
    day_of_week = models.IntegerField(default=0)
    target = models.IntegerField(default=0)  # 1 for win, 0 for loss/draw
    
    # Rolling averages for form
    gf_rolling = models.FloatField(default=0.0)
    ga_rolling = models.FloatField(default=0.0)
    sh_rolling = models.FloatField(default=0.0)
    sot_rolling = models.FloatField(default=0.0)
    dist_rolling = models.FloatField(default=0.0)
    fk_rolling = models.FloatField(default=0.0)
    pk_rolling = models.FloatField(default=0.0)
    pkatt_rolling = models.FloatField(default=0.0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.team.name} vs {self.opponent.name} - {self.date.strftime('%Y-%m-%d')}"
    
    class Meta:
        ordering = ['-date']
        unique_together = ['team', 'opponent', 'date']


class Prediction(models.Model):
    PREDICTION_CHOICES = [
        ('W', 'Win'),
        ('D', 'Draw'),
        ('L', 'Loss'),
    ]
    
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='predictions')
    predicted_result = models.CharField(max_length=1, choices=PREDICTION_CHOICES)
    confidence = models.FloatField(default=0.0)  # 0-1 confidence score
    model_version = models.CharField(max_length=50, default='v1.0')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Prediction for {self.match} - {self.predicted_result} ({self.confidence:.2f})"
    
    class Meta:
        ordering = ['-created_at']


class ModelPerformance(models.Model):
    model_version = models.CharField(max_length=50)
    accuracy = models.FloatField(default=0.0)
    precision = models.FloatField(default=0.0)
    recall = models.FloatField(default=0.0)
    f1_score = models.FloatField(default=0.0)
    test_matches_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.model_version} - Accuracy: {self.accuracy:.3f}"
    
    class Meta:
        ordering = ['-created_at']