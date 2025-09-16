import numpy as np
import pandas as pd
import sys

#Etc count as success
#603 decline remove form total
#No service calculate

def _calculate_statistical_analysis(data):
    """
    Calculates and prints statistical data for numeric columns.
    """
    target_columns = [
        "[Call Test] [Voice or Video Call] [Duration] Traffic Duration (LoggingTool)",
        "[Call Test] [VoNR VoLTE] [Duration] SIP Setup Duration (Invite~200OK)",
    ]

    target_data = data[target_columns]

    if target_data.empty:
        print("Target columns not found or are empty in the CSV file.")
        return

    print("Statistical Analysis of Target Columns:")
    for column in target_data.columns:
        if column in data.columns:
            print(f"\n--- Statistics for column: {column} ---")
            column_data = target_data[column].dropna()
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
    print("-" * 30)

def _count_invite_occurrences(data):
    """
    Counts 'INVITE' occurrences in '[Packet Data][SIP]Request Method' and returns the count.
    """
    invite_column_name = "[Packet Data] [SIP] Request Method"
    invite_count = 0
    if invite_column_name in data.columns:
        invite_count = data[invite_column_name].astype(str).str.contains("INVITE", na=False).sum()
        print(f"\n--- Count of 'INVITE' in column: {invite_column_name} ---")
        print(f"Total INVITEs: {invite_count}")
    else:
        print(f"\nColumn '{invite_column_name}' not found in the CSV file.")
    print("-" * 30)
    return invite_count

def _count_success_initiation(data):
    """
    Counts "Success initiation" based on SIP INVITE and 200 OK.
    """
    method_col = "[Packet Data] [SIP] 200 OK - Method"
    status_col = "[Packet Data] [SIP] Status"
    success_initiation_count = 0
    
    if method_col in data.columns and status_col in data.columns:
        success_initiation_df = data[
            (data[method_col].astype(str) == 'INVITE') &
            (data[status_col].astype(str).str.contains('200 OK', na=False))
        ]
        success_initiation_count = len(success_initiation_df)
        print("\n--- Success Initiation Count ---")
        print(f"Success initation: {success_initiation_count}")
    else:
        print("\n--- Success Initiation Count ---")
        print("Required columns for 'Success initation' not found.")
    print("-" * 30)
    return success_initiation_count

def _calculate_call_failure_success_metrics(invite_count, success_initiation_count):
    """
    Calculates and displays Call Failure/Success Metrics.
    """
    if invite_count > 0:
        fail_count = invite_count - success_initiation_count
        success_rate = (success_initiation_count / invite_count) * 100
        fail_rate = (fail_count / invite_count) * 100
        print("\n--- Call Failure/Success Metrics ---")
        print(f"Fail Count: {fail_count}")
        print(f"Success rate: {success_rate:.1f}%")
        print(f"Fail rate: {fail_rate:.1f}%")
    else:
        print("\n--- Call Failure/Success Metrics ---")
        print("Cannot calculate metrics (Total INVITEs is zero or not calculated).")
    print("-" * 30)

def _calculate_network_type_counts(data):
    """
    Calculates and displays Network Type counts for Voice Calls.
    """
    call_type_header_col = "[Call Test] Call Type"
    call_middle_network_col = "[Call Test] Call Middle Network"

    if call_type_header_col in data.columns and call_middle_network_col in data.columns:
        voice_calls = data[data[call_type_header_col].astype(str) == 'Voice'].copy()

        if not voice_calls.empty:
            network_type_counts = {
                "VoNR": 0,
                "VoLTE": 0,
                "EPSFB": 0,
                "Unknown": 0 # Changed from "No Service" to "Unknown" for consistency with previous logic
            }

            for index, row in voice_calls.iterrows():
                network_info = str(row[call_middle_network_col])
                if "VoNR" in network_info:
                    network_type_counts["VoNR"] += 1
                elif "LTE" in network_info:
                    network_type_counts["VoLTE"] += 1
                elif "EPSFB" in network_info:
                    network_type_counts["EPSFB"] += 1
                else:
                    network_type_counts["Unknown"] += 1
            
            print("\n--- Network Type Counts (for Voice Calls) ---")
            for network_type, count in network_type_counts.items():
                print(f"{network_type}: {count}")
        else:
            print(f"No 'Voice' calls found in column '{call_type_header_col}'.")
    else:
        print(f"Required columns for Network Type calculation ('{call_type_header_col}' or '{call_middle_network_col}') not found.")
    print("-" * 30)

def _calculate_fail_count(data):
    """
    Calculates and displays the Tool Fail Count for '[Event] Voice Call Event'.
    """
    event_column_name = "[Event] Voice Call Event"
    fail_result_string = "[Tool] Voice - Call Result : Orig. Fail" # Reverted to full string
    tool_fail_count = 0

    if event_column_name in data.columns:
        tool_fail_count = data[event_column_name].astype(str).str.contains(fail_result_string, na=False).sum()
        print(f"\n--- Tool Fail Count for '{event_column_name}' ---")
        print(f"Occurrences of '{fail_result_string}': {tool_fail_count}")
    else:
        print(f"\nColumn '{event_column_name}' not found in the CSV file.")
    print("-" * 30)

def analyze_csv(file_path):
    """
    Reads a CSV file, calculates, and prints statistical data for numeric columns.

    Args:
        file_path (str): The path to the CSV file.
    """
    try:
        data = pd.read_csv(file_path)
        print(f"Successfully loaded {file_path}")

        _calculate_statistical_analysis(data)
        invite_count = _count_invite_occurrences(data)
        success_initiation_count = _count_success_initiation(data)
        _calculate_call_failure_success_metrics(invite_count, success_initiation_count)
        _calculate_network_type_counts(data)
        _calculate_fail_count(data)

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        analyze_csv(file_path)
    else:
        print("Please provide the path to the CSV file as a command-line argument.")
        print("Usage: python Scripts/analyze_csv.py <path_to_your_csv_file>")
