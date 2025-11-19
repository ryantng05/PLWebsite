import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime
from predictions.models import Team, Match


class Command(BaseCommand):
    help = 'Import match data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        
        if not os.path.exists(csv_file):
            self.stdout.write(
                self.style.ERROR(f'CSV file not found: {csv_file}')
            )
            return

        try:
            # Read CSV data
            df = pd.read_csv(csv_file, index_col=0)
            self.stdout.write(f'Loaded {len(df)} records from CSV')
            
            # Create teams
            teams_created = 0
            teams_dict = {}
            
            for team_name in df['team'].unique():
                team, created = Team.objects.get_or_create(
                    name=team_name,
                    defaults={'short_name': team_name[:3].upper()}
                )
                teams_dict[team_name] = team
                if created:
                    teams_created += 1
            
            self.stdout.write(f'Created {teams_created} new teams')
            
            # Process matches
            matches_created = 0
            matches_updated = 0
            
            for index, row in df.iterrows():
                try:
                    # Parse date and time
                    date = pd.to_datetime(row['date']).date()
                    time_str = str(row['time']).replace(':', '')
                    if len(time_str) == 4:
                        time_obj = datetime.strptime(time_str, '%H%M').time()
                    else:
                        time_obj = datetime.strptime('15:00', '%H:%M').time()
                    
                    # Get team objects
                    team = teams_dict[row['team']]
                    opponent = teams_dict[row['opponent']]
                    
                    # Determine venue
                    venue = 'H' if row['venue'] == 'Home' else 'A'
                    
                    # Create or update match
                    match, created = Match.objects.get_or_create(
                        team=team,
                        opponent=opponent,
                        date=datetime.combine(date, time_obj),
                        defaults={
                            'time': time_obj,
                            'venue': venue,
                            'result': row['result'],
                            'goals_for': row['gf'],
                            'goals_against': row['ga'],
                            'shots': row['sh'],
                            'shots_on_target': row['sot'],
                            'distance': row['dist'],
                            'free_kicks': row['fk'],
                            'penalties': row['pk'],
                            'penalty_attempts': row['pkatt'],
                            'home_away': 1 if venue == 'H' else 0,
                            'opponent_code': self.get_team_code(row['opponent']),
                            'hour': time_obj.hour,
                            'day_of_week': date.weekday(),
                            'target': 2 if row['result'] == 'W' else (1 if row['result'] == 'D' else 0),
                        }
                    )
                    
                    if created:
                        matches_created += 1
                    else:
                        matches_updated += 1
                        
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'Error processing row {index}: {str(e)}')
                    )
                    continue
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Import completed: {matches_created} matches created, '
                    f'{matches_updated} matches updated'
                )
            )
            
            # Calculate rolling averages for all teams
            self.calculate_rolling_averages()
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error importing data: {str(e)}')
            )

    def get_team_code(self, team_name):
        """Convert team name to numeric code"""
        team_codes = {
            'Arsenal': 1, 'Aston Villa': 2, 'Brighton and Hove Albion': 3,
            'Brighton': 3, 'Chelsea': 4, 'Crystal Palace': 5, 'Everton': 6,
            'Fulham': 7, 'Leeds United': 8, 'Leicester City': 9, 'Liverpool': 10,
            'Manchester City': 11, 'Manchester United': 12, 'Newcastle United': 13,
            'Norwich City': 14, 'Southampton': 15, 'Tottenham Hotspur': 16,
            'Tottenham': 16, 'Watford': 17, 'West Ham United': 18, 'West Ham': 18,
            'Wolverhampton Wanderers': 19, 'Wolves': 19, 'Burnley': 20,
            'Sheffield United': 21, 'Brentford': 22, 'Leeds': 8
        }
        return team_codes.get(team_name, 0)

    def calculate_rolling_averages(self):
        """Calculate rolling averages for all teams"""
        self.stdout.write('Calculating rolling averages...')
        
        for team in Team.objects.all():
            matches = Match.objects.filter(team=team).order_by('date')
            
            if len(matches) < 3:
                continue
            
            # Calculate rolling averages for each match
            for i, match in enumerate(matches):
                if i < 2:  # Skip first 2 matches (need at least 3 for rolling average)
                    continue
                
                # Get last 3 matches (excluding current one)
                recent_matches = matches[i-3:i]
                
                if len(recent_matches) == 3:
                    # Calculate averages
                    match.gf_rolling = sum(m.goals_for for m in recent_matches) / 3
                    match.ga_rolling = sum(m.goals_against for m in recent_matches) / 3
                    match.sh_rolling = sum(m.shots for m in recent_matches) / 3
                    match.sot_rolling = sum(m.shots_on_target for m in recent_matches) / 3
                    match.dist_rolling = sum(m.distance for m in recent_matches) / 3
                    match.fk_rolling = sum(m.free_kicks for m in recent_matches) / 3
                    match.pk_rolling = sum(m.penalties for m in recent_matches) / 3
                    match.pkatt_rolling = sum(m.penalty_attempts for m in recent_matches) / 3
                    
                    match.save()
        
        self.stdout.write(self.style.SUCCESS('Rolling averages calculated successfully'))
