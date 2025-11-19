"""
Premier League Data Scraping Module
Scrapes team and match statistics from FBref for the Premier League
"""

from bs4 import BeautifulSoup
import pandas as pd
import requests 
import time
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PLDataScraper:
    """Scraper for Premier League data from FBref"""
    
    def __init__(self, season='2024-2025'):
        self.base_url = 'https://fbref.com'
        self.season = season
        self.all_teams = []
        self.match_data = []
        
    def scrape_team_stats(self):
        """Scrape all team statistics for the current season"""
        try:
            logger.info("Starting team statistics scraping...")
            
            # Get the main Premier League page
            url = f'{self.base_url}/en/comps/9/Premier-League-Stats'
            html = requests.get(url).text
            soup = BeautifulSoup(html, 'lxml')
            
            # Find all teams
            table = soup.find_all('table', class_='stats_table')[0]
            links = table.find_all('a')
            links = [l.get("href") for l in links]
            links = [l for l in links if '/squads/' in l]
            
            team_urls = [f"{self.base_url}{l}" for l in links]
            
            logger.info(f"Found {len(team_urls)} teams to scrape")
            
            # Scrape each team
            for idx, team_url in enumerate(team_urls, 1):
                try:
                    team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
                    logger.info(f"Scraping team {idx}/{len(team_urls)}: {team_name}")
                    
                    data = requests.get(team_url).text
                    soup = BeautifulSoup(data, 'lxml')
                    stats = soup.find_all('table', class_="stats_table")[0]
                    
                    # Convert to DataFrame
                    team_data = pd.read_html(str(stats))[0]
                    
                    # Handle multi-level columns
                    if isinstance(team_data.columns, pd.MultiIndex):
                        team_data.columns = team_data.columns.droplevel()
                    
                    team_data["Team"] = team_name
                    team_data["Scraped_Date"] = datetime.now().strftime('%Y-%m-%d')
                    
                    self.all_teams.append(team_data)
                    
                    # Be respectful to the server
                    time.sleep(5)
                    
                except Exception as e:
                    logger.error(f"Error scraping team {team_name}: {str(e)}")
                    continue
            
            # Combine all team data
            if self.all_teams:
                stat_df = pd.concat(self.all_teams, ignore_index=True)
                logger.info(f"Successfully scraped {len(self.all_teams)} teams")
                return stat_df
            else:
                logger.warning("No team data was scraped")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error in team stats scraping: {str(e)}")
            return pd.DataFrame()
    
    def scrape_match_results(self):
        """Scrape match results for the season"""
        try:
            logger.info("Starting match results scraping...")
            
            # Get the fixtures/results page
            url = f'{self.base_url}/en/comps/9/schedule/Premier-League-Scores-and-Fixtures'
            html = requests.get(url).text
            soup = BeautifulSoup(html, 'lxml')
            
            # Find the fixtures table
            table = soup.find('table', class_='stats_table')
            
            if table:
                # Convert to DataFrame
                match_df = pd.read_html(str(table))[0]
                match_df["Scraped_Date"] = datetime.now().strftime('%Y-%m-%d')
                
                logger.info(f"Successfully scraped {len(match_df)} matches")
                return match_df
            else:
                logger.warning("No match data found")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error in match scraping: {str(e)}")
            return pd.DataFrame()
    
    def scrape_team_shooting_stats(self):
        """Scrape shooting statistics for all teams"""
        try:
            logger.info("Starting shooting statistics scraping...")
            
            url = f'{self.base_url}/en/comps/9/shooting/Premier-League-Stats'
            html = requests.get(url).text
            soup = BeautifulSoup(html, 'lxml')
            
            table = soup.find('table', class_='stats_table')
            
            if table:
                shooting_df = pd.read_html(str(table))[0]
                
                # Handle multi-level columns
                if isinstance(shooting_df.columns, pd.MultiIndex):
                    shooting_df.columns = ['_'.join(col).strip() for col in shooting_df.columns.values]
                
                shooting_df["Scraped_Date"] = datetime.now().strftime('%Y-%m-%d')
                
                logger.info(f"Successfully scraped shooting stats for {len(shooting_df)} teams")
                return shooting_df
            else:
                logger.warning("No shooting data found")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error in shooting stats scraping: {str(e)}")
            return pd.DataFrame()
    
    def scrape_team_possession_stats(self):
        """Scrape possession statistics for all teams"""
        try:
            logger.info("Starting possession statistics scraping...")
            
            url = f'{self.base_url}/en/comps/9/possession/Premier-League-Stats'
            html = requests.get(url).text
            soup = BeautifulSoup(html, 'lxml')
            
            table = soup.find('table', class_='stats_table')
            
            if table:
                possession_df = pd.read_html(str(table))[0]
                
                # Handle multi-level columns
                if isinstance(possession_df.columns, pd.MultiIndex):
                    possession_df.columns = ['_'.join(col).strip() for col in possession_df.columns.values]
                
                possession_df["Scraped_Date"] = datetime.now().strftime('%Y-%m-%d')
                
                logger.info(f"Successfully scraped possession stats for {len(possession_df)} teams")
                return possession_df
            else:
                logger.warning("No possession data found")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error in possession stats scraping: {str(e)}")
            return pd.DataFrame()
    
    def save_to_csv(self, df, filename):
        """Save DataFrame to CSV file"""
        try:
            df.to_csv(filename, index=False)
            logger.info(f"Data saved to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving to CSV: {str(e)}")
            return False
    
    def scrape_all(self, output_dir='DataScraping/output'):
        """Scrape all available data and save to CSV files"""
        import os
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Scrape team stats
        logger.info("=" * 60)
        logger.info("SCRAPING TEAM STATISTICS")
        logger.info("=" * 60)
        team_stats = self.scrape_team_stats()
        if not team_stats.empty:
            self.save_to_csv(team_stats, f'{output_dir}/team_stats_{timestamp}.csv')
        
        time.sleep(10)  # Be extra respectful between different scraping tasks
        
        # Scrape match results
        logger.info("=" * 60)
        logger.info("SCRAPING MATCH RESULTS")
        logger.info("=" * 60)
        match_results = self.scrape_match_results()
        if not match_results.empty:
            self.save_to_csv(match_results, f'{output_dir}/match_results_{timestamp}.csv')
        
        time.sleep(10)
        
        # Scrape shooting stats
        logger.info("=" * 60)
        logger.info("SCRAPING SHOOTING STATISTICS")
        logger.info("=" * 60)
        shooting_stats = self.scrape_team_shooting_stats()
        if not shooting_stats.empty:
            self.save_to_csv(shooting_stats, f'{output_dir}/shooting_stats_{timestamp}.csv')
        
        time.sleep(10)
        
        # Scrape possession stats
        logger.info("=" * 60)
        logger.info("SCRAPING POSSESSION STATISTICS")
        logger.info("=" * 60)
        possession_stats = self.scrape_team_possession_stats()
        if not possession_stats.empty:
            self.save_to_csv(possession_stats, f'{output_dir}/possession_stats_{timestamp}.csv')
        
        logger.info("=" * 60)
        logger.info("SCRAPING COMPLETE!")
        logger.info("=" * 60)
        
        return {
            'team_stats': team_stats,
            'match_results': match_results,
            'shooting_stats': shooting_stats,
            'possession_stats': possession_stats
        }


def main():
    """Main function to run the scraper"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║   Premier League Data Scraper                              ║
    ║   Scraping data from FBref.com                             ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Initialize scraper
    scraper = PLDataScraper(season='2024-2025')
    
    # Scrape all data
    results = scraper.scrape_all()
    
    print("\n✅ Scraping completed successfully!")
    print(f"   - Team stats: {len(results['team_stats'])} rows")
    print(f"   - Match results: {len(results['match_results'])} rows")
    print(f"   - Shooting stats: {len(results['shooting_stats'])} rows")
    print(f"   - Possession stats: {len(results['possession_stats'])} rows")
    print("\n📁 Check the DataScraping/output/ folder for CSV files")


if __name__ == "__main__":
    main()

