import pandas as pd
import sys
import argparse
import os

def _determine_analysis_parameters(file_path):
    """
    Determines analysis parameters (direction, protocol, network, device, column names, event strings)
    from the filename.
    Returns a dictionary of parameters or None if essential parameters cannot be determined.
    """
    file_name = os.path.basename(file_path).lower()
    dir_name = os.path.basename(os.path.dirname(file_path)).lower() # Get parent directory name
    
    # print(f"DEBUG: file_name: {file_name}") # Removed as per user request
    # print(f"DEBUG: dir_name: {dir_name}") # Removed as per user request

    params = {
        "event_col": None,
        "event_col_fallback": None, # Added for fallback event column
        "start_event": None,
        "end_event": None,
        "analysis_direction_detected": None,
        "protocol_type_detected": None,
        "network_type_detected": None,
        "device_type_detected": "Unknown",
        "column_to_analyze_throughput": None,
        "column_to_analyze_throughput_fallback": None, # Added for fallback throughput column
        "column_to_analyze_jitter": None,
        "column_to_analyze_error_ratio": None,
        "column_to_analyze_ul_jitter": None,
        "column_to_analyze_ul_error_ratio": None,
    }

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
    
    # Determine network type (5G/LTE) from the full file path
    file_path_lower = file_path.lower()
    if "5g" in file_path_lower:
        params["network_type_detected"] = "5G"
    elif "lte" in file_path_lower:
        params["network_type_detected"] = "LTE"

    if "dut" in file_name:
        params["device_type_detected"] = "DUT"
    elif "ref" in file_name:
        params["device_type_detected"] = "REF"

    # If essential parameters are not detected, return None
    # For WEB_PAGE, analysis_direction_detected is not strictly necessary as it's a single metric
    if params["protocol_type_detected"] != "WEB_PAGE" and (not params["analysis_direction_detected"] or not params["protocol_type_detected"] or not params["network_type_detected"]):
        return None
    elif params["protocol_type_detected"] == "WEB_PAGE" and (not params["protocol_type_detected"] or not params["network_type_detected"]):
        return None


    if params["protocol_type_detected"] == "HTTP":
        params["event_col"] = "[Call Test] [HTTP Transfer] HTTP Transfer Call Event"
        if params["analysis_direction_detected"] == "DL":
            params["column_to_analyze_throughput"] = "[Call Test] [Throughput] Application DL TP" if params["network_type_detected"] == "5G" else "[LTE] [Data Throughput] [Downlink (All)] [PDSCH] PDSCH TP (Total)"
            params["start_event"] = "Download Started"
            params["end_event"] = "Download Ended"
        elif params["analysis_direction_detected"] == "UL":
            # Try specific 5G UL TP column first
            if params["network_type_detected"] == "5G":
                params["column_to_analyze_throughput"] = "[Call Test] [Throughput] Application UL TP"
            else: # Fallback for LTE or if 5G specific not found
                params["column_to_analyze_throughput"] = "[LTE] [Data Throughput] [Uplink (All)] [PUSCH] PUSCH TP (Total)"
            
            params["start_event"] = "Upload Started"
            params["end_event"] = "Upload Ended"
    elif params["protocol_type_detected"] == "UDP":
        params["event_col"] = "[Event][Data call test detail events]IPERF Call Event" # Primary event column
        params["event_col_fallback"] = "[Event] [Data call test detail events] IPERF Call Event" # Fallback event column
        params["start_event"] = "IPERF_T_Start"
        params["end_event"] = "IPERF_T_End"

        if params["analysis_direction_detected"] == "DL":
            params["column_to_analyze_throughput"] = "[Call Test] [Throughput] Application DL TP" if params["network_type_detected"] == "5G" else "[LTE] [Data Throughput] [Downlink (All)] [PDSCH] PDSCH TP (Total)"
            params["column_to_analyze_jitter"] = "[Call Test] [iPerf] [Throughput] DL Jitter"
            params["column_to_analyze_error_ratio"] = "[Call Test] [iPerf] [Throughput] DL Error Ratio"
        elif params["analysis_direction_detected"] == "UL":
            params["column_to_analyze_throughput"] = "[Call Test] [Throughput] Application UL TP" # Primary UL Throughput
            params["column_to_analyze_throughput_fallback"] = "[NR5G] [Throughput] PUSCH TP" # Fallback UL Throughput
            params["column_to_analyze_ul_jitter"] = "[Call Test] [iPerf] [Call Average] [Jitter and Error] UL Jitter"
            params["column_to_analyze_ul_error_ratio"] = "[Call Test] [iPerf] [Call Average] [Jitter and Error] UL Error Ratio"
    elif params["protocol_type_detected"] == "WEB_PAGE":
        params["event_col"] = "[Event] [Data call test detail events] HTTP Call Event"
        params["start_event"] = "HTTP Traffic Start"
        params["end_event"] = "HTTP Traffic End"
        params["column_to_analyze_total_duration"] = "[Call Test] [HTTP] Total duration"
    # print(f"DEBUG: _determine_analysis_parameters returning: {params}") # Removed as per user request
    return params

