import json
import numpy as np
import calendar
import matplotlib.pyplot as plt
from .metrics import MetricsTracker

def load_stats(filename="shtetloptimized_stats.json"):
    """Loads stats from the generated JSON file."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {filename}: {e}")
        return []

def plot_metrics(tracker, metric_names):
    """Plots the historical metrics using matplotlib."""
    if not tracker.history:
        print("No data to plot.")
        return

    num_points = len(next(iter(tracker.history.values())))
    months_idx = np.arange(num_points)
    
    month_labels = []
    year, month = 2005, 10
    for _ in range(num_points):
        month_labels.append(f"{calendar.month_abbr[month]} {year}")
        month += 1
        if month > 12:
            month = 1
            year += 1

    plt.figure(figsize=(15, 10))
    ncols = 3
    nrows = (len(metric_names) + ncols - 1) // ncols

    for idx, metric in enumerate(metric_names):
        if metric not in tracker.history or not tracker.history[metric]:
            continue
            
        ax = plt.subplot(nrows, ncols, idx + 1)
        ax.plot(months_idx, tracker.history[metric], label="Monthly Score", alpha=0.7)
        
        avg = tracker.averages[metric]
        ax.axhline(y=avg, color="red", linestyle=":", linewidth=1.5, label=f"Avg: {avg:.2f}")
        
        ax.set_title(f"{metric.replace('_', ' ').title()}")
        ax.set_xlabel("Month")
        ax.set_ylabel("Score")
        
        tick_spacing = max(1, num_points // 10)
        ax.set_xticks(months_idx[::tick_spacing])
        ax.set_xticklabels([month_labels[i] for i in range(0, num_points, tick_spacing)], 
                           rotation=45, fontsize=8)
        ax.legend(fontsize='small')

    plt.tight_layout()
    output_plot = "shtetl_metrics_plot.png"
    plt.savefig(output_plot)
    print(f"Plot saved to {output_plot}")
    plt.show()

def run_analysis():
    metric_names = [
        "flesch_kincaid", "flesch", "gunning_fog", "coleman_liau", 
        "dale_chall", "ari", "linsear_write", "smog", "spache"
    ]
    
    tracker = MetricsTracker()
    tracker.initialize_metrics(metric_names)
    
    data = load_stats()
    if not data:
        print("No data found. Please run analyzer first.")
        return

    for entry in data:
        month_metrics = {m: [] for m in metric_names}
        for post in entry.get("stat_array", []):
            for metric in metric_names:
                score = post.get(metric, {}).get("score")
                if score is not None:
                    month_metrics[metric].append(score)
        
        for metric in metric_names:
            if month_metrics[metric]:
                monthly_avg = sum(month_metrics[metric]) / len(month_metrics[metric])
                tracker.add_score(metric, monthly_avg)
            else:
                tracker.add_score(metric, 0.0)

    print("Metrics Analysis Complete.")
    for metric in metric_names:
        print(f"{metric:15}: Average Score = {tracker.averages[metric]:.2f}")
        
    plot_metrics(tracker, metric_names)
