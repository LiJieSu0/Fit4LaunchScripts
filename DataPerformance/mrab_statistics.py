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

    grouped_interval_sums = {
        0: [],  # Sums of intervals where index % 3 == 0
        1: [],  # Sums of intervals where index % 3 == 1
        2: []   # Sums of intervals where index % 3 == 2
    }
    grouped_interval_line_ranges = {
        0: [],
        1: [],
        2: []
    }

    for i, (interval_values, line_range) in enumerate(all_intervals_with_lines):
        if interval_values: # Only calculate sum if interval is not empty
            interval_sum = np.sum(interval_values)
            group_key = i % 3
            grouped_interval_sums[group_key].append(interval_sum)
            grouped_interval_line_ranges[group_key].append(line_range)

    results = {}
    grouped_interval_sums_with_lines = {
        0: [],
        1: [],
        2: []
    }

    for i, (interval_values, line_range) in enumerate(all_intervals_with_lines):
        if interval_values:
            interval_sum = np.sum(interval_values)
            group_key = i % 3
            grouped_interval_sums_with_lines[group_key].append((interval_sum, line_range))

    for group_key, sums_in_group in grouped_interval_sums.items():
        group_name = group_labels.get(group_key, f"Group {group_key}") # Get the descriptive name
        if not sums_in_group:
            results[group_name] = {
                "Mean": None,
                "Maximum": None,
                "Minimum": None,
                "Standard Deviation": None
            }
            continue

        total_sum_of_sums = np.sum(sums_in_group)
        average_of_sums = np.mean(sums_in_group)
        maximum_of_sums = np.max(sums_in_group)
        minimum_of_sums = np.min(sums_in_group)
        std_dev_of_sums = np.std(sums_in_group)

        results[group_name] = {
            "Mean": average_of_sums,
            "Maximum": maximum_of_sums,
            "Minimum": minimum_of_sums,
            "Standard Deviation": std_dev_of_sums
        }
    return results, grouped_interval_line_ranges, grouped_interval_sums_with_lines

def calculate_mrab_status(overall_avg_tput_dut, overall_avg_tput_ref):
    """
    Calculates the Mrab Case status based on DUT and REF overall average throughputs.

    Args:
        overall_avg_tput_dut (float): Overall Average Throughput for Device Under Test (DUT).
        overall_avg_tput_ref (float): Overall Average Throughput for Reference Device (REF).

    Returns:
        str: The Mrab Case status (Excellent, Pass, Marginal Fail, Fail).
    """
    if overall_avg_tput_ref is None or overall_avg_tput_ref == 0:
        return "Cannot calculate: Reference Throughput is zero or None."
    if overall_avg_tput_dut is None:
        return "Cannot calculate: DUT Throughput is None."

    if overall_avg_tput_dut > 1.1 * overall_avg_tput_ref:
        return "Excellent"
    elif 0.9 * overall_avg_tput_ref <= overall_avg_tput_dut <= 1.1 * overall_avg_tput_ref:
        return "Pass"
    elif 0.8 * overall_avg_tput_ref <= overall_avg_tput_dut < 0.9 * overall_avg_tput_ref:
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
    dut_mrab_sums_with_lines = {}
    if dut_intervals:
        dut_mrab_analysis, dut_mrab_line_ranges, dut_mrab_sums_with_lines = analyze_grouped_intervals(dut_intervals)
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
    ref_mrab_sums_with_lines = {}
    if ref_intervals:
        ref_mrab_analysis, ref_mrab_line_ranges, ref_mrab_sums_with_lines = analyze_grouped_intervals(ref_intervals)
        data["5G VoNR MRAB Stationary"]["REF MRAB"] = {"MRAB Statistics": ref_mrab_analysis}
        print("REF MRAB statistics generated.")
    else:
        print(f"Could not extract intervals for REF MRAB from {REF_MRAB_CSV_PATH}. Skipping REF MRAB analysis.")
        data["5G VoNR MRAB Stationary"]["REF MRAB"] = {"MRAB Statistics": {}} # Ensure key exists even if empty

    # Extract MRAB statistics for DUT and REF from the newly processed data
    dut_mrab_stats = data["5G VoNR MRAB Stationary"].get("DUT MRAB", {}).get("MRAB Statistics", {})
    ref_mrab_stats = data["5G VoNR MRAB Stationary"].get("REF MRAB", {}).get("MRAB Statistics", {})

    dut_in_call_mean = dut_mrab_stats.get("In Call", {}).get("Mean")
    ref_in_call_mean = ref_mrab_stats.get("In Call", {}).get("Mean")

    overall_mrab_status = "N/A"
    if dut_in_call_mean is not None and ref_in_call_mean is not None:
        overall_mrab_status = calculate_mrab_status(dut_in_call_mean, ref_in_call_mean)
    else:
        overall_mrab_status = "Cannot perform Mrab Case comparison: 'In Call' Mean not available for both DUT and REF."

    # Print statistics to console
    group_labels = {0: "Pre Call", 1: "In Call", 2: "Post Call"} # Define group_labels here for printing

    print("\n--- DUT MRAB Statistics ---")
    for group_key, stats in dut_mrab_analysis.items():
        print(f"  {group_key}:")
        for stat_name, value in stats.items():
            print(f"    {stat_name}: {value}")
    
    print("\n--- DUT MRAB Intervals (Line Ranges and Sums) ---")
    for group_key, sums_with_lines in dut_mrab_sums_with_lines.items():
        group_name = group_labels.get(group_key, f"Group {group_key}")
        print(f"  {group_name} Intervals:")
        if sums_with_lines:
            for interval_sum, (start, end) in sums_with_lines:
                print(f"    Lines {start}-{end}, Sum: {interval_sum:.2f}")
        else:
            print("    No intervals found for this group.")

    print("\n--- REF MRAB Statistics ---")
    for group_key, stats in ref_mrab_analysis.items():
        print(f"  {group_key}:")
        for stat_name, value in stats.items():
            print(f"    {stat_name}: {value}")

    print("\n--- REF MRAB Intervals (Line Ranges and Sums) ---")
    for group_key, sums_with_lines in ref_mrab_sums_with_lines.items():
        group_name = group_labels.get(group_key, f"Group {group_key}")
        print(f"  {group_name} Intervals:")
        if sums_with_lines:
            for interval_sum, (start, end) in sums_with_lines:
                print(f"    Lines {start}-{end}, Sum: {interval_sum:.2f}")
        else:
            print("    No intervals found for this group.")

    print(f"\nOverall Mrab Case Status: {overall_mrab_status}")

    # Add the overall Mrab status to the JSON data
    data["5G VoNR MRAB Stationary"]["overallMrabStatus"] = overall_mrab_status

    # Write the updated data back to the JSON file
    try:
        with open(JSON_OUTPUT_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"\nSuccessfully updated '{JSON_OUTPUT_PATH}' with Mrab Case Status: {overall_mrab_status}")
    except Exception as e:
        print(f"An unexpected error occurred while writing JSON: {e}")
        sys.exit(1)
