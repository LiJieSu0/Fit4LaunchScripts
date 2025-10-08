import pandas as pd
import sys
import argparse
import os
import re

def _clean_header(header):
    """
    Removes content within square brackets (tags) and strips leading/trailing whitespace from a header string.
    """
    # Remove content within square brackets, including the brackets themselves
    cleaned_header = re.sub(r'\[.*?\]', '', header)
    # Strip leading/trailing whitespace
    return cleaned_header.strip()

def _determine_analysis_parameters(file_path):
    """
    Determines analysis parameters (direction, protocol, network, device, column names, event strings)
    from the filename.
    Returns a dictionary of parameters or None if essential parameters cannot be determined.
    """
    file_name = os.path.basename(file_path).lower()
    dir_name = os.path.basename(os.path.dirname(file_path)).lower() # Get parent directory name
    
    file_name = os.path.basename(file_path).lower()
    # Get the directory name of the file, then its parent directory name
    # This is to correctly identify the "drive" context which is usually one level up from the specific test type directory
    current_file_dir = os.path.dirname(file_path)
    parent_dir_of_file_dir = os.path.basename(os.path.dirname(current_file_dir)).lower()
    
    print(f"DEBUG: _determine_analysis_parameters - file_path: {file_path}")
    print(f"DEBUG: _determine_analysis_parameters - file_name (from basename): {file_name}")
    print(f"DEBUG: _determine_analysis_parameters - parent_dir_of_file_dir: {parent_dir_of_file_dir}")

    params = {
        "event_col": None,
        "event_col_fallback": None, # Added for fallback event column
        "start_event": None,
        "end_event": None,
        "analysis_direction_detected": None,
        "protocol_type_detected": None,
        "network_type_detected": None,
        "device_type_detected": "Unknown",
        "analysis_type_detected": "Unknown", # Added for analysis type
        "column_to_analyze_throughput": None,
        "column_to_analyze_throughput_fallback": None, # Added for fallback throughput column
        "column_to_analyze_throughput_third_fallback": None, # Added for third fallback throughput column
        "column_to_analyze_jitter": None,
        "column_to_analyze_error_ratio": None,
        "column_to_analyze_ul_jitter": None,
        "column_to_analyze_ul_error_ratio": None,
        "column_to_analyze_ping_rtt": None, # Added for Ping RTT
        "is_drive_path": False, # Added to indicate if path contains "drive"
    }

    # Determine if it's a "drive" path based on the full file path
    if "drive" in file_path.lower():
        params["is_drive_path"] = True

    # Determine analysis direction from filename
    if "download" in file_name:
        params["analysis_direction_detected"] = "DL"
    elif "upload" in file_name:
        params["analysis_direction_detected"] = "UL"
    elif "dl" in file_name: # Fallback for "dl" if "download" not found
        params["analysis_direction_detected"] = "DL"
    elif "ul" in file_name: # Fallback for "ul" if "upload" not found
        params["analysis_direction_detected"] = "UL"
    
    # Determine protocol type from filename
    if "web page" in file_name:
        params["protocol_type_detected"] = "WEB_PAGE"
    elif "http" in file_name:
        params["protocol_type_detected"] = "HTTP"
    elif "udp" in file_name:
        params["protocol_type_detected"] = "UDP"
    elif "ping" in file_name: # Detect PING protocol
        params["protocol_type_detected"] = "PING"
    
    # Determine network type (5G/LTE) from the full file path
    file_path_lower = file_path.lower()
    if "5g nsa" in file_path_lower:
        params["network_type_detected"] = "5G NSA"
    elif "5g sa" in file_path_lower:
        params["network_type_detected"] = "5G SA"
    elif "5g" in file_path_lower:
        params["network_type_detected"] = "5G" # Generic 5G if SA/NSA not specified
    elif "lte" in file_path_lower:
        params["network_type_detected"] = "LTE"

    # Determine analysis type based on directory name
    if "5g vonr mrab stationary" in file_path_lower:
        params["analysis_type_detected"] = "mrab_performance"
    elif "5g auto dp" in file_path_lower or "5g nsa dp" in file_path_lower:
        params["analysis_type_detected"] = "data_performance"
    elif "5g n41 hpue coverage test" in file_path_lower:
        params["analysis_type_detected"] = "n41_coverage"
    elif "coverage" in file_path_lower: # Generic condition for other coverage analysis
        params["analysis_type_detected"] = "coverage_coordinate"

    print(f"DEBUG: _determine_analysis_parameters - 'dut' in file_name: {'dut' in file_name}")
    print(f"DEBUG: _determine_analysis_parameters - 'ref' in file_name: {'ref' in file_name}")

    device_type_match = re.search(r'(DUT|REF|PC\d+)', file_name, re.IGNORECASE) # Modified regex to match DUT/REF without digits
    if device_type_match:
        params["device_type_detected"] = device_type_match.group(0).upper() # Convert to uppercase for consistency
    else:
        params["device_type_detected"] = "Unknown" # Default to Unknown if no match

    print(f"DEBUG: _determine_analysis_parameters - device_type_detected (after logic): {params['device_type_detected']}")
    print(f"DEBUG: _determine_analysis_parameters - is_drive_path: {params['is_drive_path']}")

    # If essential parameters are not detected, return None
    # For WEB_PAGE, analysis_direction_detected is not strictly necessary as it's a single metric
    # For PING, analysis_direction_detected is not strictly necessary as it's a single metric (RTT)
    # For MRAB, protocol_type_detected and analysis_direction_detected are not strictly necessary as it's a specific analysis
    if params["analysis_type_detected"] == "mrab_performance":
        # Only need network type and device type for MRAB
        if not params["network_type_detected"] or not params["device_type_detected"]:
            return None
    elif params["protocol_type_detected"] not in ["WEB_PAGE", "PING"] and (not params["analysis_direction_detected"] or not params["protocol_type_detected"] or not params["network_type_detected"]):
        return None
    elif params["protocol_type_detected"] == "WEB_PAGE" and (not params["protocol_type_detected"] or not params["network_type_detected"]):
        return None
    elif params["protocol_type_detected"] == "PING" and (not params["protocol_type_detected"] or not params["network_type_detected"]):
        return None
    elif params["analysis_type_detected"] == "coverage_coordinate":
        # For coverage, only need device type
        if not params["device_type_detected"]:
            return None


    if params["protocol_type_detected"] == "HTTP":
        params["event_col"] = _clean_header("[Call Test] [HTTP Transfer] HTTP Transfer Call Event")
        if params["analysis_direction_detected"] == "DL":
            params["start_event"] = "Download Started"
            params["end_event"] = "Download Ended"
            if params["network_type_detected"] in ["5G", "5G NSA", "5G SA"]:
                params["column_to_analyze_throughput"] = _clean_header("[Call Test] [Throughput] Application DL TP")
                params["column_to_analyze_throughput_fallback"] = _clean_header("[NR5G] [(NR + LTE)] [Throughput] PDSCH TP") # Fallback for 5G DL HTTP
                params["column_to_analyze_throughput_third_fallback"] = _clean_header("DL TP (excl. slow start)") # Third fallback for 5G DL HTTP
            else: # LTE
                params["column_to_analyze_throughput"] = _clean_header("[LTE] [Data Throughput] [Downlink (All)] [PDSCH] PDSCH TP (Total)")
                params["column_to_analyze_throughput_third_fallback"] = _clean_header("DL TP (excl. slow start)") # Third fallback for LTE DL HTTP
        elif params["analysis_direction_detected"] == "UL":
            params["start_event"] = "Upload Started"
            params["end_event"] = "Upload Ended"
            if params["network_type_detected"] in ["5G", "5G NSA", "5G SA"]:
                params["column_to_analyze_throughput"] = _clean_header("[Call Test] [Throughput] Application UL TP")
                params["column_to_analyze_throughput_fallback"] = _clean_header("[NR5G] [(NR + LTE)] [Throughput] PUSCH TP") # Fallback for 5G UL HTTP
                params["column_to_analyze_throughput_third_fallback"] = _clean_header("UL Avg TP") # Third fallback for 5G UL HTTP
            else: # LTE
                params["column_to_analyze_throughput"] = _clean_header("[LTE] [Data Throughput] [Uplink (All)] [PUSCH] PUSCH TP (Total)")
                params["column_to_analyze_throughput_third_fallback"] = _clean_header("UL Avg TP") # Third fallback for LTE UL HTTP
    elif params["protocol_type_detected"] == "UDP":
        params["event_col"] = _clean_header("[Event][Data call test detail events]IPERF Call Event") # Primary event column
        params["event_col_fallback"] = _clean_header("[Event] [Data call test detail events] IPERF Call Event") # Fallback event column
        params["start_event"] = "IPERF_T_Start"
        params["end_event"] = "IPERF_T_End"

        if params["analysis_direction_detected"] == "DL":
            params["column_to_analyze_throughput"] = _clean_header("[Call Test] [Throughput] Application DL TP") if params["network_type_detected"] in ["5G", "5G NSA", "5G SA"] else _clean_header("[LTE] [Data Throughput] [Downlink (All)] [PDSCH] PDSCH TP (Total)")
            params["column_to_analyze_throughput_fallback"] = _clean_header("[NR5G] [(NR + LTE)] [Throughput] PDSCH TP") # Added fallback for 5G DL UDP
            params["column_to_analyze_throughput_third_fallback"] = _clean_header("DL TP (excl. slow start)") # Third fallback for DL UDP
            params["column_to_analyze_jitter"] = _clean_header("[Call Test] [iPerf] [Throughput] DL Jitter")
            params["column_to_analyze_error_ratio"] = _clean_header("[Call Test] [iPerf] [Throughput] DL Error Ratio")
        elif params["analysis_direction_detected"] == "UL":
            params["column_to_analyze_throughput"] = _clean_header("[Call Test] [Throughput] Application UL TP") # Primary UL Throughput
            params["column_to_analyze_throughput_fallback"] = _clean_header("[NR5G] [Throughput] PUSCH TP") # Fallback UL Throughput
            params["column_to_analyze_throughput_third_fallback"] = _clean_header("UL Avg TP") # Third fallback for UL Throughput
            params["column_to_analyze_ul_jitter"] = _clean_header("[Call Test] [iPerf] [Call Average] [Jitter and Error] UL Jitter")
            params["column_to_analyze_ul_error_ratio"] = _clean_header("[Call Test] [iPerf] [Call Average] [Jitter and Error] UL Error Ratio")
    elif params["protocol_type_detected"] == "WEB_PAGE":
        params["event_col"] = _clean_header("[Event] [Data call test detail events] HTTP Call Event")
        params["start_event"] = "HTTP Traffic Start"
        params["end_event"] = "HTTP Traffic End"
        params["column_to_analyze_total_duration"] = _clean_header("[Call Test] [HTTP] Total duration")
    elif params["protocol_type_detected"] == "PING":
        params["event_col"] = _clean_header("[Event] [Data call test detail events] Ping Call Event")
        params["start_event"] = "PING Traffic Start"
        params["end_event"] = "PING Traffic End"
        params["column_to_analyze_ping_rtt"] = _clean_header("[Call Test] [PING] [RTT] RTT")
    print(f"DEBUG: _determine_analysis_parameters returning: {params}")
    return params

