import os
import subprocess
import sys
import pandas as pd
import json # Import the json module
# Add the 'Scripts' directory to sys.path to enable imports from it
script_dir = os.path.dirname(os.path.abspath(__file__))
scripts_parent_dir = os.path.dirname(script_dir) # This is 'Scripts' directory
if scripts_parent_dir not in sys.path:
    sys.path.insert(0, scripts_parent_dir)

# Import the analysis functions from data_performance_statics.py
# Assuming data_performance_statics.py is in the same directory
import data_performance_statics
from data_performance_statics import _determine_analysis_parameters # Import the new helper function
import ping_statics # Import the ping_statics module
import mrab_statistics # Import the mrab_statistics module
import data_path_reader # Import the new path reader script
import check_empty_data # Import check_empty_data directly

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    base_raw_data_dir = "Raw Data" # Changed to "Raw Data" as per user's path
    output_dir = os.path.join(os.path.dirname(script_dir), "Analyze Summary") # Define output directory
    os.makedirs(output_dir, exist_ok=True) # Ensure the output directory exists
    
    # Define a list of directories to process, along with their analysis type
    # These paths are relative to base_raw_data_dir
    # This list can be easily extended for future additions
    directories_to_process = [
        {"path": "5G AUTO DP", "analysis_type": "data_performance"},
        {"path": "5G NSA DP", "analysis_type": "data_performance"},
        {"path": "5G VoNR MRAB Stationary", "analysis_type": "mrab_performance"}, # Add MRAB directory
        {"path": "TestInvalid", "analysis_type": "data_performance"}, # Add the new test directory
        # Add other directories here as needed, e.g.:
        # {"path": "Call Performance", "analysis_type": "call_performance"},
        # {"path": "Ping", "analysis_type": "ping"},
    ]
    
    all_collected_results = {}
    invalid_data_files = [] # Initialize a list to store paths of files with invalid data
    valid_data_files = [] # Initialize a list to store paths of files with valid data
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
        all_file_stats = {} # Initialize stats for the current file
        current_file_has_invalid_data = False # Flag for the current file

        params = _determine_analysis_parameters(csv_file_path)

        if params is None:
            file_name = os.path.basename(csv_file_path).lower()
            print(f"Warning: Could not fully determine analysis parameters from filename: {file_name}. Skipping.")
            current_file_has_invalid_data = True # Mark as invalid if parameters cannot be determined
        else:
            all_file_stats["Device Type"] = params["device_type_detected"]
            if params["analysis_direction_detected"] is not None:
                all_file_stats["Analysis Direction"] = params["analysis_direction_detected"]
            if params["protocol_type_detected"] is not None:
                all_file_stats["Protocol Type"] = params["protocol_type_detected"]
            all_file_stats["Network Type"] = params["network_type_detected"]
            all_file_stats["Analysis Type"] = params["analysis_type_detected"] # Store the detected analysis type

            # Always attempt to collect data performance stats if applicable
            if params["analysis_type_detected"] == "data_performance":
                if params["protocol_type_detected"] == "HTTP":
                    if params["analysis_direction_detected"] == "DL":
                        throughput_stats = data_performance_statics.analyze_throughput(csv_file_path, params["column_to_analyze_throughput"], params["event_col"], params["start_event"], params["end_event"], fallback_column_name=params["column_to_analyze_throughput_fallback"], fallback_event_col_name=params["event_col_fallback"], third_fallback_column_name=params["column_to_analyze_throughput_third_fallback"])
                        if throughput_stats:
                            all_file_stats["Throughput"] = throughput_stats
                    elif params["analysis_direction_detected"] == "UL":
                        throughput_stats = data_performance_statics.analyze_throughput(csv_file_path, params["column_to_analyze_throughput"], params["event_col"], params["start_event"], params["end_event"], fallback_column_name=params["column_to_analyze_throughput_fallback"], fallback_event_col_name=params["event_col_fallback"], third_fallback_column_name=params["column_to_analyze_throughput_third_fallback"])
                        if throughput_stats:
                            all_file_stats["Throughput"] = throughput_stats
                elif params["protocol_type_detected"] == "UDP":
                    if params["analysis_direction_detected"] == "DL":
                        throughput_stats = data_performance_statics.analyze_throughput(csv_file_path, params["column_to_analyze_throughput"], params["event_col"], params["start_event"], params["end_event"], fallback_column_name=params["column_to_analyze_throughput_fallback"], fallback_event_col_name=params["event_col_fallback"], third_fallback_column_name=params["column_to_analyze_throughput_third_fallback"])
                        if throughput_stats:
                            all_file_stats["Throughput"] = throughput_stats

                        jitter_stats = data_performance_statics.analyze_jitter(csv_file_path, params["column_to_analyze_jitter"], params["event_col"], params["start_event"], params["end_event"], fallback_event_col_name=params["event_col_fallback"])
                        if jitter_stats:
                            all_file_stats["Jitter"] = jitter_stats

                        error_ratio_stats = data_performance_statics.analyze_error_ratio(csv_file_path, params["column_to_analyze_error_ratio"], params["event_col"], params["start_event"], params["end_event"], fallback_event_col_name=params["event_col_fallback"])
                        if error_ratio_stats:
                            all_file_stats["Error Ratio"] = error_ratio_stats

                    elif params["analysis_direction_detected"] == "UL":
                        throughput_stats = data_performance_statics.analyze_throughput(csv_file_path, params["column_to_analyze_throughput"], params["event_col"], params["start_event"], params["end_event"], fallback_column_name=params["column_to_analyze_throughput_fallback"], fallback_event_col_name=params["event_col_fallback"], third_fallback_column_name=params["column_to_analyze_throughput_third_fallback"])
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
                elif params["protocol_type_detected"] == "PING":
                    # If it's a direct PING file, get its stats
                    ping_stats_result = ping_statics.calculate_ping_statistics(csv_file_path, device_type=params["device_type_detected"])
                    if ping_stats_result and "Ping RTT" in ping_stats_result:
                        all_file_stats["Ping RTT"] = ping_stats_result["Ping RTT"]
                
                # Additionally, check for related ping files if it's a "drive" path and not already a PING protocol
                if params["is_drive_path"] and params["protocol_type_detected"] != "PING":
                    related_ping_file = data_performance_statics._find_related_ping_file(csv_file_path, params["device_type_detected"])
                    if related_ping_file:
                        print(f"Found related Ping file for drive path: {related_ping_file}")
                        ping_stats_result = ping_statics.calculate_ping_statistics(related_ping_file, params["device_type_detected"])
                        if ping_stats_result and "Ping RTT" in ping_stats_result:
                            all_file_stats["Ping RTT"] = ping_stats_result["Ping RTT"]
                    else:
                        print(f"No related Ping file found for drive path: {csv_file_path}")
            
            # Add MRAB statistics collection
            elif params["analysis_type_detected"] == "mrab_performance":
                target_header = "[Call Test] [Throughput] Application DL TP"
                threshold = 10
                mrab_intervals = mrab_statistics.extract_intervals_and_values(csv_file_path, target_header, threshold)
                if mrab_intervals:
                    mrab_analysis_results = mrab_statistics.analyze_grouped_intervals(mrab_intervals)
                    if mrab_analysis_results:
                        all_file_stats["MRAB Statistics"] = mrab_analysis_results
                else:
                    print(f"No MRAB intervals found or an error occurred for: {csv_file_path}")

            # Determine if the file is invalid: it's invalid if no statistical data was collected
            statistical_keys = ["Throughput", "Jitter", "Error Ratio", "Web Page Load Time", "Ping RTT", "MRAB Statistics"]
            has_any_statistical_data = False
            for key in statistical_keys:
                if key in all_file_stats and all_file_stats[key]: # Check if key exists and its value (the dict) is not empty
                    has_any_statistical_data = True
                    break
            
            if not has_any_statistical_data:
                current_file_has_invalid_data = True
        
        if current_file_has_invalid_data:
            invalid_data_files.append(csv_file_path)
            print(f"Invalid data detected or analysis skipped for: {csv_file_path}. File will remain in its original location.")
        else:
            valid_data_files.append(csv_file_path)
            print(f"Valid data detected for: {csv_file_path}. Added to valid_data_files.")
        
        # Construct the hierarchical path for the JSON output
        if all_file_stats: # Only insert if stats were successfully collected (even if it's just device type etc.)
            relative_path = os.path.relpath(csv_file_path, base_raw_data_dir)
            path_components = relative_path.replace("\\", "/").split('/') # Use forward slashes for consistency
            
            # The last component is the filename, remove .csv extension
            filename_without_ext = os.path.splitext(path_components[-1])[0]
            path_components[-1] = filename_without_ext
            
            _insert_into_nested_dict(all_collected_results, path_components, all_file_stats)
    
    # Write the collected list of CSV files to a TXT file using the new data_path_reader script
    data_path_reader.write_csv_paths_with_two_parents(all_csv_files_processed, base_raw_data_dir, output_dir) # Pass output_dir

    # Write invalid data file paths to a text file
    invalid_output_path = os.path.join(output_dir, "invalid_data_paths.txt")
    with open(invalid_output_path, 'w', encoding='utf-8') as f:
        for path in invalid_data_files:
            f.write(f"{path}\n")
    if invalid_data_files:
        print(f"\nInvalid data file paths written to: {invalid_output_path}")
    else:
        print("\nNo invalid data files found.")

    # Write valid data file paths to a text file
    valid_output_path = os.path.join(output_dir, "valid_data_paths.txt")
    with open(valid_output_path, 'w', encoding='utf-8') as f:
        for path in valid_data_files:
            f.write(f"{path}\n")
    if valid_data_files:
        print(f"\nValid data file paths written to: {valid_output_path}")
    else:
        print("\nNo valid data files found.")

    # Generate Processed File Count.txt
    summary_output_path = os.path.join(output_dir, "Processed File Count.txt")
    total_files_processed = len(all_csv_files_processed)
    correctly_processed_files = len(valid_data_files)
    incorrect_paths_count = len(invalid_data_files)

    with open(summary_output_path, 'w', encoding='utf-8') as f:
        f.write(f"Total files processed: {total_files_processed}\n")
        f.write(f"Correctly processed statistics: {correctly_processed_files}\n")
        f.write(f"Incorrect paths: {incorrect_paths_count}\n")
    print(f"\nProcessed file count written to: {summary_output_path}")

    if all_collected_results:
        # Output results to a JSON file for the React app
        json_output_path = os.path.join("Scripts", "React", "frontend", "src", "data_analysis_results.json")
        with open(json_output_path, 'w', encoding='utf-8') as f:
            json.dump(all_collected_results, f, ensure_ascii=False, indent=4)
        print(f"\nJSON data generated: {json_output_path}")
    else:
        print("No data collected to generate a report.")
    
    # Call check_empty_data.main with the output_dir
    check_empty_data.main(output_dir)
