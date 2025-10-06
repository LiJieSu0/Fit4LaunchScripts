import pandas as pd
import os
import glob
import json
import re

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
        return results

    for file_path in csv_files:
        filename = os.path.basename(file_path)
        
        if device_type_filter and device_type_filter.lower() not in filename.lower():
            continue

        try:
            df = pd.read_csv(file_path)
            
            target_column = '[Call Test] [Throughput] Application UL TP'
            latitude_column = '[General] [GPS] Latitude'
            longitude_column = '[General] [GPS] Longitude'

            if target_column not in df.columns:
                print(f"Warning: '{target_column}' not found in {filename}. Skipping.")
                continue
            if latitude_column not in df.columns or longitude_column not in df.columns:
                print(f"Warning: '{latitude_column}' or '{longitude_column}' not found in {filename}. Skipping.")
                continue

            # Extract device type from filename (e.g., "DUT1", "REF1", "PC2", "PC3")
            device_type_match = re.search(r'(DUT\d+|REF\d+|PC\d+)', filename, re.IGNORECASE)
            device_type = device_type_match.group(0) if device_type_match else 'Unknown Device'

            found_value = False
            for index in range(len(df) - 1, -1, -1):
                ul_tp_value = df.loc[index, target_column]
                
                if pd.notna(ul_tp_value) and pd.to_numeric(ul_tp_value, errors='coerce') > 1:
                    latitude = df.loc[index, latitude_column]
                    longitude = df.loc[index, longitude_column]
                    results.append({
                        'Device type': device_type, # Changed from 'filename' to 'Device type'
                        'latitude': latitude,
                        'longitude': longitude,
                        'ul_tp_value': ul_tp_value
                    })
                    found_value = True
                    break
            
            if not found_value:
                pass

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
    
    return results

def extract_rsrp_to_csv(folder_path, output_folder='.', device_type_filters=None):
    """
    Extracts the '[NR5G] [RF] RSRP' column from all CSV files in a specified folder,
    uses the filename as the new header, and saves all extracted columns to a new CSV file.

    Args:
        folder_path (str): The path to the folder containing CSV files.
        output_folder (str): The folder where the output CSV will be saved.
        device_type_filters (list, optional): A list of device types (strings) to filter by.
                                              Only process files containing any of these device types in their name.
    """
    all_rsrp_data = pd.DataFrame()
    csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

    if not csv_files:
        print(f"No CSV files found in the specified folder: {folder_path}")
        return

    for file_path in csv_files:
        filename = os.path.basename(file_path)

        # Apply device type filter if specified
        if device_type_filters:
            matched_filter = False
            for dt_filter in device_type_filters:
                if dt_filter.lower() in filename.lower():
                    matched_filter = True
                    break
            if not matched_filter:
                continue

        try:
            df = pd.read_csv(file_path)
            filename_without_ext = os.path.splitext(filename)[0]
            rsrp_column_name = '[NR5G] [RF] RSRP'

            if rsrp_column_name not in df.columns:
                print(f"Warning: '{rsrp_column_name}' not found in {filename_without_ext}. Skipping.")
                continue

            rsrp_data = df[[rsrp_column_name]].rename(columns={rsrp_column_name: filename_without_ext})
            
            if all_rsrp_data.empty:
                all_rsrp_data = rsrp_data
            else:
                all_rsrp_data = pd.concat([all_rsrp_data, rsrp_data], axis=1)

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
    
    if not all_rsrp_data.empty:
        all_rsrp_data.dropna(inplace=True)

        if all_rsrp_data.empty:
            print("No RSRP data remaining after removing empty rows.")
            return

        os.makedirs(output_folder, exist_ok=True)
        
        # Construct filename based on folder and combined device types
        device_types_str = "_".join(device_type_filters) if device_type_filters else "All"
        output_filename = os.path.basename(os.path.normpath(folder_path)) + f"_{device_types_str}_RSRP_Analysis.csv"
        output_path = os.path.join(output_folder, output_filename)
        
        all_rsrp_data.to_csv(output_path, index=False)
        print(f"\nSuccessfully extracted RSRP data to: {output_path}")
    else:
        print("No RSRP data extracted to save.")