def _find_related_ping_file(current_file_path, device_type):
    """
    Attempts to find a related PING CSV file by searching within the 'Raw Data' directory.
    """
    # Assuming 'Raw Data' is at the root of the current working directory
    raw_data_root = "Raw Data" 
    
    if not os.path.isdir(raw_data_root):
        print(f"Error: '{raw_data_root}' directory not found at the project root.")
        return None

    device_type_lower = device_type.lower()

    for root, _, files in os.walk(raw_data_root):
        for f in files:
            file_lower = f.lower()
            # Check if it's a CSV, contains "ping" in the filename, and matches the device type
            if file_lower.endswith(".csv") and "ping" in file_lower and device_type_lower in file_lower:
                return os.path.join(root, f)
    return None

def _calculate_statistics(data_series, column_name):
    """
    Calculates statistical data for a given pandas Series.
    Returns a dictionary of statistics.
    """
    if data_series.empty:
        # print(f"\nNo valid data found to calculate statistics for '{column_name}'.")
        return {} # Return empty dict instead of None
    
    mean_val = data_series.mean()
    std_dev_val = data_series.std()
    min_val = data_series.min()
    max_val = data_series.max()
    
    stats = {
        "Mean": mean_val,
        "Standard Deviation": std_dev_val,
        "Minimum": min_val,
        "Maximum": max_val
    }
    
    return stats

