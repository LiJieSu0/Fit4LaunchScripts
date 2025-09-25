import pandas as pd
import sys
import re

def _clean_header(header):
    """
    Removes content within square brackets (tags) and strips leading/trailing whitespace from a header string.
    """
    # Remove content within square brackets, including the brackets themselves
    cleaned_header = re.sub(r'\[.*?\]', '', header)
    # Strip leading/trailing whitespace
    return cleaned_header.strip()

import os
from collections import defaultdict

def analyze_call_data(file_path):
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None, None, None
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None, None, None

    # Apply the cleaning function to all column names in the DataFrame
    df.columns = [_clean_header(col) for col in df.columns]

    # Define cleaned header names
    packet_data_sip_request_method_col = _clean_header('[Packet Data] [SIP] Request Method')
    event_voice_call_event_col = _clean_header('[Event] Voice Call Event')
    sip_setup_duration_col = _clean_header('[Call Test] [VoNR VoLTE] [Duration] SIP Setup Duration (Invite~200OK)')
    packet_data_sip_status_col = _clean_header('[Packet Data] [SIP] Status')
    call_test_call_type_col = _clean_header('[Call Test] Call Type')
    call_test_real_service_col = _clean_header('[Call Test] [Voice or Video Call] Real Service')
    call_test_call_result_col = _clean_header('[Call Test] Call Result') # New cleaned header

    # Initialize a column to mark rows for exclusion
    df['exclude_from_stats'] = False

    # Find all occurrences of 'Voice - Call Scheduling Start(Orig)'
    # Escaping parentheses to treat them as literal characters, and using regex=True explicitly
    start_indices = df[df[event_voice_call_event_col].astype(str).str.contains(r'Voice - Call Scheduling Start\(Orig\)', na=False, regex=True)].index.tolist()
    # print(f"Found {len(start_indices)} 'Voice - Call Scheduling Start(Orig)' events at indices: {start_indices}") # Commented out for cleaner output

    for i, start_idx in enumerate(start_indices):
        # Determine the end of the current section
        # The section ends at the row before the next 'Voice - Call Scheduling Start(Orig)'
        # or at the end of the DataFrame if it's the last occurrence.
        end_idx = start_indices[i+1] - 1 if i + 1 < len(start_indices) else len(df) - 1

        # Ensure end_idx does not exceed DataFrame bounds
        end_idx = min(end_idx, len(df) - 1)

        # Check for '603 Declined' within the current section
        section = df.loc[start_idx : end_idx]
        if section[packet_data_sip_status_col].astype(str).str.contains('603 Declined', na=False).any():
            df.loc[start_idx : end_idx, 'exclude_from_stats'] = True
            # print(f"Marking rows from index {start_idx} to {end_idx} for exclusion due to '603 Declined' in section.") # Commented out
        # else:
            # print(f"Section from index {start_idx} to {end_idx} does not contain '603 Declined'.") # Commented out

    # Filter out the rows marked for exclusion
    df_filtered = df[~df['exclude_from_stats']]
    # print(f"Total rows in original DataFrame: {len(df)}") # Commented out
    # print(f"Total rows marked for exclusion: {df['exclude_from_stats'].sum()}") # Commented out
    # print(f"Total rows after exclusion: {len(df_filtered)}") # Commented out

    # 1. Total attempts: Count 'Voice' call types under '[Call Test] Call Type', excluding '603 Declined' sections.
    total_attempts = df_filtered[
        df_filtered[call_test_call_type_col].astype(str).str.contains('Voice', na=False)
    ].shape[0]

    # The following statistics are temporarily removed as per user request:
    # Fail attempts
    # Mean setup Time
    # Success Rate

    # print(f"Analysis for file: {file_path}") # Commented out
    # print(f"Total attempts (Voice calls, excluding 603 Declined sections): {total_attempts}") # Commented out

    call_result_distribution = {}
    rat_distribution = {} # Initialize rat_distribution
    
    # New statistic: Call Result Distribution for 'Voice' Call Type
    if call_test_call_result_col in df_filtered.columns and call_test_call_type_col in df_filtered.columns:
        voice_calls_df = df_filtered[df_filtered[call_test_call_type_col].astype(str).str.contains('Voice', na=False)]
        if not voice_calls_df.empty:
            call_result_distribution = voice_calls_df[call_test_call_result_col].value_counts().to_dict()
            # print("\nCall Result Distribution for 'Voice' Call Type (excluding 603 Declined sections):") # Commented out
            # for result, count in call_result_distribution.items(): # Commented out
                # print(f"  {result}: {count}") # Commented out
        # else:
            # print("\nNo 'Voice' call types found in the filtered data for Call Result distribution.") # Commented out
    # else:
        # print(f"\nColumns '{call_test_call_result_col}' or '{call_test_call_type_col}' not found in the filtered data. Cannot calculate Call Result distribution for 'Voice' Call Type.") # Commented out

    # New statistic: RAT distribution for 'Voice' call type
    if call_test_call_type_col in df_filtered.columns and call_test_real_service_col in df_filtered.columns:
        voice_calls_df = df_filtered[df_filtered[call_test_call_type_col].astype(str).str.contains('Voice', na=False)]
        if not voice_calls_df.empty:
            rat_distribution = voice_calls_df[call_test_real_service_col].value_counts().to_dict()
    
    return total_attempts, call_result_distribution, rat_distribution

