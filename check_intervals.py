import json
import sys

def check_data_analysis_results(file_path, output_file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}")
        return

    # Redirect stdout to the output file
    original_stdout = sys.stdout
    try:
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            sys.stdout = outfile
            found_issues = [False] # Use a list to pass by reference

            def find_and_check(current_obj, path_keys):
                if isinstance(current_obj, dict):
                    # Check if this dictionary has 'Protocol Type' and 'Throughput'
                    if "Protocol Type" in current_obj and "Throughput" in current_obj and \
                       isinstance(current_obj["Throughput"], dict):
                        
                        protocol_type = current_obj["Protocol Type"].upper()
                        if "UDP" in protocol_type or "HTTP" in protocol_type:
                            throughput_data = current_obj["Throughput"]
                            if "Number of Intervals" in throughput_data and throughput_data["Number of Intervals"] < 20:
                                print(f"Issue found at path {' -> '.join(path_keys)}:")
                                print(f"  Protocol Type: {current_obj['Protocol Type']}")
                                print(f"  Number of Intervals: {throughput_data['Number of Intervals']} (less than 20)")
                                print(json.dumps(current_obj, indent=2))
                                found_issues[0] = True
                    
                    # Recurse for all values in the current dictionary
                    for key, value in current_obj.items():
                        find_and_check(value, path_keys + [key])

                elif isinstance(current_obj, list):
                    # Recurse for all items in the list
                    for index, item in enumerate(current_obj):
                        find_and_check(item, path_keys + [str(index)])

            find_and_check(data, [])

            if not found_issues[0]:
                print("No UDP or HTTP entries found with 'number of intervals' less than 20.")
    finally:
        sys.stdout = original_stdout # Restore original stdout

if __name__ == "__main__":
    json_file_path = "Scripts/React/frontend/src/data_analysis_results.json"
    output_file = "interval_check_results.txt" # Output file in the current working directory
    check_data_analysis_results(json_file_path, output_file)