def analyze_throughput(file_path, column_name_to_analyze, event_col_name, start_event_str, end_event_str, fallback_column_name=None, fallback_event_col_name=None, third_fallback_column_name=None):
    num_intervals = 0 # Initialize interval count
    """
    Reads a data CSV file, identifies intervals based on start/end event markers,
    calculates average throughput for each, and then performs full statistics on these averages.
    Returns a dictionary of statistics or None.
    """
    try:
        data = pd.read_csv(file_path)
        # Apply the cleaning function to all column names in the DataFrame
        data.columns = [_clean_header(col) for col in data.columns]
        # print(f"Successfully loaded {file_path}")

        # The column names to analyze are already cleaned by _determine_analysis_parameters
        # No need to strip or clean them again here.
        
        current_column_to_use = column_name_to_analyze
        
        # Check primary column
        if current_column_to_use in data.columns and not data[current_column_to_use].dropna().empty:
            pass # Primary column is good
        else:
            # Primary column is not good, try fallbacks
            if fallback_column_name in data.columns and not data[fallback_column_name].dropna().empty:
                print(f"Warning: Primary throughput column '{current_column_to_use}' is empty or not found. Using fallback column '{fallback_column_name}'.")
                current_column_to_use = fallback_column_name
            elif third_fallback_column_name in data.columns and not data[third_fallback_column_name].dropna().empty:
                print(f"Warning: Primary throughput column '{column_name_to_analyze}' and first fallback '{fallback_column_name}' are empty or not found. Using third fallback column '{third_fallback_column_name}'.")
                current_column_to_use = third_fallback_column_name
            else:
                print(f"Error: Primary throughput column '{column_name_to_analyze}' is empty or not found, and fallback column '{fallback_column_name}' is also empty or not found, and third fallback '{third_fallback_column_name}' is also empty or not found.")
                print(f"Available columns: {data.columns.tolist()}")
                return {} # Return empty dict instead of None
        
        # Check if primary event column exists, otherwise try fallback
        current_event_col_to_use = event_col_name
        if current_event_col_to_use not in data.columns:
            if fallback_event_col_name:
                if fallback_event_col_name in data.columns:
                    print(f"Warning: Primary event column '{current_event_col_to_use}' not found. Using fallback event column '{fallback_event_col_name}'.")
                    current_event_col_to_use = fallback_event_col_name
                else:
                    print(f"\nError: Primary event column '{current_event_col_to_use}' not found, and fallback event column '{fallback_event_col_name}' is also not found.")
                    print(f"Available columns: {data.columns.tolist()}")
                    return {} # Return empty dict instead of None
            else:
                print(f"\nError: Event column '{current_event_col_to_use}' not found in the CSV file, and no fallback event column was provided.")
                print(f"Available columns: {data.columns.tolist()}")
                return {} # Return empty dict instead of None
        
        # print(f"Attempting to analyze with column: '{current_column_to_use}' and event column: '{current_event_col_to_use}'") # Removed as per user request
        # print(f"Looking for start event: '{start_event_str}' and end event: '{end_event_str}'") # Removed as per user request

        filtered_data = data.copy()

        started_indices = filtered_data[filtered_data[current_event_col_to_use].astype(str).str.contains(start_event_str, na=False)].index
        ended_indices = filtered_data[filtered_data[current_event_col_to_use].astype(str).str.contains(end_event_str, na=False)].index

        if started_indices.empty or ended_indices.empty:
            print(f"\nWarning: Could not find both '{start_event_str}' and '{end_event_str}' events in '{current_event_col_to_use}'. Cannot calculate interval averages.")
            # print(f"Started indices empty: {started_indices.empty}, Ended indices empty: {ended_indices.empty}") # Removed as per user request
            print(f"Proceeding with full dataset for {current_column_to_use} analysis (this will calculate overall statistics, not statistics of averages).")
            overall_data = filtered_data[current_column_to_use].dropna()
            if overall_data.empty:
                print(f"Warning: No valid data in '{current_column_to_use}' even for overall statistics.")
            stats_result = _calculate_statistics(overall_data, current_column_to_use)
            return stats_result if stats_result is not None else {} # Ensure empty dict if _calculate_statistics returns None
        
        # print(f"Found {len(started_indices)} start events and {len(ended_indices)} end events.") # Removed as per user request

        interval_averages = []
        current_start_idx = -1

        for i in range(len(filtered_data)):
            event = str(filtered_data.loc[i, current_event_col_to_use])
            
            if start_event_str in event:
                current_start_idx = i
            elif end_event_str in event and current_start_idx != -1:
                end_idx = i
                
                interval_data = filtered_data.loc[current_start_idx : end_idx, current_column_to_use].dropna()
                
                if not interval_data.empty:
                    interval_avg = interval_data.mean()
                    interval_averages.append(interval_avg)
                # else:
                    # print(f"Interval from row {current_start_idx} to {end_idx}: No valid {current_column_to_use} data.") # Removed as per user request
                
                current_start_idx = -1 # Reset for the next interval

        if not interval_averages:
            # print(f"\nNo valid '{start_event_str}' to '{end_event_str}' intervals with {current_column_to_use} data found.") # Removed as per user request
            
            # Implement user's requested fallback logic
            overall_data_for_sum = filtered_data[current_column_to_use].dropna()
            
            # If overall_data_for_sum has more than 20 entries, take only the last 20
            if len(overall_data_for_sum) > 20:
                overall_data_for_sum = overall_data_for_sum.tail(20)
                print(f"Warning: Overall data for sum exceeded 20 rows. Using last 20 rows for calculation.")

            num_intervals_detected = len(started_indices) # Use the count of detected start events

            if not overall_data_for_sum.empty and num_intervals_detected > 0:
                # Calculate full statistics for the overall data
                stats = _calculate_statistics(overall_data_for_sum, current_column_to_use)
                if stats:
                    # Add the calculated mean (sum / intervals) and other info
                    total_sum = overall_data_for_sum.sum()
                    # If num_intervals_detected is based on the full dataset, and overall_data_for_sum is sliced,
                    # the mean calculation might be skewed. The request says "從最後20組的Row開始計算總和，而不是整Column計算"
                    # and "輸出統計的組數假如超過20組，也只計算最後20組".
                    # This implies that if we are taking the sum of the last 20 rows, the "number of intervals"
                    # for the mean calculation should also be based on these 20 rows, or the number of actual intervals
                    # found within these 20 rows. For simplicity and to align with "last 20 rows",
                    # I will use the count of the sliced `overall_data_for_sum` for the mean divisor.
                    calculated_mean = total_sum / len(overall_data_for_sum) if len(overall_data_for_sum) > 0 else 0
                    stats["Mean"] = calculated_mean # Override mean with the requested calculation
                    stats["Number of Intervals"] = len(overall_data_for_sum) # Reflect the number of rows used for sum
                    stats["Note"] = "Calculated overall sum divided by number of detected intervals due to no valid interval data. Limited to last 20 rows if applicable."
                    # print(f"Fallback: Calculated overall stats for '{current_column_to_use}': {stats}") # Removed as per user request
                    return stats
                else:
                    print(f"Warning: Cannot perform fallback calculation: No valid data in column ('{current_column_to_use}' empty: {overall_data_for_sum.empty}) or no intervals detected (num_intervals_detected: {num_intervals_detected}).")
                    print(f"Available columns in file: {data.columns.tolist()}")
                    return {} # Return empty dict instead of None
            else:
                print(f"Warning: Cannot perform fallback calculation: No valid data in column ('{current_column_to_use}' empty: {overall_data_for_sum.empty}) or no intervals detected (num_intervals_detected: {num_intervals_detected}).")
                print(f"Available columns in file: {data.columns.tolist()}")
                return {} # Return empty dict instead of None

        # If interval_averages has more than 20 entries, take only the last 20
        if len(interval_averages) > 20:
            interval_averages = interval_averages[-20:]
            print(f"Warning: Throughput interval groups exceeded 20. Using last 20 groups for statistics.")

        averages_series = pd.Series(interval_averages)
        
        # Get statistics and add interval count
        stats = _calculate_statistics(averages_series, current_column_to_use)
        if stats:
            stats["Number of Intervals"] = len(interval_averages)
        return stats

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return {} # Return empty dict instead of None
    except Exception as e:
        print(f"An error occurred: {e}")
        return {} # Return empty dict instead of None

