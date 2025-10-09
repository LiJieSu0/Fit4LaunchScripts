import os
import pandas as pd
import argparse
import re
import numpy as np

def parse_mos_metrics(file_path):
    """
    Parses a CSV file to extract MOS values from the relevant column and calculate metrics.
    """
    try:
        # Read the CSV file, skipping initial rows if they are empty or not part of the header
        # The actual header is the first line that contains '[Call Test] [Voice Quality] [Per Rx Clip] MOS Value'
        
        # Find the header row index
        header_row_index = -1
        with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if '[Call Test] [Voice Quality] [Per Rx Clip] MOS Value' in line:
                    header_row_index = i
                    break
        
        if header_row_index == -1:
            print(f"Warning: Header '[Call Test] [Voice Quality] [Per Rx Clip] MOS Value' not found in {file_path}")
            return None

        df = pd.read_csv(file_path, skiprows=header_row_index, encoding='utf-8')

        # Identify the correct column for MOS Value
        mos_value_col = None
        for col in df.columns:
            if '[Call Test] [Voice Quality] [Per Rx Clip] MOS Value' in col:
                mos_value_col = col
                break
        
        if mos_value_col is None:
            print(f"Warning: Column '[Call Test] [Voice Quality] [Per Rx Clip] MOS Value' not found in {file_path}")
            return None

        # Extract MOS values, convert to numeric, and drop NaNs
        mos_values = pd.to_numeric(df[mos_value_col], errors='coerce').dropna()

        if mos_values.empty:
            print(f"Warning: No valid MOS values found in column '{mos_value_col}' in {file_path}")
            return None

        # Calculate the required metrics
        metrics = {
            'MOS Average': mos_values.mean(),
            'MOS Stdev': mos_values.std(),
            'Maximum MOS': mos_values.max(),
            'Counts': len(mos_values),
            '% MOS < 3.0': (mos_values < 3.0).sum() / len(mos_values) * 100,
            '% MOS < 2.0': (mos_values < 2.0).sum() / len(mos_values) * 100
        }
        
        # Handle cases where std might be NaN if there's only one value
        if pd.isna(metrics['MOS Stdev']):
            metrics['MOS Stdev'] = 0.0

        return metrics

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None

def analyze_wb_voice_quality(base_path):
    """
    Analyzes WB voice quality data from BASE and Mobile folders.
    """
    results = {}
    subfolders = ['Base', 'Mobile'] # Changed to 'Base' as per user's feedback path
    
    for subfolder in subfolders:
        subfolder_path = os.path.join(base_path, subfolder)
        if not os.path.isdir(subfolder_path):
            print(f"Warning: Subfolder '{subfolder_path}' not found. Skipping.")
            continue

        results[subfolder] = {}
        # Dynamically find all CSV files in the subfolder
        found_csv_files = [f for f in os.listdir(subfolder_path) if f.endswith('.csv')]
        
        if not found_csv_files:
            print(f"Warning: No CSV files found in '{subfolder_path}'. Skipping.")
            continue

        for csv_file_name in found_csv_files:
            file_path = os.path.join(subfolder_path, csv_file_name)
            
            print(f"Processing {file_path}...")
            metrics = parse_mos_metrics(file_path)
            if metrics:
                results[subfolder][csv_file_name.replace('.csv', '')] = metrics
    
    return results

def print_results(results):
    """
    Prints the aggregated results in a readable format.
    """
    if not results:
        print("No data to display.")
        return

    for subfolder, data in results.items():
        print(f"\n--- {subfolder} ---")
        if not data:
            print("No data found for this subfolder.")
            continue
        
        # Prepare data for a pandas DataFrame for better display
        df_data = {}
        for device, metrics in data.items():
            for metric_name, value in metrics.items():
                if metric_name not in df_data:
                    df_data[metric_name] = {}
                df_data[metric_name][device] = value
        
        df = pd.DataFrame(df_data).T # Transpose to have metrics as index and devices as columns
        print(df.to_string())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze WB voice quality from specified directory.")
    parser.add_argument("path", type=str, help="Path to the directory containing BASE and Mobile folders.")
    args = parser.parse_args()

    input_path = args.path
    if not os.path.isdir(input_path):
        print(f"Error: The provided path '{input_path}' is not a valid directory.")
    else:
        print(f"Starting analysis for path: {input_path}")
        analysis_results = analyze_wb_voice_quality(input_path)
        print_results(analysis_results)
