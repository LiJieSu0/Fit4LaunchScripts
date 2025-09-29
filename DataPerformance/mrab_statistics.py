import csv
import sys
import numpy as np
import json

def extract_intervals_and_values(file_path, header_name, blank_row_threshold=10):
    """
    Extracts discrete intervals, their numerical values, and their line number ranges
    from a specified column of a CSV file.

    An interval is defined by consecutive non-empty rows. If the number of
    consecutive empty rows exceeds `blank_row_threshold`, a new interval begins.

    Args:
        file_path (str): The path to the CSV file.
        header_name (str): The name of the header column to analyze.
        blank_row_threshold (int): The maximum number of consecutive blank rows
                                   allowed within a single interval.

    Returns:
        list: A list of tuples, where each tuple contains (numerical values of an interval,
              (start_line_number, end_line_number)).
              Returns an empty list if an error occurs.
    """
    intervals_data = []
    current_interval_values = []
    current_interval_start_line = -1
    consecutive_blank_rows = 0
    in_interval = False
    line_number = 0

    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)  # Read the header row
            line_number += 1 # Account for header row

            try:
                column_index = headers.index(header_name)
            except ValueError:
                print(f"Error: Header '{header_name}' not found in the CSV file.")
                return []

            for row in reader:
                line_number += 1
                cell_value = ""
                if len(row) > column_index:
                    cell_value = row[column_index].strip()

                try:
                    numeric_value = float(cell_value)
                    # If a numeric value is found
                    if not in_interval:
                        in_interval = True
                        current_interval_values = [] # Start a new interval
                        current_interval_start_line = line_number
                    current_interval_values.append(numeric_value)
                    consecutive_blank_rows = 0 # Reset blank row counter
                except ValueError:
                    # If the cell is blank or non-numeric
                    if in_interval:
                        consecutive_blank_rows += 1
                        if consecutive_blank_rows > blank_row_threshold:
                            if current_interval_values: # Only add if the interval has data
                                # Corrected end_line_number calculation
                                intervals_data.append((current_interval_values, (current_interval_start_line, line_number - consecutive_blank_rows)))
                            in_interval = False
                            current_interval_values = []
                            current_interval_start_line = -1
                            consecutive_blank_rows = 0
            
            # Add the last interval if it was still active
            if in_interval and current_interval_values:
                intervals_data.append((current_interval_values, (current_interval_start_line, line_number)))

        return intervals_data

    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

def analyze_grouped_intervals(all_intervals_with_lines):
    """
    Groups intervals into three sets and calculates statistics for each group,
    based on the sum of values within each interval. Also stores line ranges for debugging.

    Args:
        all_intervals_with_lines (list): A list of tuples, where each tuple contains
                                         (numerical values of an interval, (start_line, end_line)).

    Returns:
        dict: A dictionary containing statistics for each group (Group 0, Group 1, Group 2).
              Each group's statistics include sum, average, max, min, and standard deviation
              of the *interval sums*, and for Group 0, a list of its interval line ranges.
    """
    group_labels = {
        0: "Pre Call",
        1: "In Call",
        2: "Post Call"
    }

    grouped_interval_averages = {
        0: [],  # Averages of intervals where index % 3 == 0
        1: [],  # Averages of intervals where index % 3 == 1
        2: []   # Averages of intervals where index % 3 == 2
    }
    grouped_interval_line_ranges = {
        0: [],
        1: [],
        2: []
    }

    for i, (interval_values, line_range) in enumerate(all_intervals_with_lines):
        if interval_values: # Only calculate average if interval is not empty
            interval_average = np.mean(interval_values)
            group_key = i % 3
            grouped_interval_averages[group_key].append(interval_average)
            grouped_interval_line_ranges[group_key].append(line_range)

    results = {}
    grouped_interval_averages_with_lines = {
        0: [],
        1: [],
        2: []
    }

    for i, (interval_values, line_range) in enumerate(all_intervals_with_lines):
        if interval_values:
            interval_average = np.mean(interval_values)
            group_key = i % 3
            grouped_interval_averages_with_lines[group_key].append((interval_average, line_range))

    for group_key, averages_in_group in grouped_interval_averages.items():
        group_name = group_labels.get(group_key, f"Group {group_key}") # Get the descriptive name
        if not averages_in_group:
            results[group_name] = {
                "Mean": None,
                "Maximum": None,
                "Minimum": None,
                "Standard Deviation": None
            }
            continue

        overall_average = np.mean(averages_in_group)
        maximum_of_averages = np.max(averages_in_group)
        minimum_of_averages = np.min(averages_in_group)
        std_dev_of_averages = np.std(averages_in_group)

        results[group_name] = {
            "Mean": overall_average,
            "Maximum": maximum_of_averages,
            "Minimum": minimum_of_averages,
            "Standard Deviation": std_dev_of_averages
        }
    return results, grouped_interval_line_ranges, grouped_interval_averages_with_lines

def calculate_group_status(dut_mean, ref_mean, group_name):
    """
    Calculates the Mrab Case status for a specific group (Pre Call, In Call, Post Call).

    Args:
        dut_mean (float): Mean throughput for the DUT in the specified group.
        ref_mean (float): Mean throughput for the REF in the specified group.
        group_name (str): The name of the group (e.g., "Pre Call", "In Call", "Post Call").

    Returns:
        str: The Mrab Case status for the group (Excellent, Pass, Marginal Fail, Fail, or error message).
    """
    if ref_mean is None or ref_mean == 0:
        return f"Cannot calculate {group_name} status: Reference Throughput is zero or None."
    if dut_mean is None:
        return f"Cannot calculate {group_name} status: DUT Throughput is None."

    if dut_mean > 1.1 * ref_mean:
        return "Excellent"
    elif 0.9 * ref_mean <= dut_mean <= 1.1 * ref_mean:
        return "Pass"
    elif 0.8 * ref_mean <= dut_mean < 0.9 * ref_mean:
        return "Marginal Fail"
    else:
        return "Fail"

