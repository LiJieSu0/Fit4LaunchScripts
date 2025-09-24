import csv
import sys
import os

def _remove_summary_from_single_csv(filepath):
    """
    Removes specific summary lines from a single CSV file in-place.
    This is a helper function for internal use.
    """
    lines_to_remove_prefixes = [
        "IMEI :",
        "IMSI :",
        "Phone Number :",
        "Start Time :",
        "End Time :"
    ]

    try:
        # Read all lines first
        with open(filepath, 'r', newline='', encoding='utf-8') as infile:
            lines = list(csv.reader(infile))

        cleaned_lines = []
        for row in lines:
            if not row:  # Skip empty rows
                continue

            # Check if the first element of the row starts with any of the prefixes to remove
            is_summary_line = False
            for prefix in lines_to_remove_prefixes:
                if row[0].strip().startswith(prefix):
                    is_summary_line = True
                    break
            
            if not is_summary_line:
                cleaned_lines.append(row)
        
        # Write the cleaned lines back to the same file
        with open(filepath, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(cleaned_lines)
        
        print(f"Successfully removed summary lines from '{filepath}' (in-place modification).")

    except FileNotFoundError:
        print(f"Error: File not found at '{filepath}'")
    except Exception as e:
        print(f"An error occurred while processing '{filepath}': {e}")

def process_csv_files_in_directory(directory_path):
    """
    Iterates through all CSV files in the specified directory and its subdirectories,
    and removes specific summary lines from each CSV file in-place.

    Args:
        directory_path (str): The path to the directory to process.
    """
    if not os.path.isdir(directory_path):
        print(f"Error: Directory not found at '{directory_path}'")
        sys.exit(1)

    print(f"Starting to process CSV files in '{directory_path}' and its subdirectories...")
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith('.csv'):
                filepath = os.path.join(root, file)
                print(f"Processing file: {filepath}")
                _remove_summary_from_single_csv(filepath)
    print("Finished processing all CSV files.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python remove_summary_from_csv.py <directory_path>")
        sys.exit(1)

    target_directory = sys.argv[1]
    process_csv_files_in_directory(target_directory)
