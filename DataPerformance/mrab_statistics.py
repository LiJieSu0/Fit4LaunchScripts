import csv
import sys
import numpy as np

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
    return results

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
        return "Fail"

if __name__ == "__main__":
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python mrab_statistics.py <path_to_data_analysis_results.json>")
        sys.exit(1)

    json_file_path = sys.argv[1]

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at '{json_file_path}'")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{json_file_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while reading JSON: {e}")
        sys.exit(1)

    # Extract MRAB statistics for DUT and REF
    mrab_data_section = data.get("5G VoNR MRAB Stationary", {})
    dut_mrab_stats = mrab_data_section.get("DUT MRAB", {}).get("MRAB Statistics", {})
    ref_mrab_stats = mrab_data_section.get("REF MRAB", {}).get("MRAB Statistics", {})

    dut_in_call_mean = dut_mrab_stats.get("In Call", {}).get("Mean")
    ref_in_call_mean = ref_mrab_stats.get("In Call", {}).get("Mean")

    overall_mrab_status = "N/A"
    if dut_in_call_mean is not None and ref_in_call_mean is not None:
        overall_mrab_status = calculate_mrab_status(dut_in_call_mean, ref_in_call_mean)
    else:
        overall_mrab_status = "Cannot perform Mrab Case comparison: 'In Call' Mean not available for both DUT and REF."

    # Add the overall Mrab status to the JSON data
    if "5G VoNR MRAB Stationary" not in data:
        data["5G VoNR MRAB Stationary"] = {}
    data["5G VoNR MRAB Stationary"]["overallMrabStatus"] = overall_mrab_status

    # Write the updated data back to the JSON file
    try:
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Successfully updated '{json_file_path}' with Mrab Case Status: {overall_mrab_status}")
    except Exception as e:
        print(f"An unexpected error occurred while writing JSON: {e}")
        sys.exit(1)
