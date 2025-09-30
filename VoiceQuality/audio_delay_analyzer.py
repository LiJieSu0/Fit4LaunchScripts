import pandas as pd
import numpy as np
import argparse
import os

def analyze_audio_delay(file_path):
    """
    Analyzes the 'Mouth to Ear Delay (Avg)' from a CSV file and calculates
    Mean, Standard Deviation, Min, and Max.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    header = '[Call Test] [Voice Quality] [Per Rx Clip] Mouth to Ear Delay (Avg)'

    if header not in df.columns:
        print(f"Error: Column '{header}' not found in the CSV file.")
        print(f"Available columns: {df.columns.tolist()}")
        return

    # Convert the column to numeric, coercing errors to NaN
    delay_data = pd.to_numeric(df[header], errors='coerce').dropna()

    if delay_data.empty:
        print(f"No valid numeric data found in column '{header}'.")
        return

    mean_val = np.mean(delay_data) * 1000
    std_dev_val = np.std(delay_data) * 1000
    min_val = np.min(delay_data) * 1000
    max_val = np.max(delay_data) * 1000
    count_val = len(delay_data) # Calculate the number of occurrences

    print(f"Analysis for '{header}' in '{file_path}':")
    print(f"  Mean: {mean_val:.2f} ms")
    print(f"  Standard Deviation: {std_dev_val:.2f} ms")
    print(f"  Min: {min_val:.2f} ms")
    print(f"  Max: {max_val:.2f} ms")
    print(f"  Occurrences: {count_val}") # Print the number of occurrences

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze audio delay from a CSV file.")
    parser.add_argument("file_path", help="Path to the CSV file.")
    args = parser.parse_args()

    analyze_audio_delay(args.file_path)