def _calculate_statistics(data_series, column_name):
    """
    Calculates statistical data for a given pandas Series.
    Returns a dictionary of statistics.
    """
    if data_series.empty:
        # print(f"\nNo valid data found to calculate statistics for '{column_name}'.")
        return None
    
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

def analyze_throughput(file_path, column_name_to_analyze, event_col_name, start_event_str, end_event_str, fallback_column_name=None, fallback_event_col_name=None):
    num_intervals = 0 # Initialize interval count
    """
    Reads a data CSV file, identifies intervals based on start/end event markers,
    calculates average throughput for each, and then performs full statistics on these averages.
    Returns a dictionary of statistics or None.
    """
    try:
        data = pd.read_csv(file_path)
        data.columns = data.columns.str.strip() # Strip whitespace from column names
        # print(f"Successfully loaded {file_path}")

        # Strip whitespace from the column names to analyze for robust matching
        column_name_to_analyze_stripped = column_name_to_analyze.strip()
        event_col_name_stripped = event_col_name.strip()
        
        # Check if primary column exists and has data, otherwise try fallback
        current_column_to_use = column_name_to_analyze_stripped
        if current_column_to_use not in data.columns or data[current_column_to_use].dropna().empty:
            if fallback_column_name:
                fallback_column_name_stripped = fallback_column_name.strip()
                if fallback_column_name_stripped in data.columns and not data[fallback_column_name_stripped].dropna().empty:
                    print(f"Warning: Primary throughput column '{current_column_to_use}' is empty or not found. Using fallback column '{fallback_column_name_stripped}'.")
                    current_column_to_use = fallback_column_name_stripped
                else:
                    print(f"Error: Primary throughput column '{current_column_to_use}' is empty or not found, and fallback column '{fallback_column_name_stripped}' is also empty or not found.")
                    print(f"Available columns: {data.columns.tolist()}")
                    return None
            else:
                print(f"\nError: Column '{current_column_to_use}' not found or is empty in the CSV file, and no fallback column was provided.")
                print(f"Available columns: {data.columns.tolist()}")
                return None
        
        # Check if primary event column exists, otherwise try fallback
        current_event_col_to_use = event_col_name_stripped
        if current_event_col_to_use not in data.columns:
            if fallback_event_col_name:
                fallback_event_col_name_stripped = fallback_event_col_name.strip()
                if fallback_event_col_name_stripped in data.columns:
                    print(f"Warning: Primary event column '{current_event_col_to_use}' not found. Using fallback event column '{fallback_event_col_name_stripped}'.")
                    current_event_col_to_use = fallback_event_col_name_stripped
                else:
                    print(f"\nError: Primary event column '{current_event_col_to_use}' not found, and fallback event column '{fallback_event_col_name_stripped}' is also not found.")
                    print(f"Available columns: {data.columns.tolist()}")
                    return None
            else:
                print(f"\nError: Event column '{current_event_col_to_use}' not found in the CSV file, and no fallback event column was provided.")
                print(f"Available columns: {data.columns.tolist()}")
                return None
        
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
            return _calculate_statistics(overall_data, current_column_to_use)
        
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
            num_intervals_detected = len(started_indices) # Use the count of detected start events

            if not overall_data_for_sum.empty and num_intervals_detected > 0:
                # Calculate full statistics for the overall data
                stats = _calculate_statistics(overall_data_for_sum, current_column_to_use)
                if stats:
                    # Add the calculated mean (sum / intervals) and other info
                    total_sum = overall_data_for_sum.sum()
                    calculated_mean = total_sum / num_intervals_detected
                    stats["Mean"] = calculated_mean # Override mean with the requested calculation
                    stats["Number of Intervals"] = num_intervals_detected
                    stats["Note"] = "Calculated overall sum divided by number of detected intervals due to no valid interval data."
                    # print(f"Fallback: Calculated overall stats for '{current_column_to_use}': {stats}") # Removed as per user request
                    return stats
                else:
                    print(f"Warning: Cannot perform fallback calculation: No valid data in column ('{current_column_to_use}' empty: {overall_data_for_sum.empty}) or no intervals detected (num_intervals_detected: {num_intervals_detected}).")
                    print(f"Available columns in file: {data.columns.tolist()}")
                    return None
            else:
                print(f"Warning: Cannot perform fallback calculation: No valid data in column ('{current_column_to_use}' empty: {overall_data_for_sum.empty}) or no intervals detected (num_intervals_detected: {num_intervals_detected}).")
                print(f"Available columns in file: {data.columns.tolist()}")
                return None # Still return None if no data at all or no intervals to divide by

        averages_series = pd.Series(interval_averages)
        
        # Get statistics and add interval count
        stats = _calculate_statistics(averages_series, current_column_to_use)
        if stats:
            stats["Number of Intervals"] = len(interval_averages)
        return stats

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def analyze_jitter(file_path, column_name_to_analyze, event_col_name, start_event_str, end_event_str, fallback_event_col_name=None):
    """
    Reads a data CSV file and reports the mean of the entire jitter column.
    Returns a dictionary of statistics or None.
    """
    try:
        data = pd.read_csv(file_path)
        data.columns = data.columns.str.strip() # Strip whitespace from column names
        # print(f"Successfully loaded {file_path}")

        column_name_to_analyze_stripped = column_name_to_analyze.strip()
        event_col_name_stripped = event_col_name.strip()

        # Check if primary event column exists, otherwise try fallback
        current_event_col_to_use = event_col_name_stripped
        if current_event_col_to_use not in data.columns:
            if fallback_event_col_name:
                fallback_event_col_name_stripped = fallback_event_col_name.strip()
                if fallback_event_col_name_stripped in data.columns:
                    print(f"Warning: Primary event column '{current_event_col_to_use}' not found. Using fallback event column '{fallback_event_col_name_stripped}'.")
                    current_event_col_to_use = fallback_event_col_name_stripped
                else:
                    print(f"\nError: Primary event column '{current_event_col_to_use}' not found, and fallback event column '{fallback_event_col_name_stripped}' is also not found.")
                    print(f"Available columns: {data.columns.tolist()}")
                    return None
            else:
                print(f"\nError: Event column '{current_event_col_to_use}' not found in the CSV file, and no fallback event column was provided.")
                print(f"Available columns: {data.columns.tolist()}")
                return None

        if column_name_to_analyze_stripped not in data.columns:
            print(f"\nError: Column '{column_name_to_analyze_stripped}' not found in the CSV file.")
            return None
        
        # Calculate mean of the entire column
        overall_jitter_data = data[column_name_to_analyze_stripped].dropna()

        if not overall_jitter_data.empty:
            mean_val = overall_jitter_data.mean()
            return {"Mean": mean_val}
        else:
            # print(f"\nNo valid data found to calculate mean for '{column_name_to_analyze_stripped}'.")
            return None

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def analyze_error_ratio(file_path, column_name_to_analyze, event_col_name, start_event_str, end_event_str, fallback_event_col_name=None):
    """
    Reads a data CSV file and reports the mean of the entire error ratio column.
    Returns a dictionary of statistics or None.
    """
    try:
        data = pd.read_csv(file_path)
        data.columns = data.columns.str.strip() # Strip whitespace from column names
        # print(f"Successfully loaded {file_path}")

        column_name_to_analyze_stripped = column_name_to_analyze.strip()
        event_col_name_stripped = event_col_name.strip()

        # Check if primary event column exists, otherwise try fallback
        current_event_col_to_use = event_col_name_stripped
        if current_event_col_to_use not in data.columns:
            if fallback_event_col_name:
                fallback_event_col_name_stripped = fallback_event_col_name.strip()
                if fallback_event_col_name_stripped in data.columns:
                    print(f"Warning: Primary event column '{current_event_col_to_use}' not found. Using fallback event column '{fallback_event_col_name_stripped}'.")
                    current_event_col_to_use = fallback_event_col_name_stripped
                else:
                    print(f"\nError: Primary event column '{current_event_col_to_use}' not found, and fallback event column '{fallback_event_col_name_stripped}' is also not found.")
                    print(f"Available columns: {data.columns.tolist()}")
                    return None
            else:
                print(f"\nError: Event column '{current_event_col_to_use}' not found in the CSV file, and no fallback event column was provided.")
                print(f"Available columns: {data.columns.tolist()}")
                return None

        if column_name_to_analyze_stripped not in data.columns:
            print(f"\nError: Column '{column_name_to_analyze_stripped}' not found in the CSV file.")
            return None
        
        # Calculate mean of the entire column
        overall_error_ratio_data = data[column_name_to_analyze_stripped].dropna()

        if not overall_error_ratio_data.empty:
            mean_val = overall_error_ratio_data.mean()
            return {"Mean": mean_val}
        else:
            # print(f"\nNo valid data found to calculate statistics for '{column_name_to_analyze_stripped}'.")
            return None

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def analyze_web_page_load_time(file_path, event_col_name, start_event_str, end_event_str, duration_col_name, fallback_event_col_name=None):
    """
    Reads a data CSV file, identifies web page load time intervals based on start/end event markers,
    extracts total duration for each, and calculates statistics (count, average, max, min, std dev).
    Returns a dictionary of statistics or None.
    """
    try:
        data = pd.read_csv(file_path)
        data.columns = data.columns.str.strip() # Strip whitespace from column names

        duration_col_name_stripped = duration_col_name.strip()
        event_col_name_stripped = event_col_name.strip()

        # Check if primary event column exists, otherwise try fallback
        current_event_col_to_use = event_col_name_stripped
        if current_event_col_to_use not in data.columns:
            if fallback_event_col_name:
                fallback_event_col_name_stripped = fallback_event_col_name.strip()
                if fallback_event_col_name_stripped in data.columns:
                    print(f"Warning: Primary event column '{current_event_col_to_use}' not found. Using fallback event column '{fallback_event_col_name_stripped}'.")
                    current_event_col_to_use = fallback_event_col_name_stripped
                else:
                    print(f"\nError: Primary event column '{current_event_col_to_use}' not found, and fallback event column '{fallback_event_col_name_stripped}' is also not found.")
                    print(f"Available columns: {data.columns.tolist()}")
                    return None
            else:
                print(f"\nError: Event column '{current_event_col_to_use}' not found in the CSV file, and no fallback event column was provided.")
                print(f"Available columns: {data.columns.tolist()}")
                return None

        if duration_col_name_stripped not in data.columns:
            print(f"\nError: Duration column '{duration_col_name_stripped}' not found in the CSV file.")
            print(f"Available columns: {data.columns.tolist()}")
            return None
        
        filtered_data = data.copy()

        started_indices = filtered_data[filtered_data[current_event_col_to_use].astype(str).str.contains(start_event_str, na=False)].index
        ended_indices = filtered_data[filtered_data[current_event_col_to_use].astype(str).str.contains(end_event_str, na=False)].index

        if started_indices.empty or ended_indices.empty:
            print(f"\nWarning: Could not find both '{start_event_str}' and '{end_event_str}' events in '{current_event_col_to_use}'. Cannot calculate web page load time intervals.")
            return None
        
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
                        duration_val = filtered_data.loc[duration_row_idx, duration_col_name_stripped]
                        
                        if pd.notna(duration_val): # Check if the value is not NaN
                            total_durations.append(duration_val)
        
        if not total_durations:
            print(f"\nNo valid '{start_event_str}' to '{end_event_str}' intervals with '{duration_col_name_stripped}' data found after 'TIMEOUT_Idle' events.")
            return None

        durations_series = pd.Series(total_durations)
        
        stats = _calculate_statistics(durations_series, duration_col_name_stripped)
        if stats:
            stats["Number of Intervals"] = len(total_durations)
        return stats

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

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
            stats = analyze_throughput(file_path, params["column_to_analyze_throughput"], params["event_col"], params["start_event"], params["end_event"], fallback_event_col_name=params["event_col_fallback"])
            print(f"Throughput Stats: {stats}")
            if stats and "Number of Intervals" in stats:
                print(f"Number of Intervals: {stats['Number of Intervals']}")
        elif params["analysis_direction_detected"] == "UL":
            print(f"\n--- Performing Throughput Analysis for {params['analysis_direction_detected']} HTTP ---")
            stats = analyze_throughput(file_path, params["column_to_analyze_throughput"], params["event_col"], params["start_event"], params["end_event"], fallback_event_col_name=params["event_col_fallback"])
            print(f"Throughput Stats: {stats}")
            if stats and "Number of Intervals" in stats:
                print(f"Number of Intervals: {stats['Number of Intervals']}")
    elif params["protocol_type_detected"] == "UDP":
        if params["analysis_direction_detected"] == "DL":
            # Analyze Throughput
            print(f"\n--- Performing Throughput Analysis for {params['analysis_direction_detected']} UDP ---")
            stats = analyze_throughput(file_path, params["column_to_analyze_throughput"], params["event_col"], params["start_event"], params["end_event"], fallback_event_col_name=params["event_col_fallback"])
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
            stats = analyze_throughput(file_path, params["column_to_analyze_throughput"], params["event_col"], params["start_event"], params["end_event"], params["column_to_analyze_throughput_fallback"], fallback_event_col_name=params["event_col_fallback"])
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

    print(f"\nDevice Type: {params['device_type_detected']}")
