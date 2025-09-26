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

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python marb_statistics.py <path_to_csv_file>")
        sys.exit(1)

    csv_file_path = sys.argv[1]
    target_header = "[Call Test] [Throughput] Application DL TP"
    threshold = 10

    all_intervals_with_lines = extract_intervals_and_values(csv_file_path, target_header, threshold)

    if all_intervals_with_lines:
        print(f"Total number of discrete intervals found: {len(all_intervals_with_lines)}")
        analysis_results = analyze_grouped_intervals(all_intervals_with_lines)
        
        for group_name, stats in analysis_results.items():
            print(f"\n--- {group_name} Statistics ---") # Changed this line
            for key, value in stats.items():
                if key == "Interval Line Ranges":
                    # print(f"{key}:") # Commented out as per user request
                    # for line_range in value: # Commented out as per user request
                    #     print(f"  Lines {line_range[0]} to {line_range[1]}") # Commented out as per user request
                    pass # Added pass to maintain valid syntax for the if block
                else:
                    print(f"{key}: {value}")
    else:
        print("No intervals found or an error occurred during extraction.")
