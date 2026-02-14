import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import re
from datetime import datetime

# Ensure we can import from the current directory
sys.path.append(os.getcwd())

try:
    from shtetltleths.metrics import calculate_all_metrics
except ImportError:
    from metrics import calculate_all_metrics

def parse_date(date_str):
    if not isinstance(date_str, str):
        return None
    
    # Fix Sept -> Sep
    date_str = date_str.replace('Sept', 'Sep')
    
    # Strip ordinal suffixes like 1st, 2nd, 3rd, 4th
    date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)
    
    # Try various formats
    formats = [
        "%d %B %Y %I:%M %p", # 13 February 2026 11:38 pm
        "%d %B %Y",          # 13 February 2026
        "%b %d, %Y",         # Jan 17, 2026
        "%B %d, %Y",         # January 17, 2026
        "%d %b %Y",          # 19 Jan 2026
        "%A, %B %d, %Y",     # Monday, October 31, 2005
        "%Y-%m-%dT%H:%M:%S.%f", # 2026-02-14T...
        "%Y-%m-%d",          # 2026-01-19
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    return None

def analyze_csv(file_path):
    print(f"Analyzing {file_path}...")
    try:
        df = pd.read_csv(file_path, on_bad_lines='skip')
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None
        
    # Standardize column names
    if 'post' not in df.columns:
        if 'summary' in df.columns:
            df = df.rename(columns={'summary': 'post'})
        else:
            print(f"Skipping {file_path}: No 'post' or 'summary' column found.")
            return None
    
    # Handle timestamp/date column
    date_col = 'timestamp' if 'timestamp' in df.columns else ('date' if 'date' in df.columns else None)
    if date_col:
        df['parsed_date'] = df[date_col].apply(parse_date)
    else:
        df['parsed_date'] = None

    # Drop empty posts
    df = df.dropna(subset=['post'])
    df = df[df['post'].astype(str).str.strip() != '']
    
    print(f"Found {len(df)} posts in {file_path}")
    
    results = []
    for i, row in df.iterrows():
        text = str(row['post'])
        if len(text.strip()) < 100:
            continue
            
        try:
            metrics = calculate_all_metrics(text)
        except Exception:
            continue
        
        fk = metrics.get('flesch_kincaid', {})
        ari = metrics.get('ari', {})
        gunning = metrics.get('gunning_fog', {})
        
        def to_float(d, key='score'):
            try:
                val = d.get(key)
                return float(val) if val is not None else None
            except (ValueError, TypeError):
                return None

        entry = {
            'title': row.get('title', 'Untitled'),
            'date': row.get('parsed_date'),
            'word_count': len(text.split()),
            'flesch_kincaid_grade': to_float(fk),
            'ari_grade': to_float(ari),
            'gunning_fog_grade': to_float(gunning)
        }
        
        words = text.split()
        unique_words = set(w.lower().strip('.,!?:;()[]"\'') for w in words if any(c.isalnum() for c in w))
        entry['lexical_diversity'] = len(unique_words) / len(words) if words else 0
        
        if entry['flesch_kincaid_grade'] is not None:
            results.append(entry)
            
    return pd.DataFrame(results)

def main():
    csv_files = [
        'scottaaronson_blog_posts.csv',
        'alexharri_posts.csv',
        'juleshenry_posts.csv',
        'simonwillison_all_blogs.csv'
    ]
    
    all_data = []
    for f in csv_files:
        if os.path.exists(f):
            df = analyze_csv(f)
            if df is not None and not df.empty:
                df['source'] = os.path.basename(f)
                all_data.append(df)
    
    if not all_data:
        print("No data found to analyze.")
        return
        
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Define metrics to plot over time
    time_metrics = ['flesch_kincaid_grade', 'ari_grade', 'gunning_fog_grade', 'lexical_diversity', 'word_count']
    
    # Final plot setup: 5 metrics over time
    fig, axes = plt.subplots(len(time_metrics), 1, figsize=(16, 6 * len(time_metrics)))
    if len(time_metrics) == 1:
        axes = [axes]
        
    sources = combined_df['source'].unique()
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f1c40f', '#9b59b6']
    
    time_df = combined_df.dropna(subset=['date']).copy()
    if time_df.empty:
        print("No valid dates found for time series analysis.")
        return

    time_df = time_df.sort_values('date')

    for idx, metric in enumerate(time_metrics):
        ax = axes[idx]
        for i, source in enumerate(sources):
            subset = time_df[time_df['source'] == source]
            if subset.empty:
                continue
            
            # Plot individual points
            ax.scatter(subset['date'], subset[metric], alpha=0.3, color=colors[i % len(colors)], label=f"{source} (points)")
            
            # Plot moving average
            window = 5 if len(subset) > 10 else 2
            subset_rolled = subset.set_index('date')[metric].rolling(window=window).mean()
            ax.plot(subset_rolled.index, subset_rolled.values, linewidth=2, color=colors[i % len(colors)], label=f"{source} (moving avg)")
            
        ax.set_title(f'{metric.replace("_", " ").title()} Over Time')
        ax.set_ylabel(metric.replace("_", " ").title())
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
    plt.tight_layout()
    plt.savefig('writing_stats_time.png')
    print("\nAnalysis complete. Results saved to writing_stats_time.png")
    
    # Print summary
    print("\nSummary Statistics:")
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    print(combined_df.groupby('source')[time_metrics].mean())

if __name__ == "__main__":
    main()
