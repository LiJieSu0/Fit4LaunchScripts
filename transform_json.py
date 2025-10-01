import json
import re

def transform_coverage_data(data):
    if "Coverage" in data and "5G VoNR Coverage Test" in data["Coverage"] and "Run1" in data["Coverage"]["5G VoNR Coverage Test"]:
        run1_data = data["Coverage"]["5G VoNR Coverage Test"]["Run1"]
        new_run1_data = {}
        for key, value in run1_data.items():
            if "dut" in key.lower():
                new_run1_data["DUT"] = value["DUT"]
            elif "ref" in key.lower():
                new_run1_data["REF"] = value["REF"]
            else:
                new_run1_data[key] = value
        data["Coverage"]["5G VoNR Coverage Test"]["Run1"] = new_run1_data
    return data

if __name__ == "__main__":
    json_file_path = "Scripts/React/frontend/src/data_analysis_results.json"
    
    with open(json_file_path, 'r') as f:
        json_data = json.load(f)

    transformed_data = transform_coverage_data(json_data)

    with open(json_file_path, 'w') as f:
        json.dump(transformed_data, f, indent=4)

    print("JSON transformation complete.")
