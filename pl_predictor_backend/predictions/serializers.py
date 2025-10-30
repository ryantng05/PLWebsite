from rest_framework import serializers
from .models import Team, Match, Prediction, ModelPerformance


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'short_name', 'created_at']


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
    class Meta:
        model = ModelPerformance
        fields = [
            'id', 'model_version', 'accuracy', 'precision', 'recall',
            'f1_score', 'test_matches_count', 'created_at'
        ]


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
