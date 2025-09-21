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
    
    params = {
        "event_col": None,
        "start_event": None,
        "end_event": None,
        "analysis_direction_detected": None,
        "protocol_type_detected": None,
        "network_type_detected": None,
        "device_type_detected": "Unknown",
        "column_to_analyze_throughput": None,
        "column_to_analyze_jitter": None,
        "column_to_analyze_error_ratio": None,
        "column_to_analyze_ul_jitter": None,
        "column_to_analyze_ul_error_ratio": None,
    }

    # Determine analysis direction from filename
    if "ul" in file_name:
        params["analysis_direction_detected"] = "UL"
    elif "dl" in file_name:
        params["analysis_direction_detected"] = "DL"
    elif "download" in file_name:
        params["analysis_direction_detected"] = "DL"
    elif "upload" in file_name:
        params["analysis_direction_detected"] = "UL"
    
    # Determine protocol type from filename
    if "http" in file_name:
        params["protocol_type_detected"] = "HTTP"
    elif "udp" in file_name:
        params["protocol_type_detected"] = "UDP"
    
    # Determine network type (5G/LTE) from filename or directory name
    if "5g" in file_name or "5g" in dir_name:
        params["network_type_detected"] = "5G"
    elif "lte" in file_name or "lte" in dir_name:
        params["network_type_detected"] = "LTE"

    if "dut" in file_name:
        params["device_type_detected"] = "DUT"
    elif "ref" in file_name:
        params["device_type_detected"] = "REF"

    # If essential parameters are not detected, return None
    if not params["analysis_direction_detected"] or not params["protocol_type_detected"] or not params["network_type_detected"]:
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
        params["event_col"] = "[Event] [Data call test detail events] IPERF Call Event"
        params["start_event"] = "IPERF_T_Start"
        params["end_event"] = "IPERF_T_End"

        if params["analysis_direction_detected"] == "DL":
            params["column_to_analyze_throughput"] = "[Call Test] [Throughput] Application DL TP" if params["network_type_detected"] == "5G" else "[LTE] [Data Throughput] [Downlink (All)] [PDSCH] PDSCH TP (Total)"
            params["column_to_analyze_jitter"] = "[Call Test] [iPerf] [Throughput] DL Jitter"
            params["column_to_analyze_error_ratio"] = "[Call Test] [iPerf] [Throughput] DL Error Ratio"
        elif params["analysis_direction_detected"] == "UL":
            params["column_to_analyze_throughput"] = "[Call Test] [Throughput] Application UL TP" if params["network_type_detected"] == "5G" else "[LTE] [Data Throughput] [Uplink (All)] [PUSCH] PUSCH TP (Total)"
            params["column_to_analyze_ul_jitter"] = "[Call Test] [iPerf] [Call Average] [Jitter and Error] UL Jitter"
            params["column_to_analyze_ul_error_ratio"] = "[Call Test] [iPerf] [Call Average] [Jitter and Error] UL Error Ratio"
    
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

