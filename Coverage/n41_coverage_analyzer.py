import pandas as pd
import os
import glob
import json # Import json for outputting results

def analyze_n41_coverage(folder_path, device_type_filter=None):
    """
    Analyzes CSV files in a specified folder for n41 coverage data.
    It reads each CSV file, searches the '[Call Test] [Throughput] Application UL TP' column
    from bottom to top for the first value greater than 1, and records its
    corresponding latitude and longitude.

    Args:
        folder_path (str): The path to the folder containing CSV files.
        device_type_filter (str, optional): If provided, only process files
                                            containing this device type in their name (e.g., 'PC2', 'PC3').

    Returns:
        list: A list of dictionaries, where each dictionary contains the filename,
              latitude, and longitude for the first UL TP value > 1.
    """
    results = []
    csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

    if not csv_files:
        # print(f"No CSV files found in the specified folder: {folder_path}") # Suppress print for integration
        return results

    for file_path in csv_files:
        filename = os.path.basename(file_path)
        
        # Apply device type filter if specified
        if device_type_filter and device_type_filter.lower() not in filename.lower():
            continue

        try:
            df = pd.read_csv(file_path)
            

            # Define the target column and coordinate columns
            target_column = '[Call Test] [Throughput] Application UL TP'
            latitude_column = '[General] [GPS] Latitude'
            longitude_column = '[General] [GPS] Longitude'

            if target_column not in df.columns:
                print(f"Warning: '{target_column}' not found in {filename}. Skipping.")
                continue
            if latitude_column not in df.columns or longitude_column not in df.columns:
                print(f"Warning: '{latitude_column}' or '{longitude_column}' not found in {filename}. Skipping.")
                continue

            # Search from bottom to top
            found_value = False
            for index in range(len(df) - 1, -1, -1):
                ul_tp_value = df.loc[index, target_column]
                
                # Ensure the value is numeric and greater than 1
                if pd.notna(ul_tp_value) and pd.to_numeric(ul_tp_value, errors='coerce') > 1:
                    latitude = df.loc[index, latitude_column]
                    longitude = df.loc[index, longitude_column]
                    results.append({
                        'filename': filename,
                        'latitude': latitude,
                        'longitude': longitude,
                        'ul_tp_value': ul_tp_value
                    })
                    found_value = True
                    break
            
            if not found_value:
                # print(f"No value > 1 found in '{target_column}' for {filename}.") # Suppress print for integration
                pass

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
    
    return results
