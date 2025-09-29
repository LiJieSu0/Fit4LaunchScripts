import os
import pandas as pd
import argparse

def analyze_csv(file_path):
    """
    Analyzes a single CSV file for voice quality metrics.
    Extracts UL MOS, DL MOS, and calculates statistics.
    """
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None, None

    ul_mos_header = '[Call Test] [Voice Quality] [UL MOS] MOS'
    dl_mos_header = '[Call Test] [Voice Quality] [Per Rx Clip] MOS Value'

    ul_mos_scores = []
    dl_mos_scores = []

    if ul_mos_header in df.columns:
        ul_mos_scores = df[ul_mos_header].dropna().tolist()
    else:
        print(f"Warning: '{ul_mos_header}' not found in {file_path}")

    if dl_mos_header in df.columns:
        dl_mos_scores = df[dl_mos_header].dropna().tolist()
    else:
        print(f"Warning: '{dl_mos_header}' not found in {file_path}")

    ul_stats = calculate_statistics(ul_mos_scores)
    dl_stats = calculate_statistics(dl_mos_scores)

    return {
        "file_path": file_path,
        "ul_mos_stats": ul_stats,
        "dl_mos_stats": dl_stats
    }

def process_directory(directory_path):
    """
    Traverses a directory, finds CSV files, and collects voice quality metrics per file.
    """
    all_file_stats = []
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                file_stats = analyze_csv(file_path)
                if file_stats is not None:
                    all_file_stats.append(file_stats)
    
    return all_file_stats

def calculate_statistics(mos_scores):
    """
    Calculates average MOS and percentage of scores less than 2.
    """
    if not mos_scores:
        return {
            "count": 0,
            "mean": 0.0,
            "std_dev": 0.0,
            "max": 0.0,
            "min": 0.0,
            "percent_less_than_2": 0.0,
            "percent_less_than_3": 0.0
        }

    series = pd.Series(mos_scores)
    
    mean_mos = series.mean()
    std_dev_mos = series.std()
    max_mos = series.max()
    min_mos = series.min()
    
    count_less_than_2 = (series < 2).sum()
    percent_less_than_2 = (count_less_than_2 / len(mos_scores)) * 100

    count_less_than_3 = (series < 3).sum()
    percent_less_than_3 = (count_less_than_3 / len(mos_scores)) * 100
    
    return {
        "count": len(mos_scores),
        "mean": mean_mos,
        "std_dev": std_dev_mos,
        "max": max_mos,
        "min": min_mos,
        "percent_less_than_2": percent_less_than_2,
        "percent_less_than_3": percent_less_than_3
    }

def main():
    parser = argparse.ArgumentParser(description="Analyze voice quality from CSV files in a given directory.")
    parser.add_argument("path", help="The path to the directory containing CSV files.")
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Directory not found at '{args.path}'")
        return

    print(f"Starting analysis for directory: {args.path}")
    all_file_stats = process_directory(args.path)

    print("\n--- Analysis Results ---")

    if not all_file_stats:
        print("No CSV files found or processed with relevant data.")
        return

    for stats in all_file_stats:
        file_name = os.path.basename(stats["file_path"])
        print(f"\n--- File: {file_name} ---")

        # Uplink MOS statistics
        ul_stats = stats["ul_mos_stats"]
        print(f"  Uplink MOS (UL MOS):")
        print(f"    Count: {ul_stats['count']}")
        print(f"    Mean: {ul_stats['mean']:.2f}")
        print(f"    Standard Deviation: {ul_stats['std_dev']:.2f}")
        print(f"    Max: {ul_stats['max']:.2f}")
        print(f"    Min: {ul_stats['min']:.2f}")
        print(f"    Percentage of scores < 2: {ul_stats['percent_less_than_2']:.2f}%")
        print(f"    Percentage of scores < 3: {ul_stats['percent_less_than_3']:.2f}%")

        # Downlink MOS statistics
        dl_stats = stats["dl_mos_stats"]
        print(f"  Downlink MOS (Per Rx Clip):")
        print(f"    Count: {dl_stats['count']}")
        print(f"    Mean: {dl_stats['mean']:.2f}")
        print(f"    Standard Deviation: {dl_stats['std_dev']:.2f}")
        print(f"    Max: {dl_stats['max']:.2f}")
        print(f"    Min: {dl_stats['min']:.2f}")
        print(f"    Percentage of scores < 2: {dl_stats['percent_less_than_2']:.2f}%")
        print(f"    Percentage of scores < 3: {dl_stats['percent_less_than_3']:.2f}%")

if __name__ == "__main__":
    main()
