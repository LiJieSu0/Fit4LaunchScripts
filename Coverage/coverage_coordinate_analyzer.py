import csv
import argparse
import os
import json
import math

BASE_STATION_COORDS = {"latitude": 47.128234, "longitude": -122.356792}

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in kilometers

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

def analyze_coverage_coordinates(file_path):
    """
    Analyzes a CSV file to find the coordinates corresponding to specific events,
    searching from the bottom up. Returns a dictionary of results.
    """
    results = {
        "last_mos_value_coords": None,
        "voice_call_drop_coords": None,
        "first_dl_tp_gt_1_coords": None,
        "first_ul_tp_gt_1_coords": None
    }

    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # Read the header row

            # Find column indices
            try:
                dl_tp_col_idx = header.index('[Call Test] [Throughput] Application DL TP')
                ul_tp_col_idx = header.index('[Call Test] [Throughput] Application UL TP')
                voice_call_event_col_idx = header.index('[Event] Voice Call Event')
                mos_value_col_idx = header.index('[Call Test] [Voice Quality] [Per Rx Clip] MOS Value')
                latitude_col_idx = header.index('[General] [GPS] Latitude')
                longitude_col_idx = header.index('[General] [GPS] Longitude')
            except ValueError as e:
                print(f"Error: Missing expected header column in {os.path.basename(file_path)}: {e}")
                return results

            rows = list(reader) # Read all rows into a list

            # Helper function to find coordinates
            def _find_coords_in_row_or_upwards(start_index, lat_idx, lon_idx):
                # Check current row
                if len(rows[start_index]) > max(lat_idx, lon_idx) and rows[start_index][lat_idx] and rows[start_index][lon_idx]:
                    return {"latitude": rows[start_index][lat_idx], "longitude": rows[start_index][lon_idx]}
                # Search upwards
                for j in reversed(range(start_index)):
                    prev_row = rows[j]
                    if len(prev_row) > max(lat_idx, lon_idx) and prev_row[lat_idx] and prev_row[lon_idx]:
                        return {"latitude": prev_row[lat_idx], "longitude": prev_row[lon_idx]}
                return None

            # --- Search for Last MOS Value ---
            for i in reversed(range(len(rows))):
                row = rows[i]
                if len(row) > mos_value_col_idx:
                    try:
                        mos_value = float(row[mos_value_col_idx])
                        coords = _find_coords_in_row_or_upwards(i, latitude_col_idx, longitude_col_idx)
                        if coords:
                            lat = float(coords["latitude"])
                            lon = float(coords["longitude"])
                            distance = haversine_distance(lat, lon, BASE_STATION_COORDS["latitude"], BASE_STATION_COORDS["longitude"])
                            results["last_mos_value_coords"] = {**coords, "distance_to_base_station_km": distance}
                        break
                    except ValueError:
                        continue

            # --- Search for Voice Call Drop Event ---
            for i in reversed(range(len(rows))):
                row = rows[i]
                if len(row) > voice_call_event_col_idx and row[voice_call_event_col_idx] == '[Tool] Voice - Call Result : Drop':
                    coords = _find_coords_in_row_or_upwards(i, latitude_col_idx, longitude_col_idx)
                    if coords:
                        lat = float(coords["latitude"])
                        lon = float(coords["longitude"])
                        distance = haversine_distance(lat, lon, BASE_STATION_COORDS["latitude"], BASE_STATION_COORDS["longitude"])
                        results["voice_call_drop_coords"] = {**coords, "distance_to_base_station_km": distance}
                    break

            # --- Search for DL TP ---
            for i in reversed(range(len(rows))):
                row = rows[i]
                if len(row) > dl_tp_col_idx:
                    try:
                        dl_tp_value = float(row[dl_tp_col_idx])
                        if dl_tp_value > 1:
                            coords = _find_coords_in_row_or_upwards(i, latitude_col_idx, longitude_col_idx)
                            if coords:
                                lat = float(coords["latitude"])
                                lon = float(coords["longitude"])
                                distance = haversine_distance(lat, lon, BASE_STATION_COORDS["latitude"], BASE_STATION_COORDS["longitude"])
                                results["first_dl_tp_gt_1_coords"] = {**coords, "distance_to_base_station_km": distance}
                            break
                    except ValueError:
                        continue

            # --- Search for UL TP ---
            for i in reversed(range(len(rows))):
                row = rows[i]
                if len(row) > ul_tp_col_idx:
                    try:
                        ul_tp_value = float(row[ul_tp_col_idx])
                        if ul_tp_value > 1:
                            coords = _find_coords_in_row_or_upwards(i, latitude_col_idx, longitude_col_idx)
                            if coords:
                                lat = float(coords["latitude"])
                                lon = float(coords["longitude"])
                                distance = haversine_distance(lat, lon, BASE_STATION_COORDS["latitude"], BASE_STATION_COORDS["longitude"])
                                results["first_ul_tp_gt_1_coords"] = {**coords, "distance_to_base_station_km": distance}
                            break
                    except ValueError:
                        continue

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred while analyzing {os.path.basename(file_path)}: {e}")

    return results