def analyze_directory(directory_path):
    total_attempts_sum = 0
    aggregated_call_results = defaultdict(int)
    aggregated_rat_distribution = defaultdict(int)
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                print(f"Analyzing file: {file_path}")
                total_attempts, call_result_distribution, rat_distribution = analyze_call_data(file_path)
                
                if total_attempts is not None:
                    total_attempts_sum += total_attempts
                
                if call_result_distribution is not None:
                    for result, count in call_result_distribution.items():
                        aggregated_call_results[result] += count
                
                if rat_distribution is not None:
                    for rat, count in rat_distribution.items():
                        aggregated_rat_distribution[rat] += count
                        
    print("\n--- Aggregated Analysis Results ---")
    print(f"Total attempts (Voice calls, excluding 603 Declined sections) across all files: {total_attempts_sum}")
    
    print("\nAggregated Call Result Distribution for 'Voice' Call Type (excluding 603 Declined sections):")
    if aggregated_call_results:
        for result, count in aggregated_call_results.items():
            print(f"  {result}: {count}")
    else:
        print("No 'Voice' call types found in the aggregated data for Call Result distribution.")

    print("\nAggregated RAT Distribution for 'Voice' Call Type:")
    if aggregated_rat_distribution:
        for rat, count in aggregated_rat_distribution.items():
            print(f"  {rat}: {count}")
    else:
        print("No 'Voice' call types found in the aggregated data for RAT distribution.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python call_analyze.py <path_to_csv_file_or_directory>")
    else:
        input_path = sys.argv[1]
        if os.path.isfile(input_path):
            total_attempts, call_result_distribution, rat_distribution = analyze_call_data(input_path)
            print(f"Analysis for file: {input_path}")
            print(f"Total attempts (Voice calls, excluding 603 Declined sections): {total_attempts}")
            if call_result_distribution:
                print("\nCall Result Distribution for 'Voice' Call Type (excluding 603 Declined sections):")
                for result, count in call_result_distribution.items():
                    print(f"  {result}: {count}")
            else:
                print("\nNo 'Voice' call types found in the filtered data for Call Result distribution.")
            
            if rat_distribution:
                print("\nRAT Distribution for 'Voice' Call Type:")
                for rat, count in rat_distribution.items():
                    print(f"  {rat}: {count}")
            else:
                print("\nNo 'Voice' call types found in the filtered data for RAT distribution.")
        elif os.path.isdir(input_path):
            analyze_directory(input_path)
        else:
            print(f"Error: Invalid path provided: {input_path}. Must be a file or a directory.")