def analyze_jitter(file_path, column_name_to_analyze, event_col_name, start_event_str, end_event_str, fallback_event_col_name=None):
    """
    Reads a data CSV file and reports the mean of the entire jitter column.
    Returns a dictionary of statistics or None.
    """
    try:
        data = pd.read_csv(file_path)
        # Apply the cleaning function to all column names in the DataFrame
        data.columns = [_clean_header(col) for col in data.columns]
        # print(f"Successfully loaded {file_path}")

        # The column names to analyze are already cleaned by _determine_analysis_parameters
        # No need to strip or clean them again here.

        # Check if primary event column exists, otherwise try fallback
        current_event_col_to_use = event_col_name
        if current_event_col_to_use not in data.columns:
            if fallback_event_col_name:
                if fallback_event_col_name in data.columns:
                    print(f"Warning: Primary event column '{current_event_col_to_use}' not found. Using fallback event column '{fallback_event_col_name}'.")
                    current_event_col_to_use = fallback_event_col_name
                else:
                    print(f"\nError: Primary event column '{current_event_col_to_use}' not found, and fallback event column '{fallback_event_col_name}' is also not found.")
                    print(f"Available columns: {data.columns.tolist()}")
                    return {} # Return empty dict instead of None
            else:
                print(f"\nError: Event column '{current_event_col_to_use}' not found in the CSV file, and no fallback event column was provided.")
                print(f"Available columns: {data.columns.tolist()}")
                return {} # Return empty dict instead of None

        if column_name_to_analyze not in data.columns:
            print(f"\nError: Column '{column_name_to_analyze}' not found in the CSV file.")
            return {} # Return empty dict instead of None
        
        # Calculate mean of the entire column
        overall_jitter_data = data[column_name_to_analyze].dropna()

        if not overall_jitter_data.empty:
            mean_val = overall_jitter_data.mean()
            return {"Mean": mean_val}
        else:
            # print(f"\nNo valid data found to calculate mean for '{column_name_to_analyze_stripped}'.")
            return {} # Return empty dict instead of None

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return {} # Return empty dict instead of None
    except Exception as e:
        print(f"An error occurred: {e}")
        return {} # Return empty dict instead of None

