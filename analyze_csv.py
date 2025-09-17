import numpy as np
import pandas as pd
import sys

#Etc count as success
#603 decline remove form total
#No service calculate

def _calculate_statistical_analysis(data):
    """
    Calculates statistical data for numeric columns and returns the mean setup time.
    """
    target_columns = [
        "[Call Test] [Voice or Video Call] [Duration] Traffic Duration (LoggingTool)",
        "[Call Test] [VoNR VoLTE] [Duration] SIP Setup Duration (Invite~200OK)",
    ]
    mean_setup_time = None

    target_data = data[target_columns]

    if target_data.empty:
        print("Target columns not found or are empty in the CSV file.")
        return mean_setup_time

    print("Statistical Analysis of Target Columns:")
    for column in target_data.columns:
        if column in data.columns:
            print(f"\n--- Statistics for column: {column} ---")
            column_data = target_data[column].dropna()
            if not column_data.empty:
                mean_val = np.mean(column_data)
                print(f"Mean: {mean_val:.2f}")
                print(f"Median: {np.median(column_data):.2f}")
                print(f"Standard Deviation: {np.std(column_data):.2f}")
                print(f"Minimum: {np.min(column_data):.2f}")
                print(f"Maximum: {np.max(column_data):.2f}")
                if column == "[Call Test] [VoNR VoLTE] [Duration] SIP Setup Duration (Invite~200OK)":
                    mean_setup_time = mean_val
            else:
                print("No valid data available for this column after dropping NaNs.")
        else:
            print(f"\nColumn '{column}' not found in the CSV file.")
    print("-" * 30)
    return mean_setup_time

