import pandas as pd
import numpy as np
import argparse
import os

def extract_device_type_from_audio_delay_filename(file_path):
    """
    Extracts device type (DUT1, DUT2, REF1, REF2) from audio delay filenames.
    Example: _20250925_153348_CH03_TMO_5G Auto_VoNR Disabled Audio Delay_DUT1 Mobile_5G Auto VoNR Disabled Audio Delay.csv
    """
    base_name = os.path.basename(file_path)
    # Look for patterns like _DUT1, _REF1, _DUT2, _REF2
    if "_DUT1" in base_name:
        return "DUT1"
    elif "_DUT2" in base_name:
        return "DUT2"
    elif "_REF1" in base_name:
        return "REF1"
    elif "_REF2" in base_name:
        return "REF2"
    return "Unknown Device"

def analyze_audio_delay(file_path):
    """
    Analyzes the 'Mouth to Ear Delay (Avg)' from a CSV file and calculates
    Mean, Standard Deviation, Min, and Max.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

    header = '[Call Test] [Voice Quality] [Per Rx Clip] Mouth to Ear Delay (Avg)'

    if header not in df.columns:
        print(f"Error: Column '{header}' not found in the CSV file.")
        print(f"Available columns: {df.columns.tolist()}")
        return None

    # Convert the column to numeric, coercing errors to NaN
    delay_data = pd.to_numeric(df[header], errors='coerce').dropna()

    if delay_data.empty:
        print(f"No valid numeric data found in column '{header}'.")
        return None

    mean_val = np.mean(delay_data) * 1000
    std_dev_val = np.std(delay_data) * 1000
    min_val = np.min(delay_data) * 1000
    max_val = np.max(delay_data) * 1000
    count_val = len(delay_data) # Calculate the number of occurrences
    device_type = extract_device_type_from_audio_delay_filename(file_path) # Extract device type

    return {
        "file_path": file_path,
        "device_type": device_type, # Add device type to the results
        "mean": mean_val,
        "std_dev": std_dev_val,
        "min": min_val,
        "max": max_val,
        "occurrences": count_val
    }

def process_directory(directory_path, subdir_filter=None):
    """
    Traverses a directory, finds CSV files, and collects audio delay metrics per file.
    If subdir_filter is provided, only processes subdirectories whose names contain the filter string.
    """
    all_file_stats = []
    
    for root, dirs, files in os.walk(directory_path):
        # If a filter is applied and we are not in the root directory, check the current subdirectory name
        if subdir_filter and root != directory_path:
            current_subdir_name = os.path.basename(root)
            if subdir_filter.lower() not in current_subdir_name.lower():
                # If the current subdirectory doesn't match the filter, skip its contents and subdirectories
                dirs[:] = [] # Clear dirs to prevent os.walk from descending further
                continue

        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                print(f"Processing audio delay file: {file_path}")
                file_stats = analyze_audio_delay(file_path)
                if file_stats is not None:
                    all_file_stats.append(file_stats)
    
    return all_file_stats

def main():
    parser = argparse.ArgumentParser(description="Analyze audio delay from a CSV file.")
    parser.add_argument("path", help="Path to the directory containing CSV files.")
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Directory not found at '{args.path}'")
        return

    print(f"Starting audio delay analysis for directory: {args.path}")
    all_file_stats = process_directory(args.path)

    print("\n--- Audio Delay Analysis Results ---")

    if not all_file_stats:
        print("No CSV files found or processed with relevant audio delay data.")
        return

    for stats in all_file_stats:
        file_name = os.path.basename(stats["file_path"])
        device_type = stats["device_type"] # Get device type
        print(f"\n--- File: {file_name} ({device_type}) ---")
        print(f"  Mean: {stats['mean_ms']:.2f} ms")
        print(f"  Standard Deviation: {stats['std_dev_ms']:.2f} ms")
        print(f"  Min: {stats['min_ms']:.2f} ms")
        print(f"  Max: {stats['max_ms']:.2f} ms")
        print(f"  Occurrences: {stats['occurrences']}")

if __name__ == "__main__":
    main()