def analyze_error_ratio(file_path, column_name_to_analyze, event_col_name, start_event_str, end_event_str, fallback_event_col_name=None):
    """
    Reads a data CSV file and reports the mean of the entire error ratio column.
    Returns a dictionary of statistics or None.
    """
    try:
        data = pd.read_csv(file_path)
        # Apply the cleaning function to all column names in the DataFrame
        data.columns = [_clean_header(col) for col in data.columns]
        # print(f"Successfully loaded {file_path}")

        # The column names to analyze are already cleaned by _determine_analysis_parameters
        # No need to strip or clean them again here.

        # Check if primary event column exists, otherwise try fallback
        current_event_col_to_use = event_col_name
        if current_event_col_to_use not in data.columns:
            if fallback_event_col_name:
                if fallback_event_col_name in data.columns:
                    print(f"Warning: Primary event column '{current_event_col_to_use}' not found. Using fallback event column '{fallback_event_col_name}'.")
                    current_event_col_to_use = fallback_event_col_name
                else:
                    print(f"\nError: Primary event column '{current_event_col_to_use}' not found, and fallback event column '{fallback_event_col_name}' is also not found.")
                    print(f"Available columns: {data.columns.tolist()}")
                    return {} # Return empty dict instead of None
            else:
                print(f"\nError: Event column '{current_event_col_to_use}' not found in the CSV file, and no fallback event column was provided.")
                print(f"Available columns: {data.columns.tolist()}")
                return {} # Return empty dict instead of None

        if column_name_to_analyze not in data.columns:
            print(f"\nError: Column '{column_name_to_analyze}' not found in the CSV file.")
            return {} # Return empty dict instead of None
        
        # Calculate mean of the entire column
        overall_error_ratio_data = data[column_name_to_analyze].dropna()

        if not overall_error_ratio_data.empty:
            mean_val = overall_error_ratio_data.mean()
            return {"Mean": mean_val}
        else:
            # print(f"\nNo valid data found to calculate statistics for '{column_name_to_analyze_stripped}'.")
            return {} # Return empty dict instead of None

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return {} # Return empty dict instead of None
    except Exception as e:
        print(f"An error occurred: {e}")
        return {} # Return empty dict instead of None

