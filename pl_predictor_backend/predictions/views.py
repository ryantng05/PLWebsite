from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from datetime import datetime, timedelta
import logging

from .models import Team, Match, Prediction, ModelPerformance
from .serializers import (
    TeamSerializer, MatchSerializer, PredictionSerializer, 
    ModelPerformanceSerializer, PredictionRequestSerializer
)
from .ml_service import PLPredictionService

logger = logging.getLogger(__name__)

# Initialize the ML service
ml_service = PLPredictionService()


class TeamListView(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class MatchListView(generics.ListCreateAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    
    def get_queryset(self):
        queryset = Match.objects.all()
        
        # Filter by team
        team = self.request.query_params.get('team', None)
        if team:
            queryset = queryset.filter(Q(team__name__icontains=team) | Q(opponent__name__icontains=team))
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        # Filter by result
        result = self.request.query_params.get('result', None)
        if result:
            queryset = queryset.filter(result=result)
        
        return queryset.order_by('-date')


class MatchDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class PredictionListView(generics.ListCreateAPIView):
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer
    
    def get_queryset(self):
        queryset = Prediction.objects.all()
        
        # Filter by team
        team = self.request.query_params.get('team', None)
        if team:
            queryset = queryset.filter(
                Q(match__team__name__icontains=team) | 
                Q(match__opponent__name__icontains=team)
            )
        
        # Filter by date
        date = self.request.query_params.get('date', None)
        if date:
            queryset = queryset.filter(match__date__date=date)
        
        return queryset.order_by('-created_at')


class PredictionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer


class ModelPerformanceListView(generics.ListCreateAPIView):
    queryset = ModelPerformance.objects.all()
    serializer_class = ModelPerformanceSerializer


class PredictMatchView(APIView):
    """API endpoint to predict a match outcome"""
    
    def post(self, request):
        serializer = PredictionRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        
        try:
            # Get team objects
            team = get_object_or_404(Team, id=data['team_id'])
            opponent = get_object_or_404(Team, id=data['opponent_id'])
            
            # Make prediction
            prediction_result = ml_service.predict_match(
                team=team,
                opponent=opponent,
                date=data['date'],
                venue=data['venue']
            )
            
            if not prediction_result:
                return Response(
                    {'error': 'Unable to make prediction. Model may not be trained.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Create prediction record
            prediction = Prediction.objects.create(
                match=None,  # This would be a future match
                predicted_result=prediction_result['predicted_result'],
                confidence=prediction_result['confidence'],
                model_version='v1.0'
            )
            
            # Extract probabilities from the prediction result
            probabilities = prediction_result.get('probabilities', {})
            
            response_data = {
                'id': prediction.id,
                'team': team.name,
                'opponent': opponent.name,
                'match_date': data['date'].isoformat() if hasattr(data['date'], 'isoformat') else str(data['date']),
                'venue': data['venue'],
                'predicted_result': prediction_result['predicted_result'],
                'win_probability': probabilities.get('W', 0.0),
                'draw_probability': probabilities.get('D', 0.0),
                'loss_probability': probabilities.get('L', 0.0),
                'confidence': prediction_result['confidence'],
                'created_at': prediction.created_at.isoformat() if prediction.created_at else None
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Error in PredictMatchView: {str(e)}")
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['POST'])
def train_model(request):
    """Train the machine learning model"""
    try:
        # Get all matches for training
        matches = Match.objects.all()
        
        if not matches.exists():
            return Response(
                {'error': 'No matches found for training'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Train the model
        performance = ml_service.train_model(matches)
        
        if not performance:
            return Response(
                {'error': 'Failed to train model'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Save performance metrics
        model_performance = ModelPerformance.objects.create(
            model_version='v1.0',
            accuracy=performance['accuracy'],
            precision=performance['precision'],
            recall=performance['recall'],
            f1_score=performance['f1_score'],
            test_matches_count=performance['test_matches_count']
        )
        
        return Response({
            'message': 'Model trained successfully',
            'performance': ModelPerformanceSerializer(model_performance).data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error training model: {str(e)}")
        return Response(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def model_info(request):
    """Get information about the current model"""
    try:
        info = ml_service.get_model_info()
        return Response(info, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        return Response(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def upcoming_matches(request):
    """Get upcoming matches that can be predicted"""
    try:
        # Get matches from today onwards
        today = datetime.now().date()
        upcoming = Match.objects.filter(date__date__gte=today).order_by('date')
        
        serializer = MatchSerializer(upcoming, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error getting upcoming matches: {str(e)}")
        return Response(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def team_stats(request, team_id):
    """Get statistics for a specific team"""
    try:
        team = get_object_or_404(Team, id=team_id)
        
        # Get team's matches
        matches = Match.objects.filter(team=team)
        
        if not matches.exists():
            return Response({'error': 'No matches found for this team'}, 
                          status=status.HTTP_404_NOT_FOUND)
        
        # Calculate statistics
        total_matches = matches.count()
        wins = matches.filter(result='W').count()
        draws = matches.filter(result='D').count()
        losses = matches.filter(result='L').count()
        
        win_rate = (wins / total_matches) * 100 if total_matches > 0 else 0
        
        # Recent form (last 5 matches)
        recent_matches = matches.order_by('-date')[:5]
        recent_results = [match.result for match in recent_matches]
        
        stats = {
            'team': TeamSerializer(team).data,
            'total_matches': total_matches,
            'wins': wins,
            'draws': draws,
            'losses': losses,
            'win_rate': round(win_rate, 2),
            'recent_form': recent_results,
            'recent_matches': MatchSerializer(recent_matches, many=True).data
        }
        
        return Response(stats, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error getting team stats: {str(e)}")
        return Response(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )