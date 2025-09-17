import pandas as pd
import sys
import argparse

def _calculate_statistics(data_series, column_name):
    """
    Calculates statistical data for a given pandas Series.
    Returns a dictionary of statistics.
    """
    if data_series.empty:
        print(f"\nNo valid data found to calculate statistics for '{column_name}'.")
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
    
    print(f"\n--- Statistical Analysis of Average {column_name} ---")
    print(f"Mean of Averages: {mean_val:.2f}")
    print(f"Standard Deviation of Averages: {std_dev_val:.2f}")
    print(f"Minimum of Averages: {min_val:.2f}")
    print(f"Maximum of Averages: {max_val:.2f}")
    
    return stats

def analyze_data_throughput(file_path, column_name_to_analyze, event_col_name, start_event_str, end_event_str):
    """
    Reads a data throughput CSV file, identifies intervals based on start/end event markers,
    calculates average for each, and then performs statistics on these averages.
    """
    try:
        data = pd.read_csv(file_path)
        print(f"Successfully loaded {file_path}")

        if column_name_to_analyze not in data.columns:
            print(f"\nError: Column '{column_name_to_analyze}' not found in the CSV file.")
            return
        if event_col_name not in data.columns:
            print(f"\nError: Event column '{event_col_name}' not found in the CSV file.")
            return
        
        filtered_data = data.copy()

        started_indices = filtered_data[filtered_data[event_col_name].astype(str).str.contains(start_event_str, na=False)].index
        ended_indices = filtered_data[filtered_data[event_col_name].astype(str).str.contains(end_event_str, na=False)].index

        if started_indices.empty or ended_indices.empty:
            print(f"\nWarning: Could not find both '{start_event_str}' and '{end_event_str}' events in '{event_col_name}'. Cannot calculate interval averages.")
            print(f"Proceeding with full dataset for {column_name_to_analyze} analysis (this will calculate overall statistics, not statistics of averages).")
            overall_data = filtered_data[column_name_to_analyze].dropna()
            if column_name_to_analyze == "[Call Test] [iPerf] [Throughput] DL Jitter":
                if not overall_data.empty:
                    mean_val = overall_data.mean()
                    print(f"\n--- Statistical Analysis of Overall {column_name_to_analyze} ---")
                    print(f"Mean: {mean_val:.2f}")
                else:
                    print(f"\nNo valid data found to calculate mean for '{column_name_to_analyze}'.")
            else:
                _calculate_statistics(overall_data, column_name_to_analyze)
            return
        
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
                    # Add unit based on column name
                    unit = "Mbps" if "Throughput" in column_name_to_analyze else "" # Default unit
                    if "Jitter" in column_name_to_analyze:
                        unit = "ms" # Assuming Jitter is in milliseconds
                    
                    # Conditional print for intervals
                    if column_name_to_analyze != "[Call Test] [iPerf] [Throughput] DL Jitter":
                        print(f"Interval from row {current_start_idx} to {end_idx}: Average {column_name_to_analyze} = {interval_avg:.2f} {unit}")
                else:
                    if column_name_to_analyze != "[Call Test] [iPerf] [Throughput] DL Jitter":
                        print(f"Interval from row {current_start_idx} to {end_idx}: No valid {column_name_to_analyze} data.")
                
                current_start_idx = -1 # Reset for the next interval

        if not interval_averages:
            print(f"\nNo valid '{start_event_str}' to '{end_event_str}' intervals with {column_name_to_analyze} data found.")
            return

        averages_series = pd.Series(interval_averages)
        
        # Conditional print for number of intervals
        if column_name_to_analyze != "[Call Test] [iPerf] [Throughput] DL Jitter":
            print(f"\nNumber of intervals with valid average {column_name_to_analyze}: {len(averages_series)}")
        
        if column_name_to_analyze == "[Call Test] [iPerf] [Throughput] DL Jitter":
            if not averages_series.empty:
                mean_val = averages_series.mean()
                print(f"\n--- Statistical Analysis of Average {column_name_to_analyze} ---")
                print(f"Mean of Averages: {mean_val:.2f} ms") # Assuming Jitter is in milliseconds
            else:
                print(f"\nNo valid data found to calculate mean for '{column_name_to_analyze}'.")
        else:
            _calculate_statistics(averages_series, column_name_to_analyze)

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze data performance statistics from a CSV file.")
    parser.add_argument("file_path", help="Path to the CSV file.")
    args = parser.parse_args()
    file_path = args.file_path

    # Determine analysis direction from filename
    file_name = file_path.lower()
    event_col = None
    start_event = None
    end_event = None
    analysis_direction_detected = None

    if "ul" in file_name:
        analysis_direction_detected = "UL"
    elif "dl" in file_name:
        analysis_direction_detected = "DL"
    else:
        print("Could not determine analysis direction (UL/DL) from the filename.")
        print("Please ensure 'UL' or 'DL' is present in the file path.")
        sys.exit(1)
    
    # Determine protocol type from filename
    protocol_type_detected = None
    if "http" in file_name:
        protocol_type_detected = "HTTP"
    elif "udp" in file_name:
        protocol_type_detected = "UDP"
    else:
        print("Could not determine protocol type (HTTP/UDP) from the filename.")
        print("Please ensure 'HTTP' or 'UDP' is present in the file path.")
        sys.exit(1)

    print(f"\nDetected analysis direction: {analysis_direction_detected}, and protocol type: {protocol_type_detected}.")

    if protocol_type_detected == "HTTP":
        event_col = "[Call Test] [HTTP Transfer] HTTP Transfer Call Event"
        if analysis_direction_detected == "DL":
            column_to_analyze = "[LTE] [Data Throughput] [Downlink (All)] [PDSCH] PDSCH TP (Total)"
            start_event = "Download Started"
            end_event = "Download Ended"
            analyze_data_throughput(file_path, column_to_analyze, event_col, start_event, end_event)
        elif analysis_direction_detected == "UL":
            column_to_analyze = "[LTE] [Data Throughput] [Uplink (All)] [PUSCH] PUSCH TP (Total)"
            start_event = "Upload Started"
            end_event = "Upload Ended"
            analyze_data_throughput(file_path, column_to_analyze, event_col, start_event, end_event)
    elif protocol_type_detected == "UDP":
        event_col = "[Event] [Data call test detail events] IPERF Call Event"
        start_event = "IPERF_T_Start"
        end_event = "IPERF_T_End"

        if analysis_direction_detected == "DL":
            # Analyze Throughput
            column_to_analyze_throughput = "[LTE] [Data Throughput] [Downlink (All)] [PDSCH] PDSCH TP (Total)"
            print(f"\n--- Performing Throughput Analysis for {analysis_direction_detected} UDP ---")
            analyze_data_throughput(file_path, column_to_analyze_throughput, event_col, start_event, end_event)

            # Analyze Jitter
            column_to_analyze_jitter = "[Call Test] [iPerf] [Throughput] DL Jitter"
            print(f"\n--- Performing Jitter Analysis for {analysis_direction_detected} UDP ---")
            analyze_data_throughput(file_path, column_to_analyze_jitter, event_col, start_event, end_event)
        elif analysis_direction_detected == "UL":
            # For UL UDP, only throughput is requested
            column_to_analyze = "[LTE] [Data Throughput] [Uplink (All)] [PUSCH] PUSCH TP (Total)"
            print(f"\n--- Performing Throughput Analysis for {analysis_direction_detected} UDP ---")
            analyze_data_throughput(file_path, column_to_analyze, event_col, start_event, end_event)