def analyze_web_page_load_time(file_path, event_col_name, start_event_str, end_event_str, duration_col_name, fallback_event_col_name=None):
    """
    Reads a data CSV file, identifies web page load time intervals based on start/end event markers,
    extracts total duration for each, and calculates statistics (count, average, max, min, std dev).
    Returns a dictionary of statistics or None.
    """
    try:
        data = pd.read_csv(file_path)
        # Apply the cleaning function to all column names in the DataFrame
        data.columns = [_clean_header(col) for col in data.columns]

        # The column names to analyze are already cleaned by _determine_analysis_parameters
        # No need to strip or clean them again here.
        
        # Check if primary event column exists, otherwise try fallback
        current_event_col_to_use = event_col_name
        if current_event_col_to_use not in data.columns:
            if fallback_event_col_name:
                if fallback_event_col_name in data.columns:
                    print(f"Warning: Primary event column '{current_event_col_to_use}' not found. Using fallback event column '{fallback_event_col_name}'.")
                    current_event_col_to_use = fallback_event_col_name
                else:
                    print(f"\nError: Primary event column '{current_event_col_to_use}' not found, and fallback event column '{fallback_event_col_name}' is also not found.")
                    print(f"Available columns: {data.columns.tolist()}")
                    return {} # Return empty dict instead of None
            else:
                print(f"\nError: Event column '{current_event_col_to_use}' not found in the CSV file, and no fallback event column was provided.")
                print(f"Available columns: {data.columns.tolist()}")
                return {} # Return empty dict instead of None

        if duration_col_name not in data.columns:
            print(f"\nError: Duration column '{duration_col_name}' not found in the CSV file.")
            print(f"Available columns: {data.columns.tolist()}")
            return {} # Return empty dict instead of None
        
        filtered_data = data.copy()

        started_indices = filtered_data[filtered_data[current_event_col_to_use].astype(str).str.contains(start_event_str, na=False)].index
        ended_indices = filtered_data[filtered_data[current_event_col_to_use].astype(str).str.contains(end_event_str, na=False)].index

        if started_indices.empty or ended_indices.empty:
            print(f"\nWarning: Could not find both '{start_event_str}' and '{end_event_str}' events in '{current_event_col_to_use}'. Cannot calculate web page load time intervals.")
            return {} # Return empty dict instead of None
        
        total_durations = []
        current_start_idx = -1
        
        # Find all start and end event indices
        start_events = filtered_data[filtered_data[current_event_col_to_use].astype(str).str.contains(start_event_str, na=False)].index
        end_events = filtered_data[filtered_data[current_event_col_to_use].astype(str).str.contains(end_event_str, na=False)].index
        timeout_idle_events = filtered_data[filtered_data[current_event_col_to_use].astype(str).str.contains("TIMEOUT_Idle", na=False)].index

        # Match start, end, and then find the duration after TIMEOUT_Idle
        for start_idx in start_events:
            # Find the first end event after this start event
            relevant_end_events = end_events[end_events > start_idx]
            if not relevant_end_events.empty:
                end_idx = relevant_end_events[0]

                # Find the first TIMEOUT_Idle event after this end event
                relevant_timeout_idle = timeout_idle_events[timeout_idle_events > end_idx]
                if not relevant_timeout_idle.empty:
                    timeout_idx = relevant_timeout_idle[0]
                    
                    # The duration value is on the row immediately after TIMEOUT_Idle
                    # Check if timeout_idx + 1 is a valid index
                    if timeout_idx + 1 < len(filtered_data):
                        duration_row_idx = timeout_idx + 1
                        duration_val = filtered_data.loc[duration_row_idx, duration_col_name]
                        
                        if pd.notna(duration_val): # Check if the value is not NaN
                            total_durations.append(duration_val)
        
        if not total_durations:
            print(f"\nNo valid '{start_event_str}' to '{end_event_str}' intervals with '{duration_col_name}' data found after 'TIMEOUT_Idle' events.")
            return {} # Return empty dict instead of None

        durations_series = pd.Series(total_durations)
        
        stats = _calculate_statistics(durations_series, duration_col_name)
        if stats:
            stats["Number of Intervals"] = len(total_durations)
        return stats

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return {} # Return empty dict instead of None
    except Exception as e:
        print(f"An error occurred: {e}")
        return {} # Return empty dict instead of None