def analyze_throughput(file_path, column_name_to_analyze, event_col_name, start_event_str, end_event_str):
    num_intervals = 0 # Initialize interval count
    """
    Reads a data CSV file, identifies intervals based on start/end event markers,
    calculates average throughput for each, and then performs full statistics on these averages.
    Returns a dictionary of statistics or None.
    """
    try:
        data = pd.read_csv(file_path)
        # print(f"Successfully loaded {file_path}")

        if column_name_to_analyze not in data.columns:
            print(f"\nError: Column '{column_name_to_analyze}' not found in the CSV file.")
            print(f"Available columns: {data.columns.tolist()}")
            return None
        if event_col_name not in data.columns:
            print(f"\nError: Event column '{event_col_name}' not found in the CSV file.")
            print(f"Available columns: {data.columns.tolist()}")
            return None
        
        # print(f"Attempting to analyze with column: '{column_name_to_analyze}' and event column: '{event_col_name}'") # Removed as per user request
        # print(f"Looking for start event: '{start_event_str}' and end event: '{end_event_str}'") # Removed as per user request

        filtered_data = data.copy()

        started_indices = filtered_data[filtered_data[event_col_name].astype(str).str.contains(start_event_str, na=False)].index
        ended_indices = filtered_data[filtered_data[event_col_name].astype(str).str.contains(end_event_str, na=False)].index

        if started_indices.empty or ended_indices.empty:
            print(f"\nWarning: Could not find both '{start_event_str}' and '{end_event_str}' events in '{event_col_name}'. Cannot calculate interval averages.")
            # print(f"Started indices empty: {started_indices.empty}, Ended indices empty: {ended_indices.empty}") # Removed as per user request
            print(f"Proceeding with full dataset for {column_name_to_analyze} analysis (this will calculate overall statistics, not statistics of averages).")
            overall_data = filtered_data[column_name_to_analyze].dropna()
            if overall_data.empty:
                print(f"Warning: No valid data in '{column_name_to_analyze}' even for overall statistics.")
            return _calculate_statistics(overall_data, column_name_to_analyze)
        
        # print(f"Found {len(started_indices)} start events and {len(ended_indices)} end events.") # Removed as per user request

        interval_averages = []
        current_start_idx = -1

        for i in range(len(filtered_data)):
            event = str(filtered_data.loc[i, event_col_name])
            
            if start_event_str in event:
                current_start_idx = i
            elif end_event_str in event and current_start_idx != -1:
                end_idx = i
                
                interval_data = filtered_data.loc[current_start_idx : end_idx, column_name_to_analyze].dropna()
                
                if not interval_data.empty:
                    interval_avg = interval_data.mean()
                    interval_averages.append(interval_avg)
                # else:
                    # print(f"Interval from row {current_start_idx} to {end_idx}: No valid {column_name_to_analyze} data.") # Removed as per user request
                
                current_start_idx = -1 # Reset for the next interval

        if not interval_averages:
            # print(f"\nNo valid '{start_event_str}' to '{end_event_str}' intervals with {column_name_to_analyze} data found.") # Removed as per user request
            
            # Implement user's requested fallback logic
            overall_data_for_sum = filtered_data[column_name_to_analyze].dropna()
            num_intervals_detected = len(started_indices) # Use the count of detected start events

            if not overall_data_for_sum.empty and num_intervals_detected > 0:
                # Calculate full statistics for the overall data
                stats = _calculate_statistics(overall_data_for_sum, column_name_to_analyze)
                if stats:
                    # Add the calculated mean (sum / intervals) and other info
                    total_sum = overall_data_for_sum.sum()
                    calculated_mean = total_sum / num_intervals_detected
                    stats["Mean"] = calculated_mean # Override mean with the requested calculation
                    stats["Number of Intervals"] = num_intervals_detected
                    stats["Note"] = "Calculated overall sum divided by number of detected intervals due to no valid interval data."
                    # print(f"Fallback: Calculated overall stats for '{column_name_to_analyze}': {stats}") # Removed as per user request
                    return stats
                else:
                    print(f"Warning: Cannot perform fallback calculation: No valid data in column ('{column_name_to_analyze}' empty: {overall_data_for_sum.empty}) or no intervals detected (num_intervals_detected: {num_intervals_detected}).")
                    print(f"Available columns in file: {data.columns.tolist()}")
                    return None
            else:
                print(f"Warning: Cannot perform fallback calculation: No valid data in column ('{column_name_to_analyze}' empty: {overall_data_for_sum.empty}) or no intervals detected (num_intervals_detected: {num_intervals_detected}).")
                print(f"Available columns in file: {data.columns.tolist()}")
                return None # Still return None if no data at all or no intervals to divide by

        averages_series = pd.Series(interval_averages)
        
        # Get statistics and add interval count
        stats = _calculate_statistics(averages_series, column_name_to_analyze)
        if stats:
            stats["Number of Intervals"] = len(interval_averages)
        return stats

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def analyze_jitter(file_path, column_name_to_analyze, event_col_name, start_event_str, end_event_str):
    """
    Reads a data CSV file and reports the mean of the entire jitter column.
    Returns a dictionary of statistics or None.
    """
    try:
        data = pd.read_csv(file_path)
        # print(f"Successfully loaded {file_path}")

        if column_name_to_analyze not in data.columns:
            print(f"\nError: Column '{column_name_to_analyze}' not found in the CSV file.")
            return None
        
        # Calculate mean of the entire column
        overall_jitter_data = data[column_name_to_analyze].dropna()

        if not overall_jitter_data.empty:
            mean_val = overall_jitter_data.mean()
            return {"Mean": mean_val}
        else:
            # print(f"\nNo valid data found to calculate mean for '{column_name_to_analyze}'.")
            return None

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def analyze_error_ratio(file_path, column_name_to_analyze, event_col_name, start_event_str, end_event_str):
    """
    Reads a data CSV file and reports the mean of the entire error ratio column.
    Returns a dictionary of statistics or None.
    """
    try:
        data = pd.read_csv(file_path)
        # print(f"Successfully loaded {file_path}")

        if column_name_to_analyze not in data.columns:
            print(f"\nError: Column '{column_name_to_analyze}' not found in the CSV file.")
            return None
        
        # Calculate mean of the entire column
        overall_error_ratio_data = data[column_name_to_analyze].dropna()

        if not overall_error_ratio_data.empty:
            mean_val = overall_error_ratio_data.mean()
            return {"Mean": mean_val}
        else:
            # print(f"\nNo valid data found to calculate statistics for '{column_name_to_analyze}'.")
            return None

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

    print(f"\nDetected analysis direction: {params['analysis_direction_detected']}, protocol type: {params['protocol_type_detected']}, and network type: {params['network_type_detected']}.")

    if params["protocol_type_detected"] == "HTTP":
        if params["analysis_direction_detected"] == "DL":
            print(f"\n--- Performing Throughput Analysis for {params['analysis_direction_detected']} HTTP ---")
            stats = analyze_throughput(file_path, params["column_to_analyze_throughput"], params["event_col"], params["start_event"], params["end_event"])
            print(f"Throughput Stats: {stats}")
            if stats and "Number of Intervals" in stats:
                print(f"Number of Intervals: {stats['Number of Intervals']}")
        elif params["analysis_direction_detected"] == "UL":
            print(f"\n--- Performing Throughput Analysis for {params['analysis_direction_detected']} HTTP ---")
            stats = analyze_throughput(file_path, params["column_to_analyze_throughput"], params["event_col"], params["start_event"], params["end_event"])
            print(f"Throughput Stats: {stats}")
            if stats and "Number of Intervals" in stats:
                print(f"Number of Intervals: {stats['Number of Intervals']}")
    elif params["protocol_type_detected"] == "UDP":
        if params["analysis_direction_detected"] == "DL":
            # Analyze Throughput
            print(f"\n--- Performing Throughput Analysis for {params['analysis_direction_detected']} UDP ---")
            stats = analyze_throughput(file_path, params["column_to_analyze_throughput"], params["event_col"], params["start_event"], params["end_event"])
            print(f"Throughput Stats: {stats}")
            if stats and "Number of Intervals" in stats:
                print(f"Number of Intervals: {stats['Number of Intervals']}")

            # Analyze Jitter
            print(f"\n--- Performing Jitter Analysis for {params['analysis_direction_detected']} UDP ---")
            stats = analyze_jitter(file_path, params["column_to_analyze_jitter"], params["event_col"], params["start_event"], params["end_event"])
            print(f"Jitter Stats: {stats}")

            # Analyze DL Error Ratio
            print(f"\n--- Performing DL Error Ratio Analysis for {params['analysis_direction_detected']} UDP ---")
            stats = analyze_error_ratio(file_path, params["column_to_analyze_error_ratio"], params["event_col"], params["start_event"], params["end_event"])
            print(f"Error Ratio Stats: {stats}")

        elif params["analysis_direction_detected"] == "UL":
            # Analyze Throughput
            print(f"\n--- Performing Throughput Analysis for {params['analysis_direction_detected']} UDP ---")
            stats = analyze_throughput(file_path, params["column_to_analyze_throughput"], params["event_col"], params["start_event"], params["end_event"])
            print(f"Throughput Stats: {stats}")
            if stats and "Number of Intervals" in stats:
                print(f"Number of Intervals: {stats['Number of Intervals']}")

            # Analyze UL Jitter
            print(f"\n--- Performing UL Jitter Analysis for {params['analysis_direction_detected']} UDP ---")
            stats = analyze_jitter(file_path, params["column_to_analyze_ul_jitter"], params["event_col"], params["start_event"], params["end_event"])
            print(f"Jitter Stats: {stats}")

            # Analyze UL Error Ratio
            print(f"\n--- Performing UL Error Ratio Analysis for {params['analysis_direction_detected']} UDP ---")
            stats = analyze_error_ratio(file_path, params["column_to_analyze_ul_error_ratio"], params["event_col"], params["start_event"], params["end_event"])
            print(f"Error Ratio Stats: {stats}")

    print(f"\nDevice Type: {params['device_type_detected']}")