def _count_invite_occurrences(data):
    """
    Counts 'INVITE' occurrences in '[Packet Data][SIP]Request Method' and returns the count.
    """
    invite_column_name = "[Packet Data] [SIP] Request Method"
    invite_count = 0
    if invite_column_name in data.columns:
        invite_count = data[invite_column_name].astype(str).str.contains("INVITE", na=False).sum()
        print(f"\n--- Count of 'INVITE' in column: {invite_column_name} ---")
        print(f"Total INVITE SIP: {invite_count}")
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
    Calculates and returns Call Failure/Success Metrics.
    """
    fail_count = 0
    success_rate = 0.0
    fail_rate = 0.0
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
    return fail_count, success_rate, fail_rate

def _calculate_network_type_counts(data):
    """
    Calculates and displays Network Type counts for Voice Calls.
    """
    call_type_header_col = "[Call Test] Call Type"
    call_middle_network_col = "[Call Test] Call Middle Network"
    network_type_counts = {
        "VoNR": 0,
        "VoLTE": 0,
        "EPSFB": 0,
        "No Service":0,
        "Unknown": 0
    }

    if call_type_header_col in data.columns and call_middle_network_col in data.columns:
        voice_calls = data[data[call_type_header_col].astype(str) == 'Voice'].copy()

        if not voice_calls.empty:
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
    return network_type_counts

def remove_from_total_count(data): # remove some other exceptions from total counts
    """
    Calculates the number of '603 Declined' occurrences in '[Packet Data] [SIP] Status'.
    """
    sip_status_column = "[Packet Data] [SIP] Status"
    declined_count = 0

    if sip_status_column in data.columns:
        declined_count = data[sip_status_column].astype(str).str.contains("603 Declined", na=False).sum()
    else:
        print(f"\nColumn '{sip_status_column}' not found in the CSV file.")
    print("-" * 30)
    return declined_count

def no_service_failed(data):
    """
    Checks for 'No Service' and '603 Declined' within specific intervals.
    An interval starts with 'Voice' and 'Orig. Fail' and ends with 'HTTP Download'.
    """
    call_type_col = "[Call Test] Call Type"
    call_result_col = "[Call Test] Call Result"
    serving_network_col = "[General] Serving Network (In Traffic)"
    sip_status_col = "[Packet Data] [SIP] Status"

    no_service_count = 0
    declined_count = 0

    if not all(col in data.columns for col in [call_type_col, call_result_col, serving_network_col, sip_status_col]):
        print("\n--- No Service and 603 Declined Counts after Failed Voice Calls ---")
        print("Required columns for 'no_service_failed' not found.")
        print("-" * 30)
        return no_service_count, declined_count

    # Find all 'Orig. Fail' events for 'Voice' calls
    fail_events_indices = data[
        (data[call_type_col].astype(str) == 'Voice') &
        (data[call_result_col].astype(str) == 'Orig. Fail')
    ].index.tolist()

    for fail_index in fail_events_indices:
        http_download_index = -1
        # Search upwards for 'HTTP Download'
        for k in range(fail_index - 1, -1, -1): # Iterate backwards from fail_index - 1 to 0
            if str(data.loc[k, call_type_col]) == 'HTTP Download':
                http_download_index = k
                break
        
        # If an 'HTTP Download' is found before the 'Orig. Fail'
        if http_download_index != -1:
            print(f"\n--- Interval found: HTTP Download at Row {http_download_index}, Orig. Fail at Row {fail_index} ---")
            
            found_in_interval = False
            # Check for '603 Declined' within the interval [http_download_index, fail_index]
            for j in range(http_download_index, fail_index + 1):
                if "603 Declined" in str(data.loc[j, sip_status_col]):
                    declined_count += 1
                    found_in_interval = True
                    print(f"  Found '603 Declined' at row {j}")
                    break # Found 603 Declined, move to next fail event
            
            # Only check for 'No Service' if '603 Declined' was not found
            if not found_in_interval:
                for j in range(http_download_index, fail_index + 1):
                    if str(data.loc[j, serving_network_col]) == 'No Service':
                        no_service_count += 1
                        print(f"  Found 'No Service' at row {j}")
                        break # Found No Service, move to next fail event
        else:
            print(f"\n--- Orig. Fail at Row {fail_index} but no preceding 'HTTP Download' found. Skipping. ---")
    print("\n--- No Service and 603 Declined Counts after Failed Voice Calls ---")
    print(f"Total No Service occurrences after failed voice calls: {no_service_count}")
    print(f"Total 603 Declined occurrences after failed voice calls: {declined_count}")
    print("-" * 30)
    return no_service_count, declined_count

def analyze_csv(file_path):
    """
    Reads a CSV file, calculates, and returns statistical data.

    Args:
        file_path (str): The path to the CSV file.
    Returns:
        dict: A dictionary containing the analyzed metrics.
    """
    metrics = {
        "Device": "N/A", # Placeholder
        "Connection Attempts": 0,
        "Mean Setup Time (s)": 0.0,
        "Successful Initiations": 0,
        "Successful Initiations (%)": 0.0,
        "Failed Initiations": 0,
        "Failed Initiations (%)": 0.0,
        "P - Value": 1.0 # Placeholder
    }

    try:
        data = pd.read_csv(file_path)
        print(f"Successfully loaded {file_path}")

        mean_setup_time = _calculate_statistical_analysis(data)
        if mean_setup_time is not None:
            metrics["Mean Setup Time (s)"] = round(mean_setup_time, 2)

        invite_count = _count_invite_occurrences(data) - remove_from_total_count(data)
        metrics["Connection Attempts"] = invite_count
        print(f"\n--- Invite_count '{invite_count}' ---")

        success_initiation_count = _count_success_initiation(data)
        metrics["Successful Initiations"] = success_initiation_count

        fail_count, success_rate, fail_rate = _calculate_call_failure_success_metrics(invite_count, success_initiation_count)
        metrics["Failed Initiations"] = fail_count
        metrics["Successful Initiations (%)"] = round(success_rate, 2)
        metrics["Failed Initiations (%)"] = round(fail_rate, 2)

        _calculate_network_type_counts(data)
        no_service_failed(data)

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return metrics

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        result_metrics = analyze_csv(file_path)
        print("\n--- Analysis Results ---")
        for key, value in result_metrics.items():
            print(f"{key}: {value}")
    else:
        print("Please provide the path to the CSV file as a command-line argument.")
        print("Usage: python Scripts/analyze_csv.py <path_to_your_csv_file>")