import re

def find_dut_ref_files(directory):
    """
    Finds DUT and REF file pairs in the given directory.
    Assumes files are named like DUTx_RunY.csv and REFx_RunY.csv.
    """
    dut_files = {}  # Key: (device_number, run_number), Value: file_path
    ref_files = {}  # Key: (device_number, run_number), Value: file_path
    
    # Regex to match DUTx_RunY.csv or REFx_RunY.csv
    pattern = re.compile(r"(DUT|REF)(\d+)_Run(\d+)\.csv", re.IGNORECASE)

    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            device_type = match.group(1).upper()
            device_number = int(match.group(2))
            run_number = int(match.group(3))
            
            key = (device_number, run_number)
            file_path = os.path.join(directory, filename)

            if device_type == "DUT":
                dut_files[key] = file_path
            elif device_type == "REF":
                ref_files[key] = file_path
    
    paired_files = []
    # Sort keys to ensure consistent pairing order
    for key in sorted(dut_files.keys()):
        if key in ref_files:
            paired_files.append((dut_files[key], ref_files[key]))
    return paired_files

def compare_analysis_results(dut_results, ref_results, file_pair_name):
    """
    Compares the analysis results of DUT and REF files and prints a summary.
    """
    print(f"\n--- Comparison for {file_pair_name} ---")
    metrics = [
        "last_mos_value_coords",
        "voice_call_drop_coords",
        "first_dl_tp_gt_1_coords",
        "first_ul_tp_gt_1_coords"
    ]

    for metric in metrics:
        dut_metric = dut_results.get(metric)
        ref_metric = ref_results.get(metric)

        print(f"  Metric: {metric}")
        
        dut_distance = dut_metric["distance_to_base_station_km"] if dut_metric and "distance_to_base_station_km" in dut_metric else "N/A"
        ref_distance = ref_metric["distance_to_base_station_km"] if ref_metric and "distance_to_base_station_km" in ref_metric else "N/A"

        print(f"    DUT Distance to Base Station: {dut_distance:.2f} km" if isinstance(dut_distance, float) else f"    DUT Distance to Base Station: {dut_distance}")
        print(f"    REF Distance to Base Station: {ref_distance:.2f} km" if isinstance(ref_distance, float) else f"    REF Distance to Base Station: {ref_distance}")

        if isinstance(dut_distance, float) and isinstance(ref_distance, float):
            difference = dut_distance - ref_distance
            print(f"    Difference (DUT - REF): {difference:.2f} km")
        else:
            print("    Difference: Cannot calculate (missing data)")
    print("-" * (len(file_pair_name) + 20))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze coverage coordinates for DUT and REF files across multiple subdirectories.")
    parser.add_argument("base_directory", help="Path to the base directory (e.g., D:\\Fit4Launch\\Raw Data\\Coverage Performance\\5G VoNR Coverage Test).")
    args = parser.parse_args()

    base_path = args.base_directory
    
    # Assuming subfolders like n25, n41, n71
    subfolders = [f.name for f in os.scandir(base_path) if f.is_dir()]

    all_comparisons_raw_data = {} # Store raw results for potential further processing

    for subfolder in subfolders:
        subfolder_path = os.path.join(base_path, subfolder)
        print(f"Analyzing subfolder: {subfolder_path}")
        
        paired_files = find_dut_ref_files(subfolder_path)
        
        if not paired_files:
            print(f"No DUT/REF pairs found in {subfolder_path}")
            continue

        subfolder_comparisons = {}
        for dut_file, ref_file in paired_files:
            print(f"Processing DUT: {os.path.basename(dut_file)} and REF: {os.path.basename(ref_file)}")
            dut_results = analyze_coverage_coordinates(dut_file)
            ref_results = analyze_coverage_coordinates(ref_file)
            
            file_pair_name = f"{os.path.basename(dut_file).replace('.csv', '')}_vs_{os.path.basename(ref_file).replace('.csv', '')}"
            subfolder_comparisons[file_pair_name] = {
                "DUT": dut_results,
                "REF": ref_results
            }
            compare_analysis_results(dut_results, ref_results, file_pair_name) # Perform comparison immediately

        all_comparisons_raw_data[subfolder] = subfolder_comparisons
    
    print("\n--- Raw Analysis Results (for debugging/detailed view) ---")
    print(json.dumps(all_comparisons_raw_data, indent=4))
