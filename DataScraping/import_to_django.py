"""
Utility script to import scraped data into Django database
Run this from the pl_predictor_backend directory:
    python ../DataScraping/import_to_django.py
"""

import os
import sys
import django
import pandas as pd
from datetime import datetime
from pathlib import Path

# Add the Django project to the path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / 'pl_predictor_backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pl_predictor_backend.settings')
django.setup()

from predictions.models import Team, Match


def import_match_results(csv_file):
    """Import match results from scraped CSV file"""
    print(f"\n📊 Importing match results from: {csv_file}")
    
    try:
        df = pd.read_csv(csv_file)
        print(f"Found {len(df)} matches in CSV file")
        
        imported_count = 0
        skipped_count = 0
        error_count = 0
        
        for idx, row in df.iterrows():
            try:
                # Skip if match doesn't have a score (not played yet)
                if pd.isna(row.get('Score', None)):
                    skipped_count += 1
                    continue
                
                # Parse the data (adjust based on actual CSV structure)
                date_str = row.get('Date', None)
                home_team_name = row.get('Home', None)
                away_team_name = row.get('Away', None)
                
                if not all([date_str, home_team_name, away_team_name]):
                    skipped_count += 1
                    continue
                
                # Parse date
                match_date = pd.to_datetime(date_str)
                
                # Get or create teams
                home_team, _ = Team.objects.get_or_create(
                    name=home_team_name,
                    defaults={'abbreviation': home_team_name[:3].upper()}
                )
                
                away_team, _ = Team.objects.get_or_create(
                    name=away_team_name,
                    defaults={'abbreviation': away_team_name[:3].upper()}
                )
                
                # Parse score (format: "2-1")
                score = str(row.get('Score', '0-0'))
                home_goals, away_goals = map(int, score.split('-'))
                
                # Determine result from home team's perspective
                if home_goals > away_goals:
                    result = 'W'
                elif home_goals < away_goals:
                    result = 'L'
                else:
                    result = 'D'
                
                # Create or update match (for home team)
                Match.objects.update_or_create(
                    team=home_team,
                    opponent=away_team,
                    date=match_date,
                    defaults={
                        'venue': 'H',
                        'result': result,
                        'goals_scored': home_goals,
                        'goals_conceded': away_goals,
                        'shots': row.get('Sh', 0) if not pd.isna(row.get('Sh', 0)) else 0,
                        'shots_on_target': row.get('SoT', 0) if not pd.isna(row.get('SoT', 0)) else 0,
                        'expected_goals': row.get('xG', 0.0) if not pd.isna(row.get('xG', 0.0)) else 0.0,
                    }
                )
                
                # Create the reverse match (for away team)
                away_result = 'W' if result == 'L' else ('L' if result == 'W' else 'D')
                Match.objects.update_or_create(
                    team=away_team,
                    opponent=home_team,
                    date=match_date,
                    defaults={
                        'venue': 'A',
                        'result': away_result,
                        'goals_scored': away_goals,
                        'goals_conceded': home_goals,
                        'shots': row.get('Sh_Away', 0) if not pd.isna(row.get('Sh_Away', 0)) else 0,
                        'shots_on_target': row.get('SoT_Away', 0) if not pd.isna(row.get('SoT_Away', 0)) else 0,
                        'expected_goals': row.get('xG_Away', 0.0) if not pd.isna(row.get('xG_Away', 0.0)) else 0.0,
                    }
                )
                
                imported_count += 1
                
                if (idx + 1) % 10 == 0:
                    print(f"  Processed {idx + 1}/{len(df)} matches...")
                
            except Exception as e:
                error_count += 1
                print(f"  Error processing row {idx}: {str(e)}")
                continue
        
        print(f"\n✅ Import complete!")
        print(f"   - Imported: {imported_count} matches")
        print(f"   - Skipped: {skipped_count} matches (not played yet)")
        print(f"   - Errors: {error_count} matches")
        
    except Exception as e:
        print(f"\n❌ Error importing file: {str(e)}")


def list_available_files():
    """List all scraped CSV files in the output directory"""
    output_dir = Path(__file__).resolve().parent / 'output'
    
    if not output_dir.exists():
        print("❌ Output directory does not exist. Run the scraper first!")
        return []
    
    csv_files = list(output_dir.glob('match_results_*.csv'))
    
    if not csv_files:
        print("❌ No match result files found. Run the scraper first!")
        return []
    
    # Sort by modification time (newest first)
    csv_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    print("\n📁 Available scraped files:")
    for idx, file in enumerate(csv_files, 1):
        mod_time = datetime.fromtimestamp(file.stat().st_mtime)
        print(f"   {idx}. {file.name} (scraped: {mod_time.strftime('%Y-%m-%d %H:%M')})")
    
    return csv_files


def main():
    """Main function"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║   Import Scraped Data to Django Database                  ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # List available files
    csv_files = list_available_files()
    
    if not csv_files:
        return
    
    # Use the most recent file by default
    if len(sys.argv) > 1:
        # File path provided as argument
        csv_file = sys.argv[1]
    else:
        # Use the most recent file
        csv_file = csv_files[0]
        print(f"\n📄 Using most recent file: {csv_file.name}")
        response = input("   Continue? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return
    
    # Import the data
    import_match_results(csv_file)
    
    # Show statistics
    print(f"\n📈 Database Statistics:")
    print(f"   - Total teams: {Team.objects.count()}")
    print(f"   - Total matches: {Match.objects.count()}")


if __name__ == "__main__":
    main()