if __name__ == "__main__":
    # Define file paths
    DUT_MRAB_CSV_PATH = "Raw Data/5G VoNR MRAB Stationary/DUT MRAB.csv"
    REF_MRAB_CSV_PATH = "Raw Data/5G VoNR MRAB Stationary/REF MRAB.csv"
    JSON_OUTPUT_PATH = "Scripts/React/frontend/src/data_analysis_results.json"
    THROUGHPUT_HEADER = "[Call Test] [Throughput] Application DL TP" # Using DL TP as discussed

    # Initialize data structure for JSON output
    data = {}
    try:
        with open(JSON_OUTPUT_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Warning: JSON file not found at '{JSON_OUTPUT_PATH}'. Creating a new one.")
        data = {} # Start with an empty dictionary if file doesn't exist
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from '{JSON_OUTPUT_PATH}'. Starting with an empty dictionary.")
        data = {}
    except Exception as e:
        print(f"An unexpected error occurred while reading JSON: {e}. Starting with an empty dictionary.")
        data = {}

    # Ensure the top-level key exists
    if "5G VoNR MRAB Stationary" not in data:
        data["5G VoNR MRAB Stationary"] = {}

    # Process DUT MRAB data
    print(f"Processing DUT MRAB data from: {DUT_MRAB_CSV_PATH}")
    dut_intervals = extract_intervals_and_values(DUT_MRAB_CSV_PATH, THROUGHPUT_HEADER)
    print(f"  Total DUT intervals counted: {len(dut_intervals)}")
    dut_mrab_analysis = {}
    dut_mrab_line_ranges = {}
    dut_mrab_averages_with_lines = {} # Renamed from sums_with_lines
    if dut_intervals:
        dut_mrab_analysis, dut_mrab_line_ranges, dut_mrab_averages_with_lines = analyze_grouped_intervals(dut_intervals)
        data["5G VoNR MRAB Stationary"]["DUT MRAB"] = {"MRAB Statistics": dut_mrab_analysis}
        print("DUT MRAB statistics generated.")
    else:
        print(f"Could not extract intervals for DUT MRAB from {DUT_MRAB_CSV_PATH}. Skipping DUT MRAB analysis.")
        data["5G VoNR MRAB Stationary"]["DUT MRAB"] = {"MRAB Statistics": {}} # Ensure key exists even if empty

    # Process REF MRAB data
    print(f"Processing REF MRAB data from: {REF_MRAB_CSV_PATH}")
    ref_intervals = extract_intervals_and_values(REF_MRAB_CSV_PATH, THROUGHPUT_HEADER)
    print(f"  Total REF intervals counted: {len(ref_intervals)}")
    ref_mrab_analysis = {}
    ref_mrab_line_ranges = {}
    ref_mrab_averages_with_lines = {} # Renamed from sums_with_lines
    if ref_intervals:
        ref_mrab_analysis, ref_mrab_line_ranges, ref_mrab_averages_with_lines = analyze_grouped_intervals(ref_intervals)
        data["5G VoNR MRAB Stationary"]["REF MRAB"] = {"MRAB Statistics": ref_mrab_analysis}
        print("REF MRAB statistics generated.")
    else:
        print(f"Could not extract intervals for REF MRAB from {REF_MRAB_CSV_PATH}. Skipping REF MRAB analysis.")
        data["5G VoNR MRAB Stationary"]["REF MRAB"] = {"MRAB Statistics": {}} # Ensure key exists even if empty

    # Extract MRAB statistics for DUT and REF from the newly processed data
    dut_mrab_stats = data["5G VoNR MRAB Stationary"].get("DUT MRAB", {}).get("MRAB Statistics", {})
    ref_mrab_stats = data["5G VoNR MRAB Stationary"].get("REF MRAB", {}).get("MRAB Statistics", {})

    # Calculate and store status for each group
    mrab_statuses = {}
    group_names = ["Pre Call", "In Call", "Post Call"]

    for group_name in group_names:
        dut_mean = dut_mrab_stats.get(group_name, {}).get("Mean")
        ref_mean = ref_mrab_stats.get(group_name, {}).get("Mean")
        status = calculate_group_status(dut_mean, ref_mean, group_name)
        mrab_statuses[group_name] = status

    # Print statistics to console
    group_labels = {0: "Pre Call", 1: "In Call", 2: "Post Call"} # Define group_labels here for printing

    print("\n--- DUT MRAB Statistics ---")
    for group_key, stats in dut_mrab_analysis.items():
        print(f"  {group_key}:")
        for stat_name, value in stats.items():
            print(f"    {stat_name}: {value}")
    
    print("\n--- REF MRAB Statistics ---")
    for group_key, stats in ref_mrab_analysis.items():
        print(f"  {group_key}:")
        for stat_name, value in stats.items():
            print(f"    {stat_name}: {value}")

    print("\n--- MRAB Case Statuses by Group ---")
    for group_name, status in mrab_statuses.items():
        print(f"  {group_name} Status: {status}")

    # Add the individual Mrab statuses to the JSON data
    data["5G VoNR MRAB Stationary"]["mrabGroupStatuses"] = mrab_statuses

    # Write the updated data back to the JSON file
    try:
        with open(JSON_OUTPUT_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"\nSuccessfully updated '{JSON_OUTPUT_PATH}' with Mrab Group Statuses.")
    except Exception as e:
        print(f"An unexpected error occurred while writing JSON: {e}")
        sys.exit(1)
