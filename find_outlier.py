import pandas as pd
import os
import sys
from datetime import datetime

# Ensure we can import from the current directory
sys.path.append(os.getcwd())

try:
    from shtetltleths.metrics import calculate_all_metrics
except ImportError:
    from metrics import calculate_all_metrics

from analyze_csvs import analyze_csv

df = analyze_csv('juleshenry_posts.csv')
if df is not None:
    outlier = df.loc[df['flesch_kincaid_grade'].idxmax()]
    print("\n--- Outlier Post ---")
    print(f"Title: {outlier['title']}")
    print(f"Date: {outlier['date']}")
    print(f"Flesch-Kincaid Grade: {outlier['flesch_kincaid_grade']}")
    print(f"Word Count: {outlier['word_count']}")
