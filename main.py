import sys
import argparse
from shtetltleths.scraper import scrape_to_files, update_csv
from shtetltleths.analyzer import analyze_all_archives
from shtetltleths.cli import run_analysis

def main():
    parser = argparse.ArgumentParser(description="ShtetlTleths: Blog Scraper and Analyzer")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Update command
    update_parser = subparsers.add_parser("update", help="Scrape new posts and update CSV")
    update_parser.add_argument("--limit", type=int, help="Limit number of posts to scrape")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Calculate readability metrics for all posts")
    
    # Plot command
    plot_parser = subparsers.add_parser("plot", help="Plot readability metrics")

    args = parser.parse_args()

    if args.command == "update":
        print("Starting update...")
        new_posts = scrape_to_files(limit=args.limit)
        if new_posts:
            print(f"Scraped {len(new_posts)} new posts. Updating CSV...")
            update_csv("scottaaronson_blog_posts.csv", new_posts)
        else:
            print("No new posts found.")
    
    elif args.command == "analyze":
        print("Analyzing archives...")
        analyze_all_archives()
        print("Analysis complete.")
        
    elif args.command == "plot":
        run_analysis()
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
