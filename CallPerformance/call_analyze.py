import pandas as pd
import sys
import re
import os
from collections import defaultdict
from scipy.stats import fisher_exact

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
    
    FAILURE_CATEGORIES = ['Etc.', 'Orig. Fail', 'Forced stop', 'Drop']
    total_failures = sum(call_result_distribution.get(cat, 0) for cat in FAILURE_CATEGORIES)

    return total_attempts, total_failures, call_result_distribution, rat_distribution, total_setup_duration, setup_duration_count

def analyze_directory(directory_path):
    total_attempts_sum = 0
    total_failures_sum = 0
    aggregated_call_results = defaultdict(int)
    aggregated_rat_distribution = defaultdict(int)
    aggregated_total_setup_duration = 0
    aggregated_setup_duration_count = 0
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                print(f"Analyzing file: {file_path}")
                total_attempts, total_failures, call_result_distribution, rat_distribution, total_setup_duration, setup_duration_count = analyze_call_data(file_path)
                
                if total_attempts is not None:
                    total_attempts_sum += total_attempts
                
                if total_failures is not None:
                    total_failures_sum += total_failures

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
        "total_failures": total_failures_sum,
        "call_result_distribution": dict(aggregated_call_results),
        "rat_distribution": dict(aggregated_rat_distribution),
        "mean_setup_time": mean_setup_time
    }

def _print_analysis_results(results, ref_results=None):
    print(f"Total attempts (Voice calls, excluding 603 Declined sections) across all files: {results['total_attempts']}")
    print(f"Total failures (Voice calls, excluding 603 Declined sections) across all files: {results['total_failures']}")
    
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

    if ref_results:
        print("\n--- Criteria Analysis ---")
        print("\n5G Auto mode Call Initiation Criteria:")
        initiation_criteria = _calculate_fisher_exact_criteria(
            results['total_failures'], results['total_attempts'],
            ref_results['total_failures'], ref_results['total_attempts'],
            criteria_type="MO/MT"
        )
        print(f"  Result: {initiation_criteria}")

        print("\n5G Auto mode Call Retention (MO Only) Criteria:")
        retention_criteria = _calculate_fisher_exact_criteria(
            results['total_failures'], results['total_attempts'],
            ref_results['total_failures'], ref_results['total_attempts'],
            criteria_type="MO"
        )
        print(f"  Result: {retention_criteria}")

        print("\n5G Auto mode Call Setup Time Criteria:")
        setup_time_criteria = _calculate_call_setup_time_criteria(
            results['mean_setup_time'], ref_results['mean_setup_time']
        )
        print(f"  Result: {setup_time_criteria}")


def _calculate_fisher_exact_criteria(dut_failures, dut_attempts, ref_failures, ref_attempts, criteria_type="MO/MT"):
    if dut_attempts == 0 or ref_attempts == 0:
        return "N/A (Insufficient data for Fisher Exact Test)"

    dut_successes = dut_attempts - dut_failures
    ref_successes = ref_attempts - ref_failures

    # Ensure all values are non-negative
    if any(x < 0 for x in [dut_failures, dut_successes, ref_failures, ref_successes]):
        return "N/A (Invalid failure/success counts)"

    table = [[dut_successes, dut_failures],
             [ ref_successes,ref_failures]]
    
    print(f"    Contingency Table for {criteria_type} failures:")
    print(f"      DUT: [Failures: {dut_failures}, Successes: {dut_successes}]")
    print(f"      REF: [Failures: {ref_failures}, Successes: {ref_successes}]")

    # If any row or column sum is zero, fisher_exact might raise an error or return NaN p-value.
    # Handle this by checking for degenerate cases.
    if dut_failures + dut_successes == 0 or ref_failures + ref_successes == 0 or \
       dut_failures + ref_failures == 0 or dut_successes + ref_successes == 0:
        # If one group has no attempts or no failures/successes, Fisher's exact test is not meaningful.
        # We can still evaluate the % failures criteria if applicable.
        pass # Proceed to p-value calculation, it might still work or return NaN

    odds_ratio, p_value = fisher_exact(table, alternative='less')

    result_string = f" (p-value: {p_value:.4f})"

    # Criteria from the image
    if p_value > 0.99:
        return "PASS (p-value > 0.99)" + result_string
    elif 0.05 <= p_value <= 0.99:
        # Check RED condition for DUT failures < 1%
        dut_failure_percentage = (dut_failures / dut_attempts) * 100 if dut_attempts > 0 else 0
        if dut_failure_percentage < 1:
            return "WARNING (RED condition satisfied: % failures (DUT) < 1%)" + result_string
        else:
            return "WARNING (0.05 <= p-value <= 0.99)" + result_string
    elif p_value < 0.05:
        return "FAIL (p-value < 0.05)" + result_string
    else:
        return "N/A (Could not determine Fisher Exact criteria)" + result_string

def _calculate_call_setup_time_criteria(dut_mean_setup_time, ref_mean_setup_time):
    if dut_mean_setup_time is None or ref_mean_setup_time is None or ref_mean_setup_time == 0:
        return "N/A (Insufficient data for Call Setup Time criteria)"

    ratio = dut_mean_setup_time / ref_mean_setup_time

    if ratio < 1.0:
        return "PASS (Average DUT Setup Time < Average REF Setup Time)"
    elif 1.0 <= ratio < 1.1:
        return "WARNING (Average DUT Setup Time is between 1.0 & 1.1 * Average REF Setup Time)"
    elif 1.1 <= ratio < 1.25:
        return "WARNING (Average DUT Setup Time is between 1.1 & 1.25 * Average REF Setup Time)"
    else: # ratio >= 1.25
        return "FAIL (Average DUT Setup Time > Average REF Setup Time * 1.25)"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python call_analyze.py <path_to_csv_file_or_directory>")
    else:
        input_path = sys.argv[1]
        if os.path.isfile(input_path):
            total_attempts, total_failures, call_result_distribution, rat_distribution, total_setup_duration, setup_duration_count = analyze_call_data(input_path)
            print(f"Analysis for file: {input_path}")
            print(f"Total attempts (Voice calls, excluding 603 Declined sections): {total_attempts}")
            print(f"Total failures (Voice calls, excluding 603 Declined sections): {total_failures}")
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
                _print_analysis_results(dut_results, ref_results) # Pass ref_results for criteria calculation
            
            if ref_results:
                print("\n--- REF Aggregated Analysis Results ---")
                _print_analysis_results(ref_results)

        else:
            print(f"Error: Invalid path provided: {input_path}. Must be a file or a directory.")
