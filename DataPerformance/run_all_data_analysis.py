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
import ping_statics # Import the ping_statics module

def run_analysis_on_file(file_path, analysis_type="data_performance"):
    """
    Runs the analysis script on a single CSV file and returns the collected statistics.
    The analysis_type parameter determines which type of analysis to perform.
    """
    if analysis_type == "ping":
        print(f"--- Analyzing Ping file: {file_path} ---")
        ping_stats = ping_statics.calculate_ping_statistics(file_path)
        if ping_stats:
            return {"Ping RTT": ping_stats}
        return None

    # Existing data performance analysis logic
    file_name = os.path.basename(file_path).lower()
    event_col = None
    start_event = None
    end_event = None
    analysis_direction_detected = None
    protocol_type_detected = None
    network_type_detected = None
    device_type_detected = "Unknown"

    if "ul" in file_name:
        analysis_direction_detected = "UL"
    elif "dl" in file_name:
        analysis_direction_detected = "DL"
    
    if "http" in file_name:
        protocol_type_detected = "HTTP"
    elif "udp" in file_name:
        protocol_type_detected = "UDP"
    
    if "5g" in file_name:
        network_type_detected = "5G"
    elif "lte" in file_name:
        network_type_detected = "LTE"

    if "dut" in file_name:
        device_type_detected = "DUT"
    elif "ref" in file_name:
        device_type_detected = "REF"

    print(f"DEBUG: file_name: {file_name}")
    print(f"DEBUG: analysis_direction_detected: {analysis_direction_detected}")
    print(f"DEBUG: protocol_type_detected: {protocol_type_detected}")
    print(f"DEBUG: network_type_detected: {network_type_detected}")

    if not analysis_direction_detected or not protocol_type_detected or not network_type_detected:
        print(f"Warning: Could not fully determine analysis parameters from filename: {file_name}. Skipping.")
        return None

    all_stats = {}
    all_stats["Device Type"] = device_type_detected
    all_stats["Analysis Direction"] = analysis_direction_detected
    all_stats["Protocol Type"] = protocol_type_detected
    all_stats["Network Type"] = network_type_detected

    if protocol_type_detected == "HTTP":
        event_col = "[Call Test] [HTTP Transfer] HTTP Transfer Call Event"
        if analysis_direction_detected == "DL":
            column_to_analyze = "[Call Test] [Throughput] Application DL TP" if network_type_detected == "5G" else "[LTE] [Data Throughput] [Downlink (All)] [PDSCH] PDSCH TP (Total)"
            start_event = "Download Started"
            end_event = "Download Ended"
            throughput_stats = data_performance_statics.analyze_throughput(file_path, column_to_analyze, event_col, start_event, end_event)
            if throughput_stats:
                all_stats["Throughput"] = throughput_stats
        elif analysis_direction_detected == "UL":
            if network_type_detected == "5G":
                column_to_analyze = "[Call Test] [Throughput] Application UL TP" # Assuming this is the 5G UL TP column
            else: # Default to LTE if not 5G
                column_to_analyze = "[LTE] [Data Throughput] [Uplink (All)] [PUSCH] PUSCH TP (Total)"
            start_event = "Upload Started"
            end_event = "Upload Ended"
            throughput_stats = data_performance_statics.analyze_throughput(file_path, column_to_analyze, event_col, start_event, end_event)
            if throughput_stats:
                all_stats["Throughput"] = throughput_stats
    elif protocol_type_detected == "UDP":
        event_col = "[Event] [Data call test detail events] IPERF Call Event"
        start_event = "IPERF_T_Start"
        end_event = "IPERF_T_End"

        if analysis_direction_detected == "DL":
            column_to_analyze_throughput = "[Call Test] [Throughput] Application DL TP" if network_type_detected == "5G" else "[LTE] [Data Throughput] [Downlink (All)] [PDSCH] PDSCH TP (Total)"
            throughput_stats = data_performance_statics.analyze_throughput(file_path, column_to_analyze_throughput, event_col, start_event, end_event)
            if throughput_stats:
                all_stats["Throughput"] = throughput_stats

            column_to_analyze_jitter = "[Call Test] [iPerf] [Throughput] DL Jitter"
            jitter_stats = data_performance_statics.analyze_jitter(file_path, column_to_analyze_jitter, event_col, start_event, end_event)
            if jitter_stats:
                all_stats["Jitter"] = jitter_stats

            column_to_analyze_dl_error_ratio = "[Call Test] [iPerf] [Throughput] DL Error Ratio"
            error_ratio_stats = data_performance_statics.analyze_error_ratio(file_path, column_to_analyze_dl_error_ratio, event_col, start_event, end_event)
            if error_ratio_stats:
                all_stats["Error Ratio"] = error_ratio_stats

        elif analysis_direction_detected == "UL":
            column_to_analyze_throughput = "[LTE] [Data Throughput] [Uplink (All)] [PUSCH] PUSCH TP (Total)"
            throughput_stats = data_performance_statics.analyze_throughput(file_path, column_to_analyze_throughput, event_col, start_event, end_event)
            if throughput_stats:
                all_stats["Throughput"] = throughput_stats

            column_to_analyze_ul_jitter = "[Call Test] [iPerf] [Call Average] [Jitter and Error] UL Jitter"
            jitter_stats = data_performance_statics.analyze_jitter(file_path, column_to_analyze_ul_jitter, event_col, start_event, end_event)
            if jitter_stats:
                all_stats["Jitter"] = jitter_stats

            column_to_analyze_ul_error_ratio = "[Call Test] [iPerf] [Call Average] [Jitter and Error] UL Error Ratio"
            error_ratio_stats = data_performance_statics.analyze_error_ratio(file_path, column_to_analyze_ul_error_ratio, event_col, start_event, end_event)
            if error_ratio_stats:
                all_stats["Error Ratio"] = error_ratio_stats
    
    return all_stats

    # Removed create_pdf_report function as it's now in pdf_report_generator.py

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    base_raw_data_dir = "Raw Data" # Changed to "Raw Data" as per user's path
    
    # Define a list of directories to process, along with their analysis type
    # This list can be easily extended for future additions
    directories_to_process = [
        {"path": os.path.join(base_raw_data_dir, "5G AUTO DP"), "analysis_type": "data_performance"},
        {"path": os.path.join(base_raw_data_dir, "5G NSA DP"), "analysis_type": "data_performance"},
        # Add other directories here as needed, e.g.:
        # {"path": os.path.join(base_raw_data_dir, "Call Performance"), "analysis_type": "call_performance"},
        # {"path": os.path.join(base_raw_data_dir, "Ping"), "analysis_type": "ping"},
    ]
    
    all_collected_results = {}
    all_csv_files_processed = [] # New list to collect all CSV file paths

    for dir_info in directories_to_process:
        current_dir_path = dir_info["path"]
        analysis_type_for_dir = dir_info["analysis_type"]
        
        if os.path.isdir(current_dir_path):
            print(f"\n{'='*100}\nProcessing {analysis_type_for_dir.replace('_', ' ').title()} data in: {current_dir_path}\n{'='*100}")
            
            # Walk through the directory to find all CSV files recursively
            for root, _, files in os.walk(current_dir_path):
                for file in files:
                    if file.lower().endswith(".csv"):
                        csv_file_path = os.path.join(root, file)
                        all_csv_files_processed.append(csv_file_path) # Collect the file path
                        
                        stats = run_analysis_on_file(csv_file_path, analysis_type=analysis_type_for_dir)
                        
                        if stats:
                            # Determine a descriptive key for the results
                            relative_path = os.path.relpath(root, current_dir_path)
                            key_prefix = f"{analysis_type_for_dir.replace('_', ' ').title()} - {relative_path}" if relative_path != "." else analysis_type_for_dir.replace('_', ' ').title()
                            
                            device_type = stats.get("Device Type", "Unknown")
                            descriptive_key = f"{key_prefix} - {os.path.basename(file).replace('.csv', '')}"
                            
                            # Store results, ensuring unique keys
                            if descriptive_key in all_collected_results:
                                # If key exists, append or merge. For simplicity, let's just overwrite for now
                                # or create a more specific key if needed.
                                # For now, let's make it more specific by including device type in the key
                                all_collected_results[f"{descriptive_key} ({device_type})"] = stats
                            else:
                                all_collected_results[descriptive_key] = stats
        else:
            print(f"Warning: Directory not found at {current_dir_path}. Skipping.")
    
    # Print the collected list of CSV files
    if all_csv_files_processed:
        print("\n--- CSV files with their immediate parent directories: ---")
        # Sort the list for consistent output
        sorted_csv_files = sorted(all_csv_files_processed)
        for csv_file_path in sorted_csv_files:
            file_name = os.path.basename(csv_file_path)
            immediate_parent_dir = os.path.basename(os.path.dirname(csv_file_path))
            grandparent_dir = os.path.basename(os.path.dirname(os.path.dirname(csv_file_path)))
            
            # Construct the path with two parent levels and the filename
            # Handle cases where there might not be two parent levels (e.g., file directly under base_raw_data_dir)
            if grandparent_dir and grandparent_dir != base_raw_data_dir: # Ensure it's not the base "Raw Data" directory itself
                print(f"- {grandparent_dir}\\{immediate_parent_dir}\\{file_name}")
            else:
                print(f"- {immediate_parent_dir}\\{file_name}")
    else:
        print("\nNo CSV files were found in the specified directories.")

    if all_collected_results:
        # Output results to a JSON file for the React app
        json_output_path = os.path.join("Scripts", "React", "frontend", "src", "data_analysis_results.json")
        with open(json_output_path, 'w', encoding='utf-8') as f:
            json.dump(all_collected_results, f, ensure_ascii=False, indent=4)
        print(f"\nJSON data generated: {json_output_path}")

        create_pdf_report(all_collected_results)
    else:
        print("No data collected to generate a report.")
