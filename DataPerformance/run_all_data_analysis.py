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
import data_path_reader # Import the new path reader script

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
        # For now, we'll assume all files from the configured directories are 'data_performance'
        # This part might need more sophisticated logic if different subdirectories require different analysis_types
        analysis_type_for_file = "data_performance" # Default to data_performance for now

        # A more robust way would be to pass the analysis_type from data_path_reader if it were configured per file
        # For simplicity, we'll infer it or use a default.
        # If the original directories_to_process had a more granular type, we'd need to pass that through.
        # For now, let's try to infer from the path if it's a ping file
        if "ping" in csv_file_path.lower():
            analysis_type_for_file = "ping"

        stats = run_analysis_on_file(csv_file_path, analysis_type=analysis_type_for_file)
        
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
    data_path_reader.print_csv_paths_with_two_parents(all_csv_files_processed, base_raw_data_dir) # Function name remains, but behavior changed

    if all_collected_results:
        # Output results to a JSON file for the React app
        json_output_path = os.path.join("Scripts", "React", "frontend", "src", "data_analysis_results.json")
        with open(json_output_path, 'w', encoding='utf-8') as f:
            json.dump(all_collected_results, f, ensure_ascii=False, indent=4)
        print(f"\nJSON data generated: {json_output_path}")

        create_pdf_report(all_collected_results)
    else:
        print("No data collected to generate a report.")
