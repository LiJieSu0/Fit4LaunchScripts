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
    Analyzes a CSV file to find the last valid GPS coordinate and calculates
    its distance to the base station. Returns a dictionary with the distance.
    """
    results = {
        "last_valid_coords_distance_to_base_station_km": None
    }

    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # Read the header row

            # Find column indices for Latitude and Longitude
            try:
                latitude_col_idx = header.index('[General] [GPS] Latitude')
                longitude_col_idx = header.index('[General] [GPS] Longitude')
            except ValueError as e:
                print(f"Error: Missing expected header column in {os.path.basename(file_path)}: {e}")
                return results

            rows = list(reader) # Read all rows into a list

            # Search for the last valid GPS coordinate from the bottom up
            for i in reversed(range(len(rows))):
                row = rows[i]
                if len(row) > max(latitude_col_idx, longitude_col_idx) and row[latitude_col_idx] and row[longitude_col_idx]:
                    try:
                        lat = float(row[latitude_col_idx])
                        lon = float(row[longitude_col_idx])
                        distance = haversine_distance(lat, lon, BASE_STATION_COORDS["latitude"], BASE_STATION_COORDS["longitude"])
                        results["last_valid_coords_distance_to_base_station_km"] = distance
                        break # Found the last valid coordinate, stop searching
                    except ValueError:
                        continue # Skip if conversion to float fails

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred while analyzing {os.path.basename(file_path)}: {e}")

    return results

import re

def find_dut_ref_files(directory):
    """
    Finds PC2.csv and PC3.csv in the given directory and treats them as DUT and REF.
    """
    pc2_file = None
    pc3_file = None

    for filename in os.listdir(directory):
        if filename.lower() == "pc2.csv":
            pc2_file = os.path.join(directory, filename)
        elif filename.lower() == "pc3.csv":
            pc3_file = os.path.join(directory, filename)
    
    paired_files = []
    if pc2_file and pc3_file:
        paired_files.append((pc2_file, pc3_file)) # Treat PC2 as DUT, PC3 as REF
    elif pc2_file:
        paired_files.append((pc2_file, None)) # Only PC2 found
    elif pc3_file:
        paired_files.append((None, pc3_file)) # Only PC3 found
    return paired_files

def compare_analysis_results(dut_results, ref_results, file_pair_name):
    """
    Compares the analysis results of DUT (PC2) and REF (PC3) files and prints a summary.
    """
    print(f"\n--- Comparison for {file_pair_name} ---")
    
    dut_distance = dut_results.get("last_valid_coords_distance_to_base_station_km")
    ref_distance = ref_results.get("last_valid_coords_distance_to_base_station_km")

    dut_distance_str = f"{dut_distance:.2f} km" if isinstance(dut_distance, float) else "N/A"
    ref_distance_str = f"{ref_distance:.2f} km" if isinstance(ref_distance, float) else "N/A"

    print(f"    PC2 Distance to Base Station: {dut_distance_str}")
    print(f"    PC3 Distance to Base Station: {ref_distance_str}")

    if isinstance(dut_distance, float) and isinstance(ref_distance, float):
        difference = dut_distance - ref_distance
        print(f"    Difference (PC2 - PC3): {difference:.2f} km")
    else:
        print("    Difference: Cannot calculate (missing data)")
    print("-" * (len(file_pair_name) + 20))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze coverage coordinates for PC2 and PC3 files across multiple subdirectories.")
    parser.add_argument("base_directory", help="Path to the base directory (e.g., D:\\Fit4Launch\\Raw Data\\Coverage Performance\\5G n41 HPUE Coverage Test).")
    args = parser.parse_args()

    base_path = args.base_directory
    
    # Assuming subfolders like Run1, Run2, etc.
    subfolders = [f.name for f in os.scandir(base_path) if f.is_dir() and f.name.startswith("Run")]
    subfolders.sort() # Ensure runs are processed in order

    all_comparisons_raw_data = {} # Store raw results for potential further processing

    for subfolder in subfolders:
        subfolder_path = os.path.join(base_path, subfolder)
        print(f"Analyzing subfolder: {subfolder_path}")
        
        paired_files = find_dut_ref_files(subfolder_path)
        
        if not paired_files:
            print(f"No PC2/PC3 files found in {subfolder_path}")
            continue

        # For PC2.csv and PC3.csv, there should only be one pair
        dut_file, ref_file = paired_files[0] 
        
        print(f"Processing PC2: {os.path.basename(dut_file) if dut_file else 'N/A'} and PC3: {os.path.basename(ref_file) if ref_file else 'N/A'}")
        
        dut_results = analyze_coverage_coordinates(dut_file) if dut_file else {}
        ref_results = analyze_coverage_coordinates(ref_file) if ref_file else {}
        
        file_pair_name = f"{os.path.basename(dut_file).replace('.csv', '') if dut_file else 'PC2'}_vs_{os.path.basename(ref_file).replace('.csv', '') if ref_file else 'PC3'}"
        
        all_comparisons_raw_data[subfolder] = {
            "PC2": dut_results.get("last_valid_coords_distance_to_base_station_km"),
            "PC3": ref_results.get("last_valid_coords_distance_to_base_station_km")
        }
        compare_analysis_results(dut_results, ref_results, file_pair_name) # Perform comparison immediately

    print("\n--- Raw Analysis Results (for frontend consumption) ---")
    print(json.dumps(all_comparisons_raw_data, indent=4))
