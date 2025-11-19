"""
Example usage of the PL Data Scraper

This script demonstrates how to use the PLDataScraper class
in your own scripts or applications.
"""

from PL_Data_Scraping import PLDataScraper
import pandas as pd


def example_1_scrape_all():
    """Example 1: Scrape all available data"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Scrape All Data")
    print("="*60)
    
    scraper = PLDataScraper(season='2024-2025')
    results = scraper.scrape_all(output_dir='output')
    
    print("\n✅ Scraping complete!")
    for key, df in results.items():
        print(f"   {key}: {len(df)} rows")


def example_2_scrape_matches_only():
    """Example 2: Scrape only match results"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Scrape Match Results Only")
    print("="*60)
    
    scraper = PLDataScraper(season='2024-2025')
    
    # Scrape match results
    match_df = scraper.scrape_match_results()
    
    # Display summary
    print(f"\n📊 Scraped {len(match_df)} matches")
    
    if not match_df.empty:
        print("\nFirst 5 matches:")
        print(match_df.head())
        
        # Save to custom location
        scraper.save_to_csv(match_df, 'output/my_custom_matches.csv')


def example_3_process_data():
    """Example 3: Scrape and process data"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Scrape and Process Data")
    print("="*60)
    
    scraper = PLDataScraper(season='2024-2025')
    
    # Scrape shooting stats
    shooting_df = scraper.scrape_team_shooting_stats()
    
    if not shooting_df.empty:
        print(f"\n📊 Scraped shooting stats for {len(shooting_df)} teams")
        
        # Example processing: Find top scorers
        if 'Gls' in shooting_df.columns or 'Goals' in shooting_df.columns:
            goal_col = 'Gls' if 'Gls' in shooting_df.columns else 'Goals'
            
            # Sort by goals
            shooting_df[goal_col] = pd.to_numeric(shooting_df[goal_col], errors='coerce')
            top_teams = shooting_df.nlargest(5, goal_col)
            
            print("\n🎯 Top 5 Teams by Goals:")
            print(top_teams[['Squad' if 'Squad' in shooting_df.columns else shooting_df.columns[0], goal_col]])


def example_4_combine_data():
    """Example 4: Scrape multiple stats and combine"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Combine Multiple Data Sources")
    print("="*60)
    
    scraper = PLDataScraper(season='2024-2025')
    
    # Scrape both shooting and possession stats
    print("Scraping shooting stats...")
    shooting_df = scraper.scrape_team_shooting_stats()
    
    print("Scraping possession stats...")
    possession_df = scraper.scrape_team_possession_stats()
    
    # Combine if both successful
    if not shooting_df.empty and not possession_df.empty:
        print(f"\n📊 Combined data:")
        print(f"   - Shooting stats: {len(shooting_df)} teams")
        print(f"   - Possession stats: {len(possession_df)} teams")
        
        # You could merge these DataFrames here if they have a common column
        # combined_df = pd.merge(shooting_df, possession_df, on='Squad')


def main():
    """Run all examples"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║   Premier League Data Scraper - Example Usage             ║
    ╚═══════════════════════════════════════════════════════════╝
    
    This script demonstrates different ways to use the scraper.
    
    Choose an example to run:
    1. Scrape all data (takes ~3-4 minutes)
    2. Scrape match results only
    3. Scrape and process shooting stats
    4. Combine multiple data sources
    5. Run all examples
    
    """)
    
    choice = input("Enter your choice (1-5): ").strip()
    
    if choice == '1':
        example_1_scrape_all()
    elif choice == '2':
        example_2_scrape_matches_only()
    elif choice == '3':
        example_3_process_data()
    elif choice == '4':
        example_4_combine_data()
    elif choice == '5':
        example_1_scrape_all()
        example_2_scrape_matches_only()
        example_3_process_data()
        example_4_combine_data()
    else:
        print("❌ Invalid choice. Please run again and choose 1-5.")
        return
    
    print("\n" + "="*60)
    print("✅ Examples completed!")
    print("="*60)


if __name__ == "__main__":
    main()

