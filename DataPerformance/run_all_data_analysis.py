import os
import subprocess
import sys
import pandas as pd
import json # Import the json module
# Add the current script's directory to sys.path to enable direct imports
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

# Import the analysis functions from data_performance_statics.py
# Assuming data_performance_statics.py is in the same directory
import data_performance_statics
from data_performance_statics import _determine_analysis_parameters # Import the new helper function
import ping_statics # Import the ping_statics module
import data_path_reader # Import the new path reader script

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    base_raw_data_dir = "Raw Data" # Changed to "Raw Data" as per user's path
    
    # Define a list of directories to process, along with their analysis type
    # These paths are relative to base_raw_data_dir
    # This list can be easily extended for future additions
    directories_to_process = [
        {"path": "5G AUTO DP", "analysis_type": "data_performance"},
        {"path": "5G NSA DP", "analysis_type": "data_performance"},
        {"path": "TestInvalid", "analysis_type": "data_performance"}, # Add the new test directory
        # Add other directories here as needed, e.g.:
        # {"path": "Call Performance", "analysis_type": "call_performance"},
        # {"path": "Ping", "analysis_type": "ping"},
    ]
    
    all_collected_results = {}
    invalid_data_files = [] # Initialize a list to store paths of files with invalid data
    valid_data_files = [] # Initialize a list to store paths of files with valid data
    invalid_data_dir = os.path.join(base_raw_data_dir, "Invalid") # Define the invalid directory
    os.makedirs(invalid_data_dir, exist_ok=True) # Ensure the invalid directory exists
    def _insert_into_nested_dict(data_dict, path_components, value):
        """Inserts a value into a nested dictionary based on a list of path components."""
        current_level = data_dict
        for i, component in enumerate(path_components):
            if i == len(path_components) - 1:
                current_level[component] = value
            else:
                if component not in current_level:
                    current_level[component] = {}
                current_level = current_level[component]

    # Get all CSV file paths using the new data_path_reader script
    all_csv_files_processed = data_path_reader.get_csv_file_paths(base_raw_data_dir, directories_to_process)

    # Now iterate through the collected files for analysis
    for csv_file_path in all_csv_files_processed:
        # Determine analysis type based on the file path or configuration if needed
        analysis_type_for_file = "data_performance"
        if "ping" in csv_file_path.lower():
            analysis_type_for_file = "ping"

        stats = None # Initialize stats for each file
        current_file_has_invalid_data = False # Flag for the current file

        if analysis_type_for_file == "ping":
            print(f"--- Analyzing Ping file: {csv_file_path} ---")
            
            # Determine device type for ping files
            device_type_for_ping = None
            filename_lower = os.path.basename(csv_file_path).lower()
            if "dut" in filename_lower:
                device_type_for_ping = "DUT"
            elif "ref" in filename_lower:
                device_type_for_ping = "REF"

            ping_stats_result = ping_statics.calculate_ping_statistics(csv_file_path, device_type=device_type_for_ping)
            if ping_stats_result:
                stats = ping_stats_result # ping_statics now returns the full dictionary including "Ping RTT" and "Device Type"
        else: # data_performance analysis
            params = _determine_analysis_parameters(csv_file_path)

            if params is None:
                file_name = os.path.basename(csv_file_path).lower()
                print(f"Warning: Could not fully determine analysis parameters from filename: {file_name}. Skipping.")
                current_file_has_invalid_data = True # Mark as invalid if parameters cannot be determined
                stats = None # Ensure stats is None if skipping
            else:
                all_file_stats = {}
                all_file_stats["Device Type"] = params["device_type_detected"]
                all_file_stats["Analysis Direction"] = params["analysis_direction_detected"]
                all_file_stats["Protocol Type"] = params["protocol_type_detected"]
                all_file_stats["Network Type"] = params["network_type_detected"]

                if params["protocol_type_detected"] == "HTTP":
                    if params["analysis_direction_detected"] == "DL":
                        throughput_stats = data_performance_statics.analyze_throughput(csv_file_path, params["column_to_analyze_throughput"], params["event_col"], params["start_event"], params["end_event"], fallback_event_col_name=params["event_col_fallback"])
                        if throughput_stats:
                            all_file_stats["Throughput"] = throughput_stats
                    elif params["analysis_direction_detected"] == "UL":
                        throughput_stats = data_performance_statics.analyze_throughput(csv_file_path, params["column_to_analyze_throughput"], params["event_col"], params["start_event"], params["end_event"], fallback_event_col_name=params["event_col_fallback"])
                        if throughput_stats:
                            all_file_stats["Throughput"] = throughput_stats
                elif params["protocol_type_detected"] == "UDP":
                    if params["analysis_direction_detected"] == "DL":
                        throughput_stats = data_performance_statics.analyze_throughput(csv_file_path, params["column_to_analyze_throughput"], params["event_col"], params["start_event"], params["end_event"], fallback_event_col_name=params["event_col_fallback"])
                        if throughput_stats:
                            all_file_stats["Throughput"] = throughput_stats

                        jitter_stats = data_performance_statics.analyze_jitter(csv_file_path, params["column_to_analyze_jitter"], params["event_col"], params["start_event"], params["end_event"], fallback_event_col_name=params["event_col_fallback"])
                        if jitter_stats:
                            all_file_stats["Jitter"] = jitter_stats

                        error_ratio_stats = data_performance_statics.analyze_error_ratio(csv_file_path, params["column_to_analyze_error_ratio"], params["event_col"], params["start_event"], params["end_event"], fallback_event_col_name=params["event_col_fallback"])
                        if error_ratio_stats:
                            all_file_stats["Error Ratio"] = error_ratio_stats

                    elif params["analysis_direction_detected"] == "UL":
                        throughput_stats = data_performance_statics.analyze_throughput(csv_file_path, params["column_to_analyze_throughput"], params["event_col"], params["start_event"], params["end_event"], fallback_event_col_name=params["event_col_fallback"])
                        if throughput_stats:
                            all_file_stats["Throughput"] = throughput_stats

                        jitter_stats = data_performance_statics.analyze_jitter(csv_file_path, params["column_to_analyze_ul_jitter"], params["event_col"], params["start_event"], params["end_event"], fallback_event_col_name=params["event_col_fallback"])
                        if jitter_stats:
                            all_file_stats["Jitter"] = jitter_stats

                        error_ratio_stats = data_performance_statics.analyze_error_ratio(csv_file_path, params["column_to_analyze_ul_error_ratio"], params["event_col"], params["start_event"], params["end_event"], fallback_event_col_name=params["event_col_fallback"])
                        if error_ratio_stats:
                            all_file_stats["Error Ratio"] = error_ratio_stats
                elif params["protocol_type_detected"] == "WEB_PAGE":
                    web_page_stats = data_performance_statics.analyze_web_page_load_time(csv_file_path, params["event_col"], params["start_event"], params["end_event"], params["column_to_analyze_total_duration"], fallback_event_col_name=params["event_col_fallback"])
                    if web_page_stats:
                        all_file_stats["Web Page Load Time"] = web_page_stats
                
                stats = all_file_stats # Assign collected stats to the 'stats' variable
        
        file_moved = False # Flag to check if the file was moved
        is_invalid = False # Flag to determine if the file is invalid

        if analysis_type_for_file == "ping":
            if not stats or stats.get("Ping RTT", {}).get("min") is None: # Check if ping stats are valid
                is_invalid = True
        else: # data_performance analysis
            params = _determine_analysis_parameters(csv_file_path)
            if params is None:
                is_invalid = True
            else:
                all_file_stats = {}
                all_file_stats["Device Type"] = params["device_type_detected"]
                all_file_stats["Analysis Direction"] = params["analysis_direction_detected"]
                all_file_stats["Protocol Type"] = params["protocol_type_detected"]
                all_file_stats["Network Type"] = params["network_type_detected"]

                if params["protocol_type_detected"] == "HTTP":
                    if params["analysis_direction_detected"] == "DL":
                        throughput_stats = data_performance_statics.analyze_throughput(csv_file_path, params["column_to_analyze_throughput"], params["event_col"], params["start_event"], params["end_event"], fallback_event_col_name=params["event_col_fallback"])
                        if throughput_stats:
                            all_file_stats["Throughput"] = throughput_stats
                    elif params["analysis_direction_detected"] == "UL":
                        throughput_stats = data_performance_statics.analyze_throughput(csv_file_path, params["column_to_analyze_throughput"], params["event_col"], params["start_event"], params["end_event"], fallback_event_col_name=params["event_col_fallback"])
                        if throughput_stats:
                            all_file_stats["Throughput"] = throughput_stats
                elif params["protocol_type_detected"] == "UDP":
                    if params["analysis_direction_detected"] == "DL":
                        throughput_stats = data_performance_statics.analyze_throughput(csv_file_path, params["column_to_analyze_throughput"], params["event_col"], params["start_event"], params["end_event"], fallback_event_col_name=params["event_col_fallback"])
                        if throughput_stats:
                            all_file_stats["Throughput"] = throughput_stats

                        jitter_stats = data_performance_statics.analyze_jitter(csv_file_path, params["column_to_analyze_jitter"], params["event_col"], params["start_event"], params["end_event"], fallback_event_col_name=params["event_col_fallback"])
                        if jitter_stats:
                            all_file_stats["Jitter"] = jitter_stats

                        error_ratio_stats = data_performance_statics.analyze_error_ratio(csv_file_path, params["column_to_analyze_error_ratio"], params["event_col"], params["start_event"], params["end_event"], fallback_event_col_name=params["event_col_fallback"])
                        if error_ratio_stats:
                            all_file_stats["Error Ratio"] = error_ratio_stats

                    elif params["analysis_direction_detected"] == "UL":
                        throughput_stats = data_performance_statics.analyze_throughput(csv_file_path, params["column_to_analyze_throughput"], params["event_col"], params["start_event"], params["end_event"], fallback_event_col_name=params["event_col_fallback"])
                        if throughput_stats:
                            all_file_stats["Throughput"] = throughput_stats

                        jitter_stats = data_performance_statics.analyze_jitter(csv_file_path, params["column_to_analyze_ul_jitter"], params["event_col"], params["start_event"], params["end_event"], fallback_event_col_name=params["event_col_fallback"])
                        if jitter_stats:
                            all_file_stats["Jitter"] = jitter_stats

                        error_ratio_stats = data_performance_statics.analyze_error_ratio(csv_file_path, params["column_to_analyze_ul_error_ratio"], params["event_col"], params["start_event"], params["end_event"], fallback_event_col_name=params["event_col_fallback"])
                        if error_ratio_stats:
                            all_file_stats["Error Ratio"] = error_ratio_stats
                elif params["protocol_type_detected"] == "WEB_PAGE":
                    web_page_stats = data_performance_statics.analyze_web_page_load_time(csv_file_path, params["event_col"], params["start_event"], params["end_event"], params["column_to_analyze_total_duration"], fallback_event_col_name=params["event_col_fallback"])
                    if web_page_stats:
                        all_file_stats["Web Page Load Time"] = web_page_stats
                
                stats = all_file_stats # Assign collected stats to the 'stats' variable

                # Check if 'stats' (all_file_stats) contains actual statistical data beyond just the metadata.
                # The metadata keys are "Device Type", "Analysis Direction", "Protocol Type", "Network Type".
                # Statistical keys are "Throughput", "Jitter", "Error Ratio", "Web Page Load Time".
                
                statistical_keys = ["Throughput", "Jitter", "Error Ratio", "Web Page Load Time"]
                has_statistical_data = any(key in all_file_stats for key in statistical_keys)

                if not has_statistical_data:
                    is_invalid = True
                else:
                    # Protocol-specific checks for required statistical data
                    if params["protocol_type_detected"] == "UDP":
                        required_udp_stats = ["Throughput", "Jitter", "Error Ratio"]
                        if not all(key in all_file_stats for key in required_udp_stats):
                            is_invalid = True
                    # Add other protocol-specific checks here if needed

                    if not is_invalid: # Only proceed to check for NA/None if not already marked invalid
                        # Check for NA/None values within the collected statistical data
                        for key in statistical_keys:
                            if key in all_file_stats:
                                value = all_file_stats[key]
                                if isinstance(value, dict):
                                    for sub_key, sub_value in value.items():
                                        if pd.isna(sub_value) or sub_value is None:
                                            is_invalid = True
                                            break
                                elif pd.isna(value) or value is None:
                                    is_invalid = True
                            if is_invalid:
                                break
        
        if is_invalid:
            invalid_data_files.append(csv_file_path)
            print(f"Invalid data detected or analysis skipped for: {csv_file_path}. Moving to invalid directory.")
            destination_path = os.path.join(invalid_data_dir, os.path.basename(csv_file_path))
            os.rename(csv_file_path, destination_path)
            file_moved = True
        else:
            valid_data_files.append(csv_file_path)
            print(f"Valid data detected for: {csv_file_path}. Added to valid_data_files.")
        
        # Construct the hierarchical path for the JSON output only if the file was not moved
        if stats and not file_moved: # Only insert if stats were successfully collected and the file was not moved
            relative_path = os.path.relpath(csv_file_path, base_raw_data_dir)
            path_components = relative_path.replace("\\", "/").split('/') # Use forward slashes for consistency
            
            # The last component is the filename, remove .csv extension
            filename_without_ext = os.path.splitext(path_components[-1])[0]
            path_components[-1] = filename_without_ext

            _insert_into_nested_dict(all_collected_results, path_components, stats)
    
    # Write the collected list of CSV files to a TXT file using the new data_path_reader script
    data_path_reader.write_csv_paths_with_two_parents(all_csv_files_processed, base_raw_data_dir) # Function name remains, but behavior changed

    # Write invalid data file paths to a text file
    invalid_output_path = "invalid_data_paths.txt"
    with open(invalid_output_path, 'w', encoding='utf-8') as f:
        for path in invalid_data_files:
            f.write(f"{path}\n")
    if invalid_data_files:
        print(f"\nInvalid data file paths written to: {invalid_output_path}")
    else:
        print("\nNo invalid data files found.")

    # Write valid data file paths to a text file
    valid_output_path = "valid_data_paths.txt"
    with open(valid_output_path, 'w', encoding='utf-8') as f:
        for path in valid_data_files:
            f.write(f"{path}\n")
    if valid_data_files:
        print(f"\nValid data file paths written to: {valid_output_path}")
    else:
        print("\nNo valid data files found.")

    # Generate summary.txt
    summary_output_path = "summary.txt"
    total_files_processed = len(all_csv_files_processed)
    correctly_processed_files = len(valid_data_files)
    incorrect_paths_count = len(invalid_data_files)

    with open(summary_output_path, 'w', encoding='utf-8') as f:
        f.write(f"Total files processed: {total_files_processed}\n")
        f.write(f"Correctly processed statistics: {correctly_processed_files}\n")
        f.write(f"Incorrect paths: {incorrect_paths_count}\n")
    print(f"\nSummary written to: {summary_output_path}")

    if all_collected_results:
        # Output results to a JSON file for the React app
        json_output_path = os.path.join("Scripts", "React", "frontend", "src", "data_analysis_results.json")
        with open(json_output_path, 'w', encoding='utf-8') as f:
            json.dump(all_collected_results, f, ensure_ascii=False, indent=4)
        print(f"\nJSON data generated: {json_output_path}")
    else:
        print("No data collected to generate a report.")
