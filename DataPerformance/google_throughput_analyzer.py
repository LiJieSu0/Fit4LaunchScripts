# This script will analyze a CSV file to calculate average throughput in specific intervals.
# The intervals are defined by a start condition (>2M throughput) and an end condition (three consecutive <2M throughput values).

import pandas as pd
import argparse

def analyze_throughput(file_path):
    """
    Analyzes a CSV file for PDSCH Throughput, identifies intervals,
    calculates average throughput for each interval, and then the overall average.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        float: The overall average of all interval averages, or None if no data/intervals found.
    """
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

    # Define the column name for PDSCH Throughput
    throughput_column = '[NR5G] [(NR + LTE)] [Throughput] PDSCH TP'

    if throughput_column not in df.columns:
        print(f"Error: Column '{throughput_column}' not found in the CSV file.")
        return None

    print(f"DEBUG: Analyzing file: {file_path}")
    throughput_data = df[throughput_column].dropna().tolist()
    print(f"DEBUG: Raw throughput_data length: {len(throughput_data)}")
    
    # Convert throughput data to numeric, handling potential non-numeric values
    numeric_throughput_data = []
    for x in throughput_data:
        try:
            numeric_throughput_data.append(float(x))
        except ValueError:
            # Skip non-numeric values
            continue
    print(f"DEBUG: Numeric throughput_data length: {len(numeric_throughput_data)}")
    print(f"DEBUG: First 20 numeric throughput values: {numeric_throughput_data[:20]}")
    print(f"DEBUG: Last 20 numeric throughput values: {numeric_throughput_data[-20:]}")

    if not numeric_throughput_data:
        print("No valid numeric throughput data found.")
        return None

    interval_averages = []
    in_interval = False
    current_interval_data = []
    consecutive_low_count = 0
    threshold = 2.0 # Assuming 2 Mbps as the threshold based on user feedback and image

    for i, value in enumerate(numeric_throughput_data):
        if not in_interval:
            if value > threshold:
                in_interval = True
                current_interval_data.append(value)
                consecutive_low_count = 0 # Reset count when a new interval starts
        else: # Currently in an interval
            current_interval_data.append(value)
            if value < threshold:
                consecutive_low_count += 1
            else:
                consecutive_low_count = 0 # Reset if value is >= threshold

            # Check for end of interval condition (3 consecutive values < threshold)
            if consecutive_low_count >= 3:
                # The interval ends at the value *before* the three consecutive low values.
                # So, remove the last three values from current_interval_data
                if len(current_interval_data) > 3:
                    interval_to_average = current_interval_data[:-3]
                    if interval_to_average:
                        interval_averages.append(sum(interval_to_average) / len(interval_to_average))
                elif len(current_interval_data) > 0: # Handle cases where interval is very short
                    interval_to_average = current_interval_data[:-consecutive_low_count]
                    if interval_to_average:
                        interval_averages.append(sum(interval_to_average) / len(interval_to_average))
                
                in_interval = False
                current_interval_data = []
                consecutive_low_count = 0

    # Handle any remaining data if an interval was open at the end of the file
    if in_interval and current_interval_data:
        # If the last part of the data was an open interval, average what's there
        # We don't have 3 consecutive low values to end it, so we average all of it.
        interval_averages.append(sum(current_interval_data) / len(current_interval_data))

    print(f"DEBUG: Final interval_averages: {interval_averages}")

    if interval_averages:
        overall_average = sum(interval_averages) / len(interval_averages)
        print(f"Individual interval averages: {interval_averages}")
        print(f"Overall average of all interval averages: {overall_average}")
        return {"overall_average": overall_average, "interval_averages": interval_averages}
    else:
        # Fallback: If no valid intervals are found, calculate the average of all non-zero throughput values
        non_zero_throughput = [val for val in numeric_throughput_data if val > 0]
        print(f"DEBUG: Non-zero throughput for fallback: {non_zero_throughput[:20]}...")
        if non_zero_throughput:
            overall_average = sum(non_zero_throughput) / len(non_zero_throughput)
            print("No valid intervals found using the defined criteria. Calculating overall average of all non-zero throughput values as a fallback.")
            print(f"Fallback overall average throughput: {overall_average}")
            return {"overall_average": overall_average, "interval_averages": []} # Return empty list for individual averages
        else:
            print("No valid intervals found and no non-zero throughput data to calculate a fallback average.")
            return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze PDSCH Throughput from a CSV file.")
    parser.add_argument("file_path", type=str, help="The path to the CSV file to analyze.")
    args = parser.parse_args()

    print(f"Analyzing throughput for file: {args.file_path}")
    analyze_throughput(args.file_path)
