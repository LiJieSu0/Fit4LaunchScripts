import os
import subprocess
import sys
import pandas as pd
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

def run_analysis_on_file(file_path):
    """
    Runs the analysis script on a single CSV file and returns the collected statistics.
    """
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
    # analysis_script_path is no longer needed as data_performance_statics is imported directly
    
    base_data_dir = os.path.join("RawData", "DataPerformance") # Updated base directory
    
    if not os.path.isdir(base_data_dir):
        print(f"Error: Base data directory not found at {base_data_dir}")
        sys.exit(1)

    all_collected_results = {}

    # Dynamically discover case directories (e.g., TC91-1, TC94-1)
    case_dirs = [d for d in os.listdir(base_data_dir) if os.path.isdir(os.path.join(base_data_dir, d))]
    
    for case_dir_name in case_dirs:
        full_case_dir_path = os.path.join(base_data_dir, case_dir_name)
        
        # Dynamically discover protocol directories (e.g., HTTP, UDP) within each case directory
        protocol_dirs = [d for d in os.listdir(full_case_dir_path) if os.path.isdir(os.path.join(full_case_dir_path, d))]

        for protocol_dir_name in protocol_dirs:
            full_protocol_dir_path = os.path.join(full_case_dir_path, protocol_dir_name)
            print(f"\n{'='*100}\nProcessing data in: {full_protocol_dir_path}\n{'='*100}")
            
            subdir_results = {}
            for file in os.listdir(full_protocol_dir_path):
                if file.lower().endswith(".csv"):
                    csv_file_path = os.path.join(full_protocol_dir_path, file)
                    print(f"--- Analyzing file: {csv_file_path} ---")
                    stats = run_analysis_on_file(csv_file_path)
                    if stats:
                        device_type = stats.get("Device Type")
                        if device_type:
                            subdir_results[device_type] = stats
            
            # Create a descriptive key for the results (e.g., "TC91-1 - Multi Stream HTTP Download for 30 seconds_Good")
            descriptive_key = f"{case_dir_name} - {protocol_dir_name}"
            all_collected_results[descriptive_key] = subdir_results
        
    if all_collected_results:
        create_pdf_report(all_collected_results)
    else:
        print("No data collected to generate a report.")
