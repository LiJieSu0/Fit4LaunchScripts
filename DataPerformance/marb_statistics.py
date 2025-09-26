import csv
import sys

def calculate_intervals(file_path, header_name, blank_row_threshold=10):
    """
    Calculates the number of discrete intervals in a specified column of a CSV file.

    An interval is defined by consecutive non-empty rows. If the number of
    consecutive empty rows exceeds `blank_row_threshold`, a new interval begins.

    Args:
        file_path (str): The path to the CSV file.
        header_name (str): The name of the header column to analyze.
        blank_row_threshold (int): The maximum number of consecutive blank rows
                                   allowed within a single interval.

    Returns:
        int: The total number of discrete intervals found.
    """
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)  # Read the header row

            try:
                column_index = headers.index(header_name)
            except ValueError:
                print(f"Error: Header '{header_name}' not found in the CSV file.")
                return 0

            interval_count = 0
            consecutive_blank_rows = 0
            in_interval = False

            for row in reader:
                if len(row) > column_index:
                    cell_value = row[column_index].strip()
                else:
                    cell_value = "" # Treat as blank if row is too short

                if cell_value:  # If the cell is not blank
                    if not in_interval:
                        interval_count += 1
                        in_interval = True
                    consecutive_blank_rows = 0
                else:  # If the cell is blank
                    if in_interval:
                        consecutive_blank_rows += 1
                        if consecutive_blank_rows > blank_row_threshold:
                            in_interval = False
                            consecutive_blank_rows = 0 # Reset for next potential interval

        return interval_count

    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'")
        return 0
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python marb_statistics.py <path_to_csv_file>")
        sys.exit(1)

    csv_file_path = sys.argv[1]
    target_header = "[Call Test] [Throughput] Application DL TP"
    threshold = 10

    intervals = calculate_intervals(csv_file_path, target_header, threshold)
    if intervals > 0:
        print(f"Number of discrete intervals for '{target_header}': {intervals}")
