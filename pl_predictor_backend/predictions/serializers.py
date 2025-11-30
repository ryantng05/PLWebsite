from rest_framework import serializers
from .models import Team, Match, Prediction, ModelPerformance


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'short_name', 'created_at']


class TeamStatsSerializer(serializers.Serializer):
    """Serializer for detailed team statistics"""
    id = serializers.IntegerField()
    name = serializers.CharField()
    short_name = serializers.CharField()
    matches_played = serializers.IntegerField()
    wins = serializers.IntegerField()
    draws = serializers.IntegerField()
    losses = serializers.IntegerField()
    points = serializers.IntegerField()
    goals_for = serializers.IntegerField()
    goals_against = serializers.IntegerField()
    goal_difference = serializers.IntegerField()
    win_rate = serializers.FloatField()
    avg_goals_scored = serializers.FloatField()
    avg_goals_conceded = serializers.FloatField()


class MatchSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.name', read_only=True)
    opponent_name = serializers.CharField(source='opponent.name', read_only=True)
    
    class Meta:
        model = Match
        fields = [
            'id', 'team', 'team_name', 'opponent', 'opponent_name', 'date', 'time', 'venue',
            'result', 'goals_for', 'goals_against', 'shots', 'shots_on_target', 'distance',
            'free_kicks', 'penalties', 'penalty_attempts', 'home_away', 'opponent_code',
            'hour', 'day_of_week', 'target', 'gf_rolling', 'ga_rolling', 'sh_rolling',
            'sot_rolling', 'dist_rolling', 'fk_rolling', 'pk_rolling', 'pkatt_rolling',
            'created_at', 'updated_at'
        ]


class PredictionSerializer(serializers.ModelSerializer):
    match_detail = MatchSerializer(source='match', read_only=True)
    
    class Meta:
        model = Prediction
        fields = [
            'id', 'match', 'match_detail', 'predicted_result', 'confidence',
            'model_version', 'created_at'
        ]


class ModelPerformanceSerializer(serializers.ModelSerializer):
    training_date = serializers.DateTimeField(source='created_at', read_only=True)
    test_set_size = serializers.IntegerField(source='test_matches_count', read_only=True)
    feature_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ModelPerformance
        fields = [
            'id', 'model_version', 'accuracy', 'precision', 'recall',
            'f1_score', 'training_date', 'test_set_size', 'feature_count'
        ]
    
    def get_feature_count(self, obj):
        # Return the number of features used in the model
        # Base predictors + rolling predictors + derived predictors
        return 4 + 8 + 1  # home_away, opponent_code, hour, day_of_week + 8 rolling + goal_diff_rolling


class PredictionRequestSerializer(serializers.Serializer):
    team_id = serializers.IntegerField()
    opponent_id = serializers.IntegerField()
    date = serializers.DateTimeField()
    venue = serializers.ChoiceField(choices=[('H', 'Home'), ('A', 'Away')])
    
    def validate(self, data):
        # Validate that team and opponent are different
        if data['team_id'] == data['opponent_id']:
            raise serializers.ValidationError("Team and opponent must be different")
        return data
