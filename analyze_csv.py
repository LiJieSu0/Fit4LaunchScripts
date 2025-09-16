import numpy as np
import pandas as pd
import sys

def analyze_csv(file_path):
    """
    Reads a CSV file, calculates, and prints statistical data for numeric columns.

    Args:
        file_path (str): The path to the CSV file.
    """
    try:
        # Read the CSV file using pandas
        data = pd.read_csv(file_path)
        print(f"Successfully loaded {file_path}")
        print("First 5 rows of the data:")
        print(data.head())
        print("-" * 30)

        # Define the specific columns to be analyzed
        target_columns = [
            "[Call Test][Voice or Video Call][Duration]Traffic Duration (LoggingTool)(sec)",
            "[Call Test][VoNR VoLTE][Duration]SIP Setup Duration (Invite~200OK)(sec)"
        ]

        # Filter the data to include only the target columns
        target_data = data[target_columns]

        if target_data.empty:
            print("Target columns not found or are empty in the CSV file.")
            return

        print("Statistical Analysis of Target Columns:")
        for column in target_data.columns:
            # Ensure the column exists in the dataframe before processing
            if column in data.columns:
                print(f"\n--- Statistics for column: {column} ---")
                column_data = target_data[column].dropna() # Drop NaN values for accurate stats
                if not column_data.empty:
                    print(f"Mean: {np.mean(column_data):.2f}")
                    print(f"Median: {np.median(column_data):.2f}")
                    print(f"Standard Deviation: {np.std(column_data):.2f}")
                    print(f"Minimum: {np.min(column_data):.2f}")
                    print(f"Maximum: {np.max(column_data):.2f}")
                else:
                    print("No valid data available for this column after dropping NaNs.")
            else:
                print(f"\nColumn '{column}' not found in the CSV file.")

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Check if the file path is provided from the command line
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        analyze_csv(file_path)
    else:
        print("Please provide the path to the CSV file as a command-line argument.")
        print("Usage: python Scripts/analyze_csv.py <path_to_your_csv_file>")
