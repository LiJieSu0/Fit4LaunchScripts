import os
import subprocess
import sys
import pandas as pd
import json # Import the json module
import re # Import the re module for regex operations
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
from CallPerformance.call_analyze import analyze_directory, _calculate_fisher_exact_criteria # Import analyze_directory and _calculate_fisher_exact_criteria
from VoiceQuality.voice_quality_analyzer import process_directory as analyze_voice_quality_directory # Import process_directory from voice_quality_analyzer.py
from VoiceQuality.audio_delay_analyzer import process_directory as analyze_audio_delay_directory # Import process_directory from audio_delay_analyzer.py
from Coverage.coverage_coordinate_analyzer import analyze_coverage_coordinates, find_dut_ref_files, compare_analysis_results # Import the coverage analysis functions
from Coverage.n41_coverage_analyzer import analyze_n41_coverage, extract_coverage_data_to_csv # Import the n41 coverage analyzer and generic data extractor

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    base_raw_data_dir = "Raw Data" # Changed to "Raw Data" as per user's path
    output_dir = os.path.join(os.path.dirname(script_dir), "Analyze Summary") # Define output directory
    os.makedirs(output_dir, exist_ok=True) # Ensure the output directory exists
    
    # Define a list of directories to process, along with their analysis type
    # These paths are relative to base_raw_data_dir
    # This list can be easily extended for future additions
    directories_to_process = [
        {"path": "Data Performance/5G AUTO DP", "analysis_type": "data_performance"},
        {"path": "Data Performance/5G NSA DP", "analysis_type": "data_performance"},
        {"path": "5G VoNR MRAB Stationary", "analysis_type": "mrab_performance"}, # Add MRAB directory
        {"path": "TestInvalid", "analysis_type": "data_performance"}, # Add the new test directory
        {"path": "Call Performance", "analysis_type": "call_performance"}, # Add Call Performance directory
        {"path": "Voice Quality", "analysis_type": "voice_quality"}, # Add Voice Quality directory
        {"path": "Voice Quality", "analysis_type": "audio_delay"}, # Add Audio Delay directory, using the same base path
        {"path": "Coverage Performance", "analysis_type": "coverage_coordinate"}, # Add Coverage Coordinate directory
        {"path": "Coverage Performance/5G n41 HPUE Coverage Test", "analysis_type": "n41_coverage"}, # Add N41 Coverage directory
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
    # This will now also include Voice Quality CSVs, but they won't be processed in the main loop
    # Define analysis types that are handled at the directory level and should not have individual CSVs processed in the main loop
    excluded_analysis_types_for_individual_csvs = [
        "call_performance",
        "voice_quality",
        "audio_delay",
        "coverage_coordinate",
        "n41_coverage" # Add n41_coverage to excluded list
    ]

    # Get all CSV file paths using the new data_path_reader script, excluding those handled separately
    all_csv_files_processed = data_path_reader.get_csv_file_paths(
        base_raw_data_dir, 
        directories_to_process, 
        excluded_analysis_types=excluded_analysis_types_for_individual_csvs
    )

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
                    mrab_analysis_results, _, _ = mrab_statistics.analyze_grouped_intervals(mrab_intervals) # Unpack and get only the results
                    if mrab_analysis_results:
                        all_file_stats["MRAB Statistics"] = mrab_analysis_results
                else:
                    print(f"No MRAB intervals found or an error occurred for: {csv_file_path}")
            
            # Add Call Performance statistics collection
            elif params["analysis_type_detected"] == "call_performance":
                # For call performance, we analyze the entire directory, not individual files here.
                # This block will be skipped for individual CSVs, and handled after the loop.
                pass
            # Voice Quality analysis will also be handled after the loop, so skip here
            elif params["analysis_type_detected"] == "voice_quality":
                pass

            # Determine if the file is invalid: it's invalid if no statistical data was collected
            statistical_keys = ["Throughput", "Jitter", "Error Ratio", "Web Page Load Time", "Ping RTT", "MRAB Statistics"]
            has_any_statistical_data = False
            for key in statistical_keys:
                if key in all_file_stats and all_file_stats[key]: # Check if key exists and its value (the dict) is not empty
                    has_any_statistical_data = True
                    break
            
            if not has_any_statistical_data and params["analysis_type_detected"] not in ["call_performance", "voice_quality"]: # Don't mark call_performance or voice_quality files as invalid here
                current_file_has_invalid_data = True
        
        if current_file_has_invalid_data:
            invalid_data_files.append(csv_file_path)
            print(f"Invalid data detected or analysis skipped for: {csv_file_path}. File will remain in its original location.")
        else:
            valid_data_files.append(csv_file_path)
            print(f"Valid data detected for: {csv_file_path}. Added to valid_data_files.")
        
        # Construct the hierarchical path for the JSON output
        if all_file_stats and params["analysis_type_detected"] not in ["call_performance", "voice_quality"]: # Only insert if stats were successfully collected and not call_performance or voice_quality
            relative_path = os.path.relpath(csv_file_path, base_raw_data_dir)
            path_components = relative_path.replace("\\", "/").split('/') # Use forward slashes for consistency
            
            # The last component is the filename, remove .csv extension
            filename_without_ext = os.path.splitext(path_components[-1])[0]
            path_components[-1] = filename_without_ext
            
            _insert_into_nested_dict(all_collected_results, path_components, all_file_stats)
    
    # After processing all individual CSVs, handle directory-level analyses
    for directory_info in directories_to_process:
        if directory_info["analysis_type"] == "call_performance":
            call_performance_path = os.path.join(base_raw_data_dir, directory_info["path"])
            if os.path.isdir(call_performance_path):
                print(f"\n--- Starting Call Performance analysis for directory: {call_performance_path} ---")
                
                # Iterate through subdirectories within the main Call Performance directory
                for sub_dir_name in os.listdir(call_performance_path):
                    sub_dir_full_path = os.path.join(call_performance_path, sub_dir_name)
                    
                    if os.path.isdir(sub_dir_full_path):
                        # Check for DUT and REF subdirectories within the current sub_dir_full_path
                        dut_call_path = os.path.join(sub_dir_full_path, 'DUT')
                        ref_call_path = os.path.join(sub_dir_full_path, 'REF')

                        if os.path.isdir(dut_call_path) or os.path.isdir(ref_call_path):
                            print(f"\n--- Analyzing Call Performance data in: {sub_dir_full_path} ---")
                            call_results_for_subdir = {}

                            if os.path.isdir(dut_call_path):
                                print(f"Analyzing DUT call data in: {dut_call_path}")
                                dut_call_results = analyze_directory(dut_call_path)
                                if dut_call_results:
                                    call_results_for_subdir['DUT'] = dut_call_results
                            else:
                                print(f"Warning: DUT directory not found for Call Performance at {dut_call_path}")

                            if os.path.isdir(ref_call_path):
                                print(f"Analyzing REF call data in: {ref_call_path}")
                                ref_call_results = analyze_directory(ref_call_path)
                                if ref_call_results:
                                    call_results_for_subdir['REF'] = ref_call_results
                            else:
                                print(f"Warning: REF directory not found for Call Performance at {ref_call_path}")

                            if call_results_for_subdir:
                                # Calculate p-values for aggregated results if both DUT and REF data are available
                                if 'DUT' in call_results_for_subdir and 'REF' in call_results_for_subdir:
                                    dut_res = call_results_for_subdir['DUT']
                                    ref_res = call_results_for_subdir['REF']

                                    # Initiation P-value
                                    _, initiation_p_value = _calculate_fisher_exact_criteria(
                                        dut_res['total_initiation_failures'], dut_res['total_attempts'] - dut_res['total_initiation_failures'],
                                        ref_res['total_initiation_failures'], ref_res['total_attempts'] - ref_res['total_initiation_failures'],
                                        criteria_type="MO/MT"
                                    )
                                    if initiation_p_value is not None:
                                        call_results_for_subdir['initiation_p_value'] = initiation_p_value

                                    # Retention P-value
                                    _, retention_p_value = _calculate_fisher_exact_criteria(
                                        dut_res['total_retention_failures'], dut_res['total_initiation_successes'],
                                        ref_res['total_retention_failures'], ref_res['total_initiation_successes'],
                                        criteria_type="MO"
                                    )
                                    if retention_p_value is not None:
                                        call_results_for_subdir['retention_p_value'] = retention_p_value

                                # Insert results under the specific subdirectory's name
                                _insert_into_nested_dict(all_collected_results, [directory_info["path"], sub_dir_name], call_results_for_subdir)
                                print(f"Call Performance analysis for {sub_dir_name} completed and added to results.")
                            else:
                                print(f"No call performance data collected for {sub_dir_name}.")
                        else:
                            print(f"Skipping directory {sub_dir_name}: No 'DUT' or 'REF' subdirectories found.")
            else:
                print(f"Warning: Call Performance directory not found at {call_performance_path}. Skipping analysis.")
        
        elif directory_info["analysis_type"] == "voice_quality":
            voice_quality_path = os.path.join(base_raw_data_dir, directory_info["path"])
            if os.path.isdir(voice_quality_path):
                print(f"\n--- Starting Voice Quality analysis for directory: {voice_quality_path} ---")
                # Pass the subdir_filter to process_directory
                voice_quality_results = analyze_voice_quality_directory(voice_quality_path, subdir_filter="VQ")
                print(f"Raw voice_quality_results: {voice_quality_results}") # Debug print
                
                if voice_quality_results:
                    # Organize results by subdirectory and then by device type
                    organized_vq_results = {}
                    for file_stats in voice_quality_results:
                        # Extract the subdirectory name from the file_path
                        # Example: Raw Data/Voice Quality/5G Auto VoNR Enabled AMR NB VQ/DUT1.csv
                        # We want "5G Auto VoNR Enabled AMR NB VQ"
                        relative_path_to_vq_dir = os.path.relpath(file_stats["file_path"], voice_quality_path)
                        
                        # Handle cases where the file is directly in the voice_quality_path
                        if os.sep not in relative_path_to_vq_dir:
                            # If the file is directly in the voice_quality_path, use its parent directory name
                            # which is the voice_quality_path itself, or a more generic name like "Root"
                            sub_dir_name = os.path.basename(voice_quality_path)
                        else:
                            sub_dir_name = relative_path_to_vq_dir.split(os.sep)[0] # Get the first directory after voice_quality_path

                        if sub_dir_name not in organized_vq_results:
                            organized_vq_results[sub_dir_name] = {}
                        
                        # Use device_type (DUT1, DUT2, REF) as keys under the subdirectory
                        organized_vq_results[sub_dir_name][file_stats["device_type"]] = {
                            "ul_mos_stats": file_stats["ul_mos_stats"],
                            "dl_mos_stats": file_stats["dl_mos_stats"]
                        }
                    
                    print(f"Organized VQ Results before insertion: {organized_vq_results}") # Debug print
                    _insert_into_nested_dict(all_collected_results, [directory_info["path"]], organized_vq_results)
                    print(f"Voice Quality analysis for {voice_quality_path} completed and added to results.")
                    print(f"All collected results after VQ insertion: {all_collected_results.get(directory_info['path'])}") # Debug print
                else:
                    print(f"No voice quality data collected for {voice_quality_path}.")
            else:
                print(f"Warning: Voice Quality directory not found at {voice_quality_path}. Skipping analysis.")
        
        elif directory_info["analysis_type"] == "audio_delay":
            audio_delay_path = os.path.join(base_raw_data_dir, directory_info["path"])
            print(f"Debug: Checking audio_delay_path: {audio_delay_path}, exists: {os.path.isdir(audio_delay_path)}")
            if os.path.isdir(audio_delay_path):
                print(f"\n--- Starting Audio Delay analysis for directory: {audio_delay_path} ---")
                # Pass the subdir_filter to process_directory
                audio_delay_results = analyze_audio_delay_directory(audio_delay_path, subdir_filter="Audio Delay")
                print(f"Debug: Raw audio_delay_results: {audio_delay_results}") # Debug print
                
                if audio_delay_results:
                    # Organize results by subdirectory
                    organized_ad_results = {}
                    for file_stats in audio_delay_results:
                        # Extract the subdirectory name from the file_path
                        relative_path_to_ad_dir = os.path.relpath(file_stats["file_path"], audio_delay_path)
                        
                        if os.sep not in relative_path_to_ad_dir:
                            sub_dir_name = os.path.basename(audio_delay_path)
                        else:
                            sub_dir_name = relative_path_to_ad_dir.split(os.sep)[0]

                        if sub_dir_name not in organized_ad_results:
                            organized_ad_results[sub_dir_name] = {} # Change to dictionary for device types
                        
                        # Use device_type (DUT1, DUT2, REF1, REF2) as keys under the subdirectory
                        organized_ad_results[sub_dir_name][file_stats["device_type"]] = {
                            "mean": file_stats["mean"],
                            "std_dev": file_stats["std_dev"],
                            "min": file_stats["min"],
                            "max": file_stats["max"],
                            "occurrences": file_stats["occurrences"]
                        }
                    
                    print(f"Debug: Organized AD Results before insertion: {organized_ad_results}") # Debug print
                    _insert_into_nested_dict(all_collected_results, [directory_info["path"], "Audio Delay"], organized_ad_results)
                    print(f"Debug: all_collected_results after AD insertion: {all_collected_results.get(directory_info['path'])}") # Debug print
                    print(f"Audio Delay analysis for {audio_delay_path} completed and added to results.")
                else:
                    print(f"No audio delay data collected for {audio_delay_path}.")
            else:
                print(f"Warning: Audio Delay directory not found at {audio_delay_path}. Skipping analysis.")
        
        elif directory_info["analysis_type"] == "coverage_coordinate":
            # The user specified the target directory as D:\Fit4Launch\Raw Data\Coverage Performance\5G VoNR Coverage Test
            base_coverage_test_path = os.path.join(base_raw_data_dir, "Coverage Performance", "5G VoNR Coverage Test")
            
            if os.path.isdir(base_coverage_test_path):
                print(f"\n--- Starting Coverage Coordinate analysis for base directory: {base_coverage_test_path} ---")
                
                # Assuming subfolders like n25, n41, n71 directly under 5G VoNR Coverage Test
                subfolders = [f.name for f in os.scandir(base_coverage_test_path) if f.is_dir()]

                coverage_comparisons = {}

                for subfolder in subfolders:
                    subfolder_path = os.path.join(base_coverage_test_path, subfolder)
                    print(f"Analyzing subfolder: {subfolder_path}")
                    
                    paired_files = find_dut_ref_files(subfolder_path)
                    
                    if not paired_files:
                        print(f"No DUT/REF pairs found in {subfolder_path}")
                        continue

                    subfolder_comparison_results = {"DUT": {}, "REF": {}}
                    # Regex to extract Run number from filenames like DUTx_RunY.csv
                    run_pattern = re.compile(r"(DUT|REF)\d+_Run(\d+)\.csv", re.IGNORECASE)

                    for dut_file, ref_file in paired_files:
                        print(f"Processing DUT: {os.path.basename(dut_file)} and REF: {os.path.basename(ref_file)}")
                        dut_results = analyze_coverage_coordinates(dut_file)
                        ref_results = analyze_coverage_coordinates(ref_file)
                        
                        # Extract run number for structuring JSON
                        dut_match = run_pattern.match(os.path.basename(dut_file))
                        ref_match = run_pattern.match(os.path.basename(ref_file))
                        
                        run_name = "UnknownRun"
                        if dut_match:
                            run_name = f"Run{int(dut_match.group(2))}"
                        elif ref_match: # Fallback if only ref_file matches (shouldn't happen with paired_files)
                            run_name = f"Run{int(ref_match.group(2))}"

                        subfolder_comparison_results["DUT"][run_name] = dut_results
                        subfolder_comparison_results["REF"][run_name] = ref_results
                        
                        # Print comparison summary to console
                        file_pair_name = f"{os.path.basename(dut_file).replace('.csv', '')}_vs_{os.path.basename(ref_file).replace('.csv', '')}"
                        compare_analysis_results(dut_results, ref_results, file_pair_name) 

                    coverage_comparisons[subfolder] = subfolder_comparison_results
                
                # Insert the structured comparison results into all_collected_results
                # Path components: ['Coverage Performance', '5G VoNR Coverage Test']
                _insert_into_nested_dict(all_collected_results, ["Coverage Performance", "5G VoNR Coverage Test"], coverage_comparisons)
                print(f"Coverage Coordinate analysis for {base_coverage_test_path} completed and added to results.")
            else:
                print(f"Warning: Coverage base directory not found at {base_coverage_test_path}. Skipping analysis.")
        
        elif directory_info["analysis_type"] == "n41_coverage":
            n41_base_path = os.path.join(base_raw_data_dir, directory_info["path"])
            if os.path.isdir(n41_base_path):
                print(f"\n--- Starting N41 Coverage analysis for directory: {n41_base_path} ---")
                
                # The analyze_n41_coverage function expects a folder path containing CSVs
                # The directory_info["path"] is "Coverage Performance/5G n41 HPUE Coverage Test"
                # We need to iterate through Run1, Run2, etc.
                
                n41_coverage_results_by_run = {}
                
                # List subdirectories (Run1, Run2, etc.)
                for run_folder_name in os.listdir(n41_base_path):
                    run_folder_path = os.path.join(n41_base_path, run_folder_name)
                    if os.path.isdir(run_folder_path) and run_folder_name.startswith("Run"):
                        print(f"Analyzing n41 coverage data in: {run_folder_path}")
                        n41_results = analyze_n41_coverage(run_folder_path)
                        
                        if n41_results:
                            n41_coverage_results_by_run[run_folder_name] = n41_results
                            print(f"Found {len(n41_results)} n41 coverage points for {run_folder_name}.")
                        else:
                            print(f"No n41 coverage results found for {run_folder_name}.")
                
                if n41_coverage_results_by_run:
                    _insert_into_nested_dict(all_collected_results, ["Coverage Performance", "5G n41 HPUE Coverage Test"], n41_coverage_results_by_run)
                    print(f"N41 Coverage analysis for {n41_base_path} completed and added to results.")
                else:
                    print(f"No N41 Coverage data collected for {n41_base_path}.")
            else:
                print(f"Warning: N41 Coverage directory not found at {n41_base_path}. Skipping analysis.")

    # After all other analyses, extract RSRP and Tx Power to CSV
    rsrp_output_folder = os.path.join(scripts_parent_dir, "React", "frontend", "public", "rsrp_data")
    tx_power_output_folder = os.path.join(scripts_parent_dir, "React", "frontend", "public", "tx_power_data")
    
    os.makedirs(rsrp_output_folder, exist_ok=True) # Ensure the RSRP output directory exists
    os.makedirs(tx_power_output_folder, exist_ok=True) # Ensure the Tx Power output directory exists

    n41_hpue_coverage_test_path = os.path.join(base_raw_data_dir, "Coverage Performance", "5G n41 HPUE Coverage Test")
    if os.path.isdir(n41_hpue_coverage_test_path):
        print(f"\n--- Starting RSRP and Tx Power extraction for directory: {n41_hpue_coverage_test_path} ---")
        for run_folder_name in os.listdir(n41_hpue_coverage_test_path):
            run_folder_path = os.path.join(n41_hpue_coverage_test_path, run_folder_name)
            if os.path.isdir(run_folder_path) and run_folder_name.startswith("Run"):
                print(f"Extracting RSRP for {run_folder_name}...")
                extract_coverage_data_to_csv(
                    folder_path=run_folder_path,
                    output_folder=rsrp_output_folder,
                    device_type_filters=['PC2', 'PC3'],
                    data_column_name='[NR5G] [RF] RSRP',
                    output_suffix='RSRP_Analysis'
                )
                
                print(f"Extracting Tx Power for {run_folder_name}...")
                extract_coverage_data_to_csv(
                    folder_path=run_folder_path,
                    output_folder=tx_power_output_folder,
                    device_type_filters=['PC2', 'PC3'],
                    data_column_name='[NR5G] [Power] Tx power (Total Actual)',
                    output_suffix='TxPower_Analysis'
                )
    else:
        print(f"Warning: 5G n41 HPUE Coverage Test directory not found at {n41_hpue_coverage_test_path}. Skipping RSRP and Tx Power extraction.")

    # Write the collected list of CSV files to a TXT file using the new data_path_reader script
    # Note: all_csv_files_processed only contains paths for data_performance and mrab_performance.
    # Call performance and Voice Quality files are handled by their respective directory analyzers.
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
