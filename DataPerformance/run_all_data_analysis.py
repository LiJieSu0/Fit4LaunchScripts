import os
import subprocess
import sys
import pandas as pd
import json # Import the json module
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch

# Add the current script's directory to sys.path to enable direct imports
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from pdf_report_generator import create_pdf_report # Import the PDF generation function

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
        # Add other directories here as needed, e.g.:
        # {"path": "Call Performance", "analysis_type": "call_performance"},
        # {"path": "Ping", "analysis_type": "ping"},
    ]
    
    all_collected_results = {}
    
    # Get all CSV file paths using the new data_path_reader script
    all_csv_files_processed = data_path_reader.get_csv_file_paths(base_raw_data_dir, directories_to_process)

    # Now iterate through the collected files for analysis
    for csv_file_path in all_csv_files_processed:
        # Determine analysis type based on the file path or configuration if needed
        analysis_type_for_file = "data_performance"
        if "ping" in csv_file_path.lower():
            analysis_type_for_file = "ping"

        stats = None # Initialize stats for each file

        if analysis_type_for_file == "ping":
            print(f"--- Analyzing Ping file: {csv_file_path} ---")
            ping_stats_result = ping_statics.calculate_ping_statistics(csv_file_path)
            if ping_stats_result:
                stats = {"Ping RTT": ping_stats_result}
        else: # data_performance analysis
            params = _determine_analysis_parameters(csv_file_path)

            if params is None:
                file_name = os.path.basename(csv_file_path).lower()
                print(f"Warning: Could not fully determine analysis parameters from filename: {file_name}. Skipping.")
                stats = None # Ensure stats is None if skipping
            else:
                all_file_stats = {}
                all_file_stats["Device Type"] = params["device_type_detected"]
                all_file_stats["Analysis Direction"] = params["analysis_direction_detected"]
                all_file_stats["Protocol Type"] = params["protocol_type_detected"]
                all_file_stats["Network Type"] = params["network_type_detected"]

                if params["protocol_type_detected"] == "HTTP":
                    if params["analysis_direction_detected"] == "DL":
                        throughput_stats = data_performance_statics.analyze_throughput(csv_file_path, params["column_to_analyze_throughput"], params["event_col"], params["start_event"], params["end_event"])
                        if throughput_stats:
                            all_file_stats["Throughput"] = throughput_stats
                    elif params["analysis_direction_detected"] == "UL":
                        throughput_stats = data_performance_statics.analyze_throughput(csv_file_path, params["column_to_analyze_throughput"], params["event_col"], params["start_event"], params["end_event"])
                        if throughput_stats:
                            all_file_stats["Throughput"] = throughput_stats
                elif params["protocol_type_detected"] == "UDP":
                    if params["analysis_direction_detected"] == "DL":
                        throughput_stats = data_performance_statics.analyze_throughput(csv_file_path, params["column_to_analyze_throughput"], params["event_col"], params["start_event"], params["end_event"])
                        if throughput_stats:
                            all_file_stats["Throughput"] = throughput_stats

                        jitter_stats = data_performance_statics.analyze_jitter(csv_file_path, params["column_to_analyze_jitter"], params["event_col"], params["start_event"], params["end_event"])
                        if jitter_stats:
                            all_file_stats["Jitter"] = jitter_stats

                        error_ratio_stats = data_performance_statics.analyze_error_ratio(csv_file_path, params["column_to_analyze_error_ratio"], params["event_col"], params["start_event"], params["end_event"])
                        if error_ratio_stats:
                            all_file_stats["Error Ratio"] = error_ratio_stats

                    elif params["analysis_direction_detected"] == "UL":
                        throughput_stats = data_performance_statics.analyze_throughput(csv_file_path, params["column_to_analyze_throughput"], params["event_col"], params["start_event"], params["end_event"])
                        if throughput_stats:
                            all_file_stats["Throughput"] = throughput_stats

                        jitter_stats = data_performance_statics.analyze_jitter(csv_file_path, params["column_to_analyze_ul_jitter"], params["event_col"], params["start_event"], params["end_event"])
                        if jitter_stats:
                            all_file_stats["Jitter"] = jitter_stats

                        error_ratio_stats = data_performance_statics.analyze_error_ratio(csv_file_path, params["column_to_analyze_ul_error_ratio"], params["event_col"], params["start_event"], params["end_event"])
                        if error_ratio_stats:
                            all_file_stats["Error Ratio"] = error_ratio_stats
                stats = all_file_stats # Assign collected stats to the 'stats' variable
        
        if stats:
            # Determine a descriptive key for the results
            # We need to get the relative path from base_raw_data_dir for the key
            relative_path_from_base = os.path.relpath(os.path.dirname(csv_file_path), base_raw_data_dir)
            key_prefix = f"{analysis_type_for_file.replace('_', ' ').title()} - {relative_path_from_base}" if relative_path_from_base != "." else analysis_type_for_file.replace('_', ' ').title()
            
            device_type = stats.get("Device Type", "Unknown")
            descriptive_key = f"{key_prefix} - {os.path.basename(csv_file_path).replace('.csv', '')}"
            
            # Store results, ensuring unique keys
            if descriptive_key in all_collected_results:
                all_collected_results[f"{descriptive_key} ({device_type})"] = stats
            else:
                all_collected_results[descriptive_key] = stats
    
    # Write the collected list of CSV files to a TXT file using the new data_path_reader script
    data_path_reader.write_csv_paths_with_two_parents(all_csv_files_processed, base_raw_data_dir) # Function name remains, but behavior changed

    if all_collected_results:
        # Output results to a JSON file for the React app
        json_output_path = os.path.join("Scripts", "React", "frontend", "src", "data_analysis_results.json")
        with open(json_output_path, 'w', encoding='utf-8') as f:
            json.dump(all_collected_results, f, ensure_ascii=False, indent=4)
        print(f"\nJSON data generated: {json_output_path}")

        create_pdf_report(all_collected_results)
    else:
        print("No data collected to generate a report.")