def evaluate_performance(dut_value, ref_value, metric_type):
    """
    Evaluates performance based on DUT and REF values for a given metric type.
    Returns one of "Excellent", "Pass", "Marginal Fail", "Fail".
    """
    if ref_value == 0:
        return "Cannot evaluate: Reference value is zero."

    if metric_type == "throughput":
        if dut_value > 1.1 * ref_value:
            return "Excellent"
        elif 0.9 * ref_value <= dut_value <= 1.1 * ref_value:
            return "Pass"
        elif 0.8 * ref_value <= dut_value < 0.9 * ref_value:
            return "Marginal Fail"
        elif dut_value < 0.8 * ref_value:
            return "Fail"
    elif metric_type == "jitter":
        # Jitter criteria (lower is better)
        if dut_value < 0.9 * ref_value:
            return "Excellent"
        elif (0.9 * ref_value <= dut_value <= 1.1 * ref_value) or (dut_value < 10):
            return "Pass"
        elif 1.1 * ref_value < dut_value <= 1.20 * ref_value: # Corrected condition based on clarification
            return "Marginal Fail"
        elif dut_value > 1.20 * ref_value:
            return "Fail"
    elif metric_type == "ping_rtt":
        # Ping RTT criteria (lower is better)
        if dut_value < 0.9 * ref_value:
            return "Excellent"
        elif 0.9 * ref_value <= dut_value <= 1.1 * ref_value:
            return "Pass"
        elif 1.1 * ref_value < dut_value <= 1.20 * ref_value:
            return "Marginal Fail"
        elif dut_value > 1.20 * ref_value:
            return "Fail"
    elif metric_type == "error_ratio":
        # Error Ratio criteria (lower is better)
        # Assuming dut_value is %Packet Loss AVG DUT and ref_value is % Packet Loss AVG REF
        if dut_value < ref_value:
            return "Excellent"
        elif dut_value <= 5.0 or (dut_value - ref_value) <= 10.0:
            return "Pass"
        elif 10.0 < (dut_value - ref_value) <= 20.0:
            return "Marginal Fail"
        elif (dut_value - ref_value) > 20.0:
            return "Fail"
    
    return "Unknown" # Should not happen with the above conditions

