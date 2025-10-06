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
            
            ul_tp_column = '[Call Test] [Throughput] Application UL TP'
            serving_network_column = '[General] Serving Network'
            rsrp_column = '[NR5G] [RF] RSRP'
            latitude_column = '[General] [GPS] Latitude'
            longitude_column = '[General] [GPS] Longitude'

            required_columns = [ul_tp_column, serving_network_column, rsrp_column, latitude_column, longitude_column]
            if not all(col in df.columns for col in required_columns):
                missing_cols = [col for col in required_columns if col not in df.columns]
                print(f"Warning: Missing columns {missing_cols} in {filename}. Skipping.")
                continue

            device_type_match = re.search(r'(DUT\d+|REF\d+|PC\d+)', filename, re.IGNORECASE)
            device_type = device_type_match.group(0) if device_type_match else 'Unknown Device'

            no_service_indices = df[df[serving_network_column].astype(str).str.contains('No service', case=False, na=False)].index.tolist()

            found_data_point = False
            for no_service_idx in no_service_indices: # Iterate from top to bottom for 'No service'
                # Search upwards from the 'No service' index for the first UL TP value > 1
                for ul_tp_idx in range(no_service_idx, -1, -1):
                    ul_tp_value = df.loc[ul_tp_idx, ul_tp_column]
                    
                    if pd.notna(ul_tp_value) and pd.to_numeric(ul_tp_value, errors='coerce') > 1: # Changed condition to > 1
                        latitude = df.loc[ul_tp_idx, latitude_column]
                        longitude = df.loc[ul_tp_idx, longitude_column]
                        rsrp_value = df.loc[ul_tp_idx, rsrp_column]
                        
                        results.append({
                            'Device type': device_type,
                            'latitude': latitude,
                            'longitude': longitude,
                            'ul_tp_value': ul_tp_value,
                            'rsrp_value': rsrp_value
                        })
                        found_data_point = True
                        break # Found UL TP for this 'No service', move to next 'No service'
                if found_data_point:
                    break # Found a data point for at least one 'No service', stop processing this file
            
            if not found_data_point:
                pass # No relevant data point found for this file
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

            serving_network_column = '[General] Serving Network'
            if serving_network_column not in df.columns:
                print(f"Warning: '{serving_network_column}' not found in {filename_without_ext}. Cannot filter RSRP by 'No service'. Extracting full column.")
                no_service_idx = len(df) # Process entire column if 'No service' column is missing
            else:
                no_service_indices = df[df[serving_network_column].astype(str).str.contains('No service', case=False, na=False)].index
                if not no_service_indices.empty:
                    no_service_idx = no_service_indices[0] # First occurrence of 'No service'
                else:
                    no_service_idx = len(df) # No 'No service' found, process entire column

            # Extract RSRP data up to the first 'No service' entry (exclusive of the 'No service' row)
            rsrp_data = df.iloc[:no_service_idx, :][[rsrp_column_name]].rename(columns={rsrp_column_name: filename_without_ext})
            
            if all_rsrp_data.empty:
                all_rsrp_data = rsrp_data
            else:
                all_rsrp_data = pd.concat([all_rsrp_data, rsrp_data], axis=1)

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
    
    if not all_rsrp_data.empty:
        # Removed all_rsrp_data.dropna(inplace=True) to keep all rows,
        # filling missing values with NaN if columns have different lengths.
        # Removed all_rsrp_data.dropna(inplace=True) to keep all rows,
        # filling missing values with NaN if columns have different lengths.
        # Now, remove only rows where ALL values are NaN, as requested ("不要有空Row").
        all_rsrp_data.dropna(how='all', inplace=True)

        if all_rsrp_data.empty:
            print("No RSRP data extracted to save after removing empty rows.")
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
