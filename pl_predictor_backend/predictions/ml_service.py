import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from django.utils import timezone
from datetime import datetime, time
import logging

logger = logging.getLogger(__name__)


class PLPredictionService:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100, 
            min_samples_split=10, 
            random_state=1
        )
        self.predictors = ["home_away", "opponent_code", "hour", "day_of_week"]
        self.rolling_predictors = [
            "gf_rolling", "ga_rolling", "sh_rolling", "sot_rolling",
            "dist_rolling", "fk_rolling", "pk_rolling", "pkatt_rolling"
        ]
        self.is_trained = False
    
    def prepare_match_data(self, matches_queryset):
        """Convert Django QuerySet to pandas DataFrame for ML processing"""
        matches_data = []
        
        for match in matches_queryset:
            match_data = {
                'date': match.date,
                'team': match.team.name,
                'opponent': match.opponent.name,
                'venue': match.venue,
                'time': match.time,
                'result': match.result,
                'gf': match.goals_for,
                'ga': match.goals_against,
                'sh': match.shots,
                'sot': match.shots_on_target,
                'dist': match.distance,
                'fk': match.free_kicks,
                'pk': match.penalties,
                'pkatt': match.penalty_attempts,
                'home_away': match.home_away,
                'opponent_code': match.opponent_code,
                'hour': match.hour,
                'day_of_week': match.day_of_week,
                'target': match.target,
                'gf_rolling': match.gf_rolling,
                'ga_rolling': match.ga_rolling,
                'sh_rolling': match.sh_rolling,
                'sot_rolling': match.sot_rolling,
                'dist_rolling': match.dist_rolling,
                'fk_rolling': match.fk_rolling,
                'pk_rolling': match.pk_rolling,
                'pkatt_rolling': match.pkatt_rolling,
            }
            matches_data.append(match_data)
        
        return pd.DataFrame(matches_data)
    
    def calculate_rolling_averages(self, df, cols, new_cols, window=3):
        """Calculate rolling averages for team form"""
        df = df.sort_values("date")
        rolling_stats = df[cols].rolling(window, closed='left').mean()
        df[new_cols] = rolling_stats
        df = df.dropna(subset=new_cols)
        return df
    
    def train_model(self, matches_queryset):
        """Train the machine learning model on historical data"""
        try:
            # Prepare data
            df = self.prepare_match_data(matches_queryset)
            
            if df.empty:
                logger.warning("No data available for training")
                return False
            
            # Calculate rolling averages for all teams
            all_teams_data = []
            for team in df['team'].unique():
                team_data = df[df['team'] == team].copy()
                team_data = self.calculate_rolling_averages(
                    team_data, 
                    ['gf', 'ga', 'sh', 'sot', 'dist', 'fk', 'pk', 'pkatt'],
                    ['gf_rolling', 'ga_rolling', 'sh_rolling', 'sot_rolling',
                     'dist_rolling', 'fk_rolling', 'pk_rolling', 'pkatt_rolling']
                )
                all_teams_data.append(team_data)
            
            if all_teams_data:
                df = pd.concat(all_teams_data, ignore_index=True)
            
            # Split data for training and testing
            train_cutoff = '2022-01-01'
            train = df[df["date"] < train_cutoff]
            test = df[df["date"] >= train_cutoff]
            
            if train.empty or test.empty:
                logger.warning("Insufficient data for train/test split")
                return False
            
            # Prepare features
            all_predictors = self.predictors + self.rolling_predictors
            available_predictors = [p for p in all_predictors if p in train.columns]
            
            X_train = train[available_predictors]
            y_train = train["target"]
            X_test = test[available_predictors]
            y_test = test["target"]
            
            # Train model
            self.model.fit(X_train, y_train)
            self.is_trained = True
            
            # Evaluate model
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
            recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
            f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
            
            logger.info(f"Model trained successfully. Accuracy: {accuracy:.3f}, Precision: {precision:.3f}")
            
            return {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'test_matches_count': len(test)
            }
            
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            return False
    
    def predict_match(self, team, opponent, date, venue):
        """Predict the outcome of a specific match"""
        if not self.is_trained:
            logger.error("Model not trained yet")
            return None
        
        try:
            from predictions.models import Match
            
            # Prepare match features
            home_away = 1 if venue == 'H' else 0
            
            # Get team codes
            opponent_code = self._get_team_code(opponent)
            
            # Extract time features
            hour = 15  # Default to 3 PM if not specified
            day_of_week = date.weekday() if hasattr(date, 'weekday') else 0
            
            # Get recent team statistics for rolling averages
            recent_matches = Match.objects.filter(
                team=team
            ).order_by('-date')[:5]  # Last 5 matches
            
            if recent_matches.exists() and len(recent_matches) > 0:
                # Calculate averages from recent matches
                # Use goals_for/goals_against from the Match model
                rolling_values = [
                    sum(m.goals_for for m in recent_matches) / len(recent_matches),  # gf_rolling
                    sum(m.goals_against for m in recent_matches) / len(recent_matches),  # ga_rolling
                    sum(m.shots for m in recent_matches) / len(recent_matches),  # sh_rolling
                    sum(m.shots_on_target for m in recent_matches) / len(recent_matches),  # sot_rolling
                    sum(m.distance for m in recent_matches) / len(recent_matches),  # dist_rolling
                    sum(m.free_kicks for m in recent_matches) / len(recent_matches),  # fk_rolling
                    sum(m.penalties for m in recent_matches) / len(recent_matches),  # pk_rolling
                    sum(m.penalty_attempts for m in recent_matches) / len(recent_matches),  # pkatt_rolling
                ]
            else:
                # Use league averages or defaults if no recent matches
                rolling_values = [1.5, 1.5, 12.0, 4.0, 0.0, 0.0, 0.0, 0.0]
            
            # Create feature vector
            features = [home_away, opponent_code, hour, day_of_week] + rolling_values
            feature_names = self.predictors + self.rolling_predictors
            
            # Ensure we have the right number of features
            if len(features) != len(feature_names):
                # Pad with zeros if needed
                features = features[:len(feature_names)]
                while len(features) < len(feature_names):
                    features.append(0.0)
            
            X = np.array(features).reshape(1, -1)
            
            # Make prediction
            prediction_proba = self.model.predict_proba(X)[0]
            prediction_class = self.model.predict(X)[0]
            
            # Map prediction to result based on model's classes
            # Check how many classes the model has
            n_classes = len(prediction_proba)
            
            if n_classes == 3:
                # Three-class model: Loss, Draw, Win (our encoding: L=0, D=1, W=2)
                result_map = {0: 'L', 1: 'D', 2: 'W'}
                probabilities = {
                    'W': float(prediction_proba[2]),
                    'D': float(prediction_proba[1]),
                    'L': float(prediction_proba[0])
                }
            else:
                # Binary model: Loss, Win
                result_map = {0: 'L', 1: 'W'}
                probabilities = {
                    'W': float(prediction_proba[1] if len(prediction_proba) > 1 else 0.0),
                    'D': 0.0,
                    'L': float(prediction_proba[0] if len(prediction_proba) > 0 else 0.0)
                }
            
            predicted_result = result_map.get(prediction_class, 'D')
            
            # Get confidence (probability of the predicted class)
            confidence = float(prediction_proba.max())
            
            return {
                'predicted_result': predicted_result,
                'confidence': confidence,
                'probabilities': probabilities
            }
            
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}")
            return None
    
    def _get_team_code(self, team_name):
        """Convert team name to numeric code for ML model"""
        # This is a simple implementation - in production you'd want a proper mapping
        team_codes = {
            'Arsenal': 1, 'Aston Villa': 2, 'Brighton': 3, 'Chelsea': 4,
            'Crystal Palace': 5, 'Everton': 6, 'Fulham': 7, 'Leeds': 8,
            'Leicester': 9, 'Liverpool': 10, 'Manchester City': 11,
            'Manchester United': 12, 'Newcastle': 13, 'Norwich': 14,
            'Southampton': 15, 'Tottenham': 16, 'Watford': 17,
            'West Ham': 18, 'Wolves': 19, 'Burnley': 20, 'Sheffield United': 21
        }
        return team_codes.get(team_name, 0)
    
    def get_model_info(self):
        """Get information about the current model"""
        return {
            'is_trained': self.is_trained,
            'predictors': self.predictors,
            'rolling_predictors': self.rolling_predictors,
            'model_type': 'RandomForestClassifier'
        }
