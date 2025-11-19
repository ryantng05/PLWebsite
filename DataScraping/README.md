# Premier League Data Scraping Module

This module scrapes Premier League statistics from [FBref.com](https://fbref.com) for use in the match prediction system.

## Features

- ✅ **Team Statistics**: Player-level stats for all Premier League teams
- ✅ **Match Results**: Complete fixture list with scores
- ✅ **Shooting Statistics**: Goals, shots, xG, and shooting accuracy
- ✅ **Possession Statistics**: Passing, touches, carries, and possession metrics
- ✅ **Respectful Scraping**: Built-in delays to avoid server overload
- ✅ **Error Handling**: Robust error handling and logging
- ✅ **Timestamped Output**: All files are timestamped for version control

## Installation

### 1. Install Dependencies

```bash
cd DataScraping
pip install -r requirements.txt
```

### 2. Run the Scraper

```bash
python PL_Data_Scraping.py
```

## Output

The scraper creates timestamped CSV files in the `DataScraping/output/` directory:

- `team_stats_YYYYMMDD_HHMMSS.csv` - Player statistics for all teams
- `match_results_YYYYMMDD_HHMMSS.csv` - All match results and fixtures
- `shooting_stats_YYYYMMDD_HHMMSS.csv` - Team shooting statistics
- `possession_stats_YYYYMMDD_HHMMSS.csv` - Team possession statistics

## Usage as a Module

You can also import and use the scraper programmatically:

```python
from PL_Data_Scraping import PLDataScraper

# Initialize scraper
scraper = PLDataScraper(season='2024-2025')

# Scrape specific data
team_stats = scraper.scrape_team_stats()
match_results = scraper.scrape_match_results()
shooting_stats = scraper.scrape_team_shooting_stats()
possession_stats = scraper.scrape_team_possession_stats()

# Save to custom location
scraper.save_to_csv(team_stats, 'my_custom_file.csv')

# Or scrape everything at once
all_data = scraper.scrape_all(output_dir='my_output_folder')
```

## Scraping Process

1. **Team Statistics** (5 seconds delay between teams)
   - Scrapes all team pages
   - Extracts player-level performance data
   - Approximately 20 teams × 5 seconds = ~2 minutes

2. **Match Results** (one request)
   - Scrapes the fixtures/results table
   - Contains all matches for the season

3. **Shooting Statistics** (one request)
   - Team-level shooting metrics
   - Goals, shots, expected goals (xG)

4. **Possession Statistics** (one request)
   - Team-level possession metrics
   - Passing accuracy, touches, carries

**Total Time**: Approximately 3-4 minutes for a full scrape

## Important Notes

### Respectful Scraping
- ⏱️ **5-second delay** between each team scrape
- ⏱️ **10-second delay** between different data types
- 🤝 Follows best practices to avoid overwhelming the server

### Data Freshness
- Run the scraper **weekly** or **after each matchday** for updated stats
- Match results are updated as games are played
- FBref typically updates within 24 hours of a match

### Rate Limiting
If you encounter connection errors or blocks:
1. Increase the delay times in the code
2. Wait 30-60 minutes before trying again
3. Ensure you have a stable internet connection

## Integrating with the Django Backend

To import the scraped data into your Django database:

### Option 1: Update the Django Import Command

Modify `pl_predictor_backend/predictions/management/commands/import_csv_data.py` to use the newly scraped files.

### Option 2: Create a New Management Command

```bash
cd pl_predictor_backend
python manage.py import_scraped_data --file ../DataScraping/output/match_results_TIMESTAMP.csv
```

### Option 3: Manual Processing

Process the CSV files with pandas and create a custom import script:

```python
import pandas as pd
from predictions.models import Team, Match

# Read the match results
df = pd.read_csv('DataScraping/output/match_results_TIMESTAMP.csv')

# Process and import into Django models
# ... your custom logic here ...
```

## Troubleshooting

### Module Not Found Errors
```bash
pip install beautifulsoup4 pandas requests lxml
```

### No Data Scraped
- Check your internet connection
- Verify FBref.com is accessible
- Check if the website structure has changed

### Permission Errors
- Ensure the `DataScraping/output/` directory is writable
- Run with appropriate permissions

## Data Schema

### Team Statistics
- Player names and positions
- Games played, starts, minutes
- Goals, assists, xG, xAG
- Team identifier

### Match Results
- Date, Time, Venue
- Home team, Away team
- Score (if played)
- xG for both teams

### Shooting Statistics
- Goals, Shots, Shots on Target
- Expected Goals (xG)
- Shooting accuracy percentages

### Possession Statistics
- Touches in different areas
- Pass completion rates
- Progressive passes and carries

## Future Enhancements

- [ ] Add defensive statistics scraping
- [ ] Scrape historical seasons (multiple years)
- [ ] Add player-specific detailed stats
- [ ] Implement incremental updates (only new matches)
- [ ] Add data validation and cleaning
- [ ] Create automated scheduling (cron jobs)
- [ ] Add API endpoint to trigger scraping from Django

## Legal & Ethical Considerations

⚠️ **Important**: This scraper is for **educational purposes only**. Please:
- Review FBref's Terms of Service
- Do not scrape excessively or abuse their servers
- Consider using official APIs when available
- Give credit to FBref for the data source

## License

This module is part of the Premier League Predictor project and follows the same MIT license.

## Credits

- Data source: [FBref.com](https://fbref.com)
- Powered by BeautifulSoup and pandas

