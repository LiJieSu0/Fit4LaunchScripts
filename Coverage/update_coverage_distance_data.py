import json
import math
import os
import sys

# Add the parent directory of Scripts/Coverage to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Scripts.Coverage.coverage_coordinate_analyzer import haversine_distance

BASE_STATION_COORDS = {"latitude": 47.128234, "longitude": -122.356792}
DATA_ANALYSIS_RESULTS_PATH = "Scripts/React/frontend/src/data_analysis_results.json"
OUTPUT_JSON_PATH = "Scripts/React/frontend/src/coverage_distance_data.json"

def calculate_distances_from_analysis_results():
    try:
        with open(DATA_ANALYSIS_RESULTS_PATH, 'r', encoding='utf-8') as f:
            data_results = json.load(f)
    except FileNotFoundError:
        print(f"Error: {DATA_ANALYSIS_RESULTS_PATH} not found.")
        return

    n41_hpue_data = data_results.get("Coverage Performance", {}).get("5G n41 HPUE Coverage Test", {})

    pc2_distances = []
    pc3_distances = []
    
    runs = ["Run1", "Run2", "Run3", "Run4", "Run5"]
    
    for run_key in runs:
        run_data = n41_hpue_data.get(run_key, [])
        
        pc2_coords = None
        pc3_coords = None

        for device_data in run_data:
            if device_data.get("Device type") == "PC2":
                pc2_coords = {"latitude": device_data["latitude"], "longitude": device_data["longitude"]}
            elif device_data.get("Device type") == "PC3":
                pc3_coords = {"latitude": device_data["latitude"], "longitude": device_data["longitude"]}
        
        if pc2_coords:
            dist = haversine_distance(pc2_coords["latitude"], pc2_coords["longitude"], 
                                      BASE_STATION_COORDS["latitude"], BASE_STATION_COORDS["longitude"])
            pc2_distances.append(dist)
        else:
            pc2_distances.append(None)

        if pc3_coords:
            dist = haversine_distance(pc3_coords["latitude"], pc3_coords["longitude"], 
                                      BASE_STATION_COORDS["latitude"], BASE_STATION_COORDS["longitude"])
            pc3_distances.append(dist)
        else:
            pc3_distances.append(None)

    # Calculate averages
    avg_pc2 = sum(d for d in pc2_distances if d is not None) / len([d for d in pc2_distances if d is not None]) if any(d is not None for d in pc2_distances) else None
    avg_pc3 = sum(d for d in pc3_distances if d is not None) / len([d for d in pc3_distances if d is not None]) if any(d is not None for d in pc3_distances) else None

    # Prepare data for output JSON
    output_headers = ["Device"] + runs + ["Average"]
    output_rows = []

    pc2_row = {"Device": "PC2"}
    for i, run_key in enumerate(runs):
        pc2_row[run_key] = pc2_distances[i]
    pc2_row["Average"] = avg_pc2
    output_rows.append(pc2_row)

    pc3_row = {"Device": "PC3"}
    for i, run_key in enumerate(runs):
        pc3_row[run_key] = pc3_distances[i]
    pc3_row["Average"] = avg_pc3
    output_rows.append(pc3_row)

    output_data = {
        "headers": output_headers,
        "rows": output_rows
    }

    with open(OUTPUT_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"Successfully updated {OUTPUT_JSON_PATH}")

if __name__ == "__main__":
    calculate_distances_from_analysis_results()
