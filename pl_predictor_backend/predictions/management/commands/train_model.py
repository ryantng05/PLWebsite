"""
Management command to train the ML prediction model
"""
from django.core.management.base import BaseCommand
from predictions.models import Match
from predictions.views import ml_service


class Command(BaseCommand):
    help = 'Train the machine learning prediction model with match data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting model training...'))
        
        # Get all matches
        matches = Match.objects.all()
        match_count = matches.count()
        
        if match_count == 0:
            self.stdout.write(self.style.ERROR('No match data available. Please import data first.'))
            return
        
        self.stdout.write(f'Found {match_count} matches in database')
        
        # Train the model
        success = ml_service.train_model(matches)
        
        if success:
            self.stdout.write(self.style.SUCCESS(f'✅ Model trained successfully!'))
            
            # Check if performance_metrics exists and display them
            if hasattr(ml_service, 'performance_metrics') and ml_service.performance_metrics:
                self.stdout.write(f'   Model accuracy: {ml_service.performance_metrics.get("accuracy", 0):.2%}')
                self.stdout.write(f'   Precision: {ml_service.performance_metrics.get("precision", 0):.2%}')
                self.stdout.write(f'   Recall: {ml_service.performance_metrics.get("recall", 0):.2%}')
                self.stdout.write(f'   F1 Score: {ml_service.performance_metrics.get("f1_score", 0):.2%}')
            else:
                self.stdout.write('   (Performance metrics will be available after model evaluation)')
        else:
            self.stdout.write(self.style.ERROR('❌ Model training failed. Check logs for details.'))

