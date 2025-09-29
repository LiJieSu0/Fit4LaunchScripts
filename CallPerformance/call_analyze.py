import pandas as pd
import sys
import re
import os
from collections import defaultdict

def _clean_header(header):
    """
    Removes content within square brackets (tags) and strips leading/trailing whitespace from a header string.
    """
    # Remove content within square brackets, including the brackets themselves
    cleaned_header = re.sub(r'\[.*?\]', '', header)
    # Strip leading/trailing whitespace
    return cleaned_header.strip()

def analyze_call_data(file_path):
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None, None, None, None, None
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None, None, None, None, None

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
    # Success Rate

    # print(f"Analysis for file: {file_path}") # Commented out
    # print(f"Total attempts (Voice calls, excluding 603 Declined sections): {total_attempts}") # Commented out

    call_result_distribution = {}
    rat_distribution = {} # Initialize rat_distribution
    total_setup_duration = 0
    setup_duration_count = 0
    
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

    # New statistic: Mean setup Time
    if sip_setup_duration_col in df_filtered.columns:
        # Convert to numeric, coercing errors to NaN, then drop NaNs
        setup_durations = df_filtered[sip_setup_duration_col].apply(pd.to_numeric, errors='coerce').dropna()
        if not setup_durations.empty:
            total_setup_duration = setup_durations.sum()
            setup_duration_count = setup_durations.count()
    
    return total_attempts, call_result_distribution, rat_distribution, total_setup_duration, setup_duration_count

def analyze_directory(directory_path):
    total_attempts_sum = 0
    aggregated_call_results = defaultdict(int)
    aggregated_rat_distribution = defaultdict(int)
    aggregated_total_setup_duration = 0
    aggregated_setup_duration_count = 0
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                print(f"Analyzing file: {file_path}")
                total_attempts, call_result_distribution, rat_distribution, total_setup_duration, setup_duration_count = analyze_call_data(file_path)
                
                if total_attempts is not None:
                    total_attempts_sum += total_attempts
                
                if call_result_distribution is not None:
                    for result, count in call_result_distribution.items():
                        aggregated_call_results[result] += count
                
                if rat_distribution is not None:
                    for rat, count in rat_distribution.items():
                        aggregated_rat_distribution[rat] += count
                
                if total_setup_duration is not None:
                    aggregated_total_setup_duration += total_setup_duration
                if setup_duration_count is not None:
                    aggregated_setup_duration_count += setup_duration_count
                        
    mean_setup_time = None
    if aggregated_setup_duration_count > 0:
        mean_setup_time = aggregated_total_setup_duration / aggregated_setup_duration_count

    return {
        "total_attempts": total_attempts_sum,
        "call_result_distribution": dict(aggregated_call_results),
        "rat_distribution": dict(aggregated_rat_distribution),
        "mean_setup_time": mean_setup_time
    }

def _print_analysis_results(results):
    print(f"Total attempts (Voice calls, excluding 603 Declined sections) across all files: {results['total_attempts']}")
    
    print("\nAggregated Call Result Distribution for 'Voice' Call Type (excluding 603 Declined sections):")
    if results['call_result_distribution']:
        for result, count in results['call_result_distribution'].items():
            print(f"  {result}: {count}")
    else:
        print("No 'Voice' call types found in the aggregated data for Call Result distribution.")

    print("\nAggregated RAT Distribution for 'Voice' Call Type:")
    if results['rat_distribution']:
        for rat, count in results['rat_distribution'].items():
            print(f"  {rat}: {count}")
    else:
        print("No 'Voice' call types found in the aggregated data for RAT distribution.")

    print("\nAggregated Mean Setup Time (excluding 603 Declined sections):")
    if results['mean_setup_time'] is not None:
        print(f"  {results['mean_setup_time']:.2f} (seconds)")
    else:
        print("  No valid setup durations found for aggregation.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python call_analyze.py <path_to_csv_file_or_directory>")
    else:
        input_path = sys.argv[1]
        if os.path.isfile(input_path):
            total_attempts, call_result_distribution, rat_distribution, total_setup_duration, setup_duration_count = analyze_call_data(input_path)
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
            
            print("\nMean Setup Time (excluding 603 Declined sections):")
            if setup_duration_count > 0:
                mean_setup_time = total_setup_duration / setup_duration_count
                print(f"  {mean_setup_time:.2f} (seconds)")
            else:
                print("  No valid setup durations found.")
        elif os.path.isdir(input_path):
            dut_path = os.path.join(input_path, 'DUT')
            ref_path = os.path.join(input_path, 'REF')

            dut_results = None
            ref_results = None

            if os.path.isdir(dut_path):
                print(f"\n--- Analyzing DUT data in: {dut_path} ---")
                dut_results = analyze_directory(dut_path)
            else:
                print(f"Warning: DUT directory not found at {dut_path}")

            if os.path.isdir(ref_path):
                print(f"\n--- Analyzing REF data in: {ref_path} ---")
                ref_results = analyze_directory(ref_path)
            else:
                print(f"Warning: REF directory not found at {ref_path}")

            if dut_results:
                print("\n--- DUT Aggregated Analysis Results ---")
                _print_analysis_results(dut_results)
            
            if ref_results:
                print("\n--- REF Aggregated Analysis Results ---")
                _print_analysis_results(ref_results)

        else:
            print(f"Error: Invalid path provided: {input_path}. Must be a file or a directory.")