import ping_statics # Import ping_statics here to avoid circular dependencies if ping_statics also imports data_performance_statics

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze data performance statistics from a CSV file.")
    parser.add_argument("file_path", help="Path to the CSV file.")
    args = parser.parse_args()
    file_path = args.file_path

    # Determine analysis direction from filename
    # Extract only the filename from the full path
    file_name = os.path.basename(file_path).lower()
    event_col = None
    start_event = None
    end_event = None
    analysis_direction_detected = None

    params = _determine_analysis_parameters(file_path)

    if params is None:
        print(f"Error: Could not determine analysis parameters for {file_path}. Exiting.")
        sys.exit(1)

    print(f"\nDetected protocol type: {params['protocol_type_detected']}, and network type: {params['network_type_detected']}.")
    if params["analysis_direction_detected"]:
        print(f"Detected analysis direction: {params['analysis_direction_detected']}.")

    if params["protocol_type_detected"] == "HTTP":
        if params["analysis_direction_detected"] == "DL":
            print(f"\n--- Performing Throughput Analysis for {params['analysis_direction_detected']} HTTP ---")
            stats = analyze_throughput(file_path, params["column_to_analyze_throughput"], params["event_col"], params["start_event"], params["end_event"], fallback_column_name=params["column_to_analyze_throughput_fallback"], fallback_event_col_name=params["event_col_fallback"])
            print(f"Throughput Stats: {stats}")
            if stats and "Number of Intervals" in stats:
                print(f"Number of Intervals: {stats['Number of Intervals']}")
        elif params["analysis_direction_detected"] == "UL":
            print(f"\n--- Performing Throughput Analysis for {params['analysis_direction_detected']} HTTP ---")
            stats = analyze_throughput(file_path, params["column_to_analyze_throughput"], params["event_col"], params["start_event"], params["end_event"], fallback_column_name=params["column_to_analyze_throughput_fallback"], fallback_event_col_name=params["event_col_fallback"])
            print(f"Throughput Stats: {stats}")
            if stats and "Number of Intervals" in stats:
                print(f"Number of Intervals: {stats['Number of Intervals']}")
    elif params["protocol_type_detected"] == "UDP":
        if params["analysis_direction_detected"] == "DL":
            # Analyze Throughput
            print(f"\n--- Performing Throughput Analysis for {params['analysis_direction_detected']} UDP ---")
            stats = analyze_throughput(file_path, params["column_to_analyze_throughput"], params["event_col"], params["start_event"], params["end_event"], fallback_column_name=params["column_to_analyze_throughput_fallback"], fallback_event_col_name=params["event_col_fallback"])
            print(f"Throughput Stats: {stats}")
            if stats and "Number of Intervals" in stats:
                print(f"Number of Intervals: {stats['Number of Intervals']}")

            # Analyze Jitter
            print(f"\n--- Performing Jitter Analysis for {params['analysis_direction_detected']} UDP ---")
            stats = analyze_jitter(file_path, params["column_to_analyze_jitter"], params["event_col"], params["start_event"], params["end_event"], fallback_event_col_name=params["event_col_fallback"])
            print(f"Jitter Stats: {stats}")

            # Analyze DL Error Ratio
            print(f"\n--- Performing DL Error Ratio Analysis for {params['analysis_direction_detected']} UDP ---")
            stats = analyze_error_ratio(file_path, params["column_to_analyze_error_ratio"], params["event_col"], params["start_event"], params["end_event"], fallback_event_col_name=params["event_col_fallback"])
            print(f"Error Ratio Stats: {stats}")

        elif params["analysis_direction_detected"] == "UL":
            # Analyze Throughput
            print(f"\n--- Performing Throughput Analysis for {params['analysis_direction_detected']} UDP ---")
            stats = analyze_throughput(file_path, params["column_to_analyze_throughput"], params["event_col"], params["start_event"], params["end_event"], fallback_column_name=params["column_to_analyze_throughput_fallback"], fallback_event_col_name=params["event_col_fallback"], third_fallback_column_name=params["column_to_analyze_throughput_third_fallback"])
            print(f"Throughput Stats: {stats}")
            if stats and "Number of Intervals" in stats:
                print(f"Number of Intervals: {stats['Number of Intervals']}")

            # Analyze UL Jitter
            print(f"\n--- Performing UL Jitter Analysis for {params['analysis_direction_detected']} UDP ---")
            stats = analyze_jitter(file_path, params["column_to_analyze_ul_jitter"], params["event_col"], params["start_event"], params["end_event"], fallback_event_col_name=params["event_col_fallback"])
            print(f"Jitter Stats: {stats}")

            # Analyze UL Error Ratio
            print(f"\n--- Performing UL Error Ratio Analysis for {params['analysis_direction_detected']} UDP ---")
            stats = analyze_error_ratio(file_path, params["column_to_analyze_ul_error_ratio"], params["event_col"], params["start_event"], params["end_event"], fallback_event_col_name=params["event_col_fallback"])
            print(f"Error Ratio Stats: {stats}")
    elif params["protocol_type_detected"] == "WEB_PAGE":
        print(f"\n--- Performing Web Page Load Time Analysis ---")
        stats = analyze_web_page_load_time(file_path, params["event_col"], params["start_event"], params["end_event"], params["column_to_analyze_total_duration"], fallback_event_col_name=params["event_col_fallback"])
        print(f"Web Page Load Time Stats: {stats}")
        if stats and "Number of Intervals" in stats:
            print(f"Number of Intervals: {stats['Number of Intervals']}")
    elif params["protocol_type_detected"] == "PING": # This block handles direct PING files
        print(f"\n--- Performing Ping RTT Analysis ---")
        ping_stats = ping_statics.calculate_ping_statistics(file_path, params["device_type_detected"])
        if ping_stats and "Ping RTT" in ping_stats:
            print(f"Ping RTT Mean: {ping_stats['Ping RTT']['avg']:.2f} ms")
            print(f"Ping RTT Min: {ping_stats['Ping RTT']['min']:.2f} ms")
            print(f"Ping RTT Max: {ping_stats['Ping RTT']['max']:.2f} ms")
            print(f"Ping RTT Std Dev: {ping_stats['Ping RTT']['std_dev']:.2f} ms")
        else:
            print("No Ping RTT statistics could be calculated.")

    # Additional Ping RTT analysis for "drive" paths, regardless of primary protocol
    if params["is_drive_path"] and params["protocol_type_detected"] != "PING":
        print(f"DEBUG: Attempting to find related ping file for drive path. is_drive_path: {params['is_drive_path']}, protocol_type_detected: {params['protocol_type_detected']}, device_type_detected: {params['device_type_detected']}")
        related_ping_file = _find_related_ping_file(file_path, params["device_type_detected"])
        if related_ping_file:
            print(f"Found related Ping file: {related_ping_file}")
            ping_stats = ping_statics.calculate_ping_statistics(related_ping_file, params["device_type_detected"])
            if ping_stats and "Ping RTT" in ping_stats:
                print(f"Ping RTT Mean: {ping_stats['Ping RTT']['avg']:.2f} ms")
                print(f"Ping RTT Min: {ping_stats['Ping RTT']['min']:.2f} ms")
                print(f"Ping RTT Max: {ping_stats['Ping RTT']['max']:.2f} ms")
                print(f"Ping RTT Std Dev: {ping_stats['Ping RTT']['std_dev']:.2f} ms")
            else:
                print(f"No Ping RTT statistics could be calculated from {related_ping_file}.")
        else:
            print(f"No related Ping file found for drive path: {file_path}")

    print(f"\nDevice Type: {params['device_type_detected']}")
