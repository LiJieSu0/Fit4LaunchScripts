import pandas as pd
import argparse
import os

def find_coordinates(df, start_index, column_lat, column_lon):
    """
    Searches upwards from start_index for the first valid latitude and longitude.
    """
    for i in range(start_index, -1, -1):
        lat = df.loc[i, column_lat]
        lon = df.loc[i, column_lon]
        if pd.notna(lat) and pd.notna(lon):
            return lat, lon
    return None, None

def analyze_csv(file_path):
    """
    Analyzes a single CSV file to extract the four required coordinate pairs.
    """
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

    # Define column names
    col_event_voice_call = '[Event] Voice Call Event'
    col_call_result = '[Tool] Voice - Call Result : Drop'
    col_mos_value = '[Call Test] [Voice Quality] [Per Rx Clip] MOS Value'
    col_dl_tp = '[Call Test] [Throughput] Application DL TP'
    col_ul_tp = '[Call Test] [Throughput] Application UL TP'
    col_latitude = '[General] [GPS] Latitude'
    col_longitude = '[General] [GPS] Longitude'

    coords = {
        "mos_before_drop": (None, None),
        "call_drop": (None, None),
        "first_dl_tp_gt_1": (None, None),
        "first_ul_tp_gt_1": (None, None),
    }

    # Coordinate 1: Last valid MOS recorded before call dropped
    drop_events = df[df[col_event_voice_call] == col_call_result]
    if not drop_events.empty:
        drop_index = drop_events.index[0] # Assuming the first drop event is relevant
        
        # Search upwards for MOS value
        mos_index = -1
        for i in range(drop_index, -1, -1):
            mos_val = df.loc[i, col_mos_value]
            if pd.notna(mos_val) and pd.to_numeric(mos_val, errors='coerce') is not None:
                mos_index = i
                break
        
        if mos_index != -1:
            coords["mos_before_drop"] = find_coordinates(df, mos_index, col_latitude, col_longitude)
        else:
            # If no MOS value found, find the first valid coordinate upwards from drop_index
            coords["mos_before_drop"] = find_coordinates(df, drop_index, col_latitude, col_longitude)

    # Coordinate 2: Drop event coordinates
    if not drop_events.empty:
        drop_index = drop_events.index[0]
        lat_drop = df.loc[drop_index, col_latitude]
        lon_drop = df.loc[drop_index, col_longitude]
        if pd.notna(lat_drop) and pd.notna(lon_drop):
            coords["call_drop"] = (lat_drop, lon_drop)
        else:
            # If current row has no coordinates, search upwards
            coords["call_drop"] = find_coordinates(df, drop_index, col_latitude, col_longitude)

    # Coordinate 3: First DL TP > 1 from bottom
    for i in range(len(df) - 1, -1, -1):
        dl_tp_val = df.loc[i, col_dl_tp]
        if pd.notna(dl_tp_val) and pd.to_numeric(dl_tp_val, errors='coerce') > 1:
            coords["first_dl_tp_gt_1"] = find_coordinates(df, i, col_latitude, col_longitude)
            break

    # Coordinate 4: First UL TP > 1 from bottom
    for i in range(len(df) - 1, -1, -1):
        ul_tp_val = df.loc[i, col_ul_tp]
        if pd.notna(ul_tp_val) and pd.to_numeric(ul_tp_val, errors='coerce') > 1:
            coords["first_ul_tp_gt_1"] = find_coordinates(df, i, col_latitude, col_longitude)
            break

    return coords

def main():
    parser = argparse.ArgumentParser(description="Analyze CSV files for coverage performance coordinates.")
    parser.add_argument("input_dir", help="Path to the directory containing DUT and REF CSV files.")
    args = parser.parse_args()

    input_directory = args.input_dir

    if not os.path.isdir(input_directory):
        print(f"Error: Directory not found at {input_directory}")
        return

    print(f"Analyzing CSV files in: {input_directory}")

    for root, _, files in os.walk(input_directory):
        for file_name in files:
            if file_name.endswith(".csv"):
                file_path = os.path.join(root, file_name)
                print(f"\n--- Analyzing {file_name} ---")
                results = analyze_csv(file_path)
                if results:
                    for key, (lat, lon) in results.items():
                        print(f"{key.replace('_', ' ').title()}: Latitude={lat}, Longitude={lon}")
                else:
                    print("No results found or error during analysis.")

if __name__ == "__main__":
    main()
