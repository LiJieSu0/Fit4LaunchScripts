import pandas as pd
import sys

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
    
    print(f"\n--- Statistical Analysis of Average Throughputs for {column_name} ---")
    print(f"Mean of Averages: {mean_val:.2f} Mbps")
    print(f"Standard Deviation of Averages: {std_dev_val:.2f} Mbps")
    print(f"Minimum of Averages: {min_val:.2f} Mbps")
    print(f"Maximum of Averages: {max_val:.2f} Mbps")
    
    return stats

def analyze_data_throughput(file_path, throughput_col_name, start_event_str, end_event_str):
    """
    Reads a data throughput CSV file, identifies intervals based on start/end event markers,
    calculates average throughput for each, and then performs statistics on these averages.
    """
    try:
        data = pd.read_csv(file_path)
        print(f"Successfully loaded {file_path}")

        event_column = "[Call Test] [HTTP Transfer] HTTP Transfer Call Event"
        # No explicit time or index column, will use row index for filtering

        if throughput_col_name not in data.columns:
            print(f"\nError: Throughput column '{throughput_col_name}' not found in the CSV file.")
            return
        if event_column not in data.columns:
            print(f"\nError: Event column '{event_column}' not found in the CSV file.")
            return
        
        filtered_data = data.copy()

        # Find 'Started' and 'Ended' events based on the event_column and provided strings
        started_indices = filtered_data[filtered_data[event_column].astype(str).str.contains(start_event_str, na=False)].index
        ended_indices = filtered_data[filtered_data[event_column].astype(str).str.contains(end_event_str, na=False)].index

        if started_indices.empty or ended_indices.empty:
            print(f"\nWarning: Could not find both '{start_event_str}' and '{end_event_str}' events in '{event_column}'. Cannot calculate interval averages.")
            print("Proceeding with full dataset for throughput analysis (this will calculate overall statistics, not statistics of averages).")
            overall_throughput_data = filtered_data[throughput_col_name].dropna()
            _calculate_statistics(overall_throughput_data, throughput_col_name)
            return
        
        interval_averages = []
        current_start_idx = -1

        # Iterate through the data to find 'Started' and 'Ended' pairs
        for i in range(len(filtered_data)):
            event = str(filtered_data.loc[i, event_column])
            
            if start_event_str in event:
                current_start_idx = i
            elif end_event_str in event and current_start_idx != -1:
                end_idx = i
                
                # Extract data for this interval
                interval_data = filtered_data.loc[current_start_idx : end_idx, throughput_col_name].dropna()
                
                if not interval_data.empty:
                    interval_avg = interval_data.mean()
                    interval_averages.append(interval_avg)
                    print(f"Interval from row {current_start_idx} to {end_idx}: Average Throughput = {interval_avg:.2f} Mbps")
                else:
                    print(f"Interval from row {current_start_idx} to {end_idx}: No valid throughput data.")
                
                current_start_idx = -1 # Reset for the next interval

        if not interval_averages:
            print(f"\nNo valid '{start_event_str}' to '{end_event_str}' intervals with throughput data found.")
            return

        # Convert the list of averages to a pandas Series for statistical calculation
        averages_series = pd.Series(interval_averages)
        
        print(f"\nNumber of intervals with valid average throughputs: {len(averages_series)}")
        
        _calculate_statistics(averages_series, throughput_col_name)

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        
        # Determine analysis type from filename
        file_name = file_path.lower()
        throughput_col = None
        start_event = None
        end_event = None
        analysis_type_detected = None

        if "ul" in file_name:
            analysis_type_detected = "UL"
            throughput_col = "[LTE] [Data Throughput] [Uplink (All)] [PUSCH] PUSCH TP (Total)"
            start_event = "Upload Started"
            end_event = "Upload Ended"
        elif "dl" in file_name:
            analysis_type_detected = "DL"
            throughput_col = "[LTE] [Data Throughput] [Downlink (All)] [PDSCH] PDSCH TP (Total)"
            start_event = "Download Started"
            end_event = "Download Ended"
        else:
            print("Could not determine analysis type (UL/DL) from the filename.")
            print("Please ensure 'UL' or 'DL' is present in the file path.")
            print("Usage: python Scripts/DataPerformance/data_performance_statics.py <path_to_your_csv_file>")
            sys.exit(1)
        
        print(f"\nDetected analysis type: {analysis_type_detected} based on filename.")
        analyze_data_throughput(file_path, throughput_col, start_event, end_event)
    else:
        print("Please provide the path to the CSV file as a command-line argument.")
        print("Usage: python Scripts/DataPerformance/data_performance_statics.py <path_to_your_csv_file>")
        sys.exit(1)
