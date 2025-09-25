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

def analyze_call_data(file_path):
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    # Apply the cleaning function to all column names in the DataFrame
    df.columns = [_clean_header(col) for col in df.columns]

    # Define cleaned header names
    packet_data_sip_request_method_col = _clean_header('[Packet Data] [SIP] Request Method')
    event_voice_call_event_col = _clean_header('[Event] Voice Call Event')
    sip_setup_duration_col = _clean_header('[Call Test] [VoNR VoLTE] [Duration] SIP Setup Duration (Invite~200OK)')
    packet_data_sip_status_col = _clean_header('[Packet Data] [SIP] Status')

    # Initialize a column to mark rows for exclusion
    df['exclude_from_stats'] = False

    # Find all occurrences of 'Voice - Call Scheduling Start(Orig)'
    # Escaping parentheses to treat them as literal characters, and using regex=True explicitly
    start_indices = df[df[event_voice_call_event_col].astype(str).str.contains(r'Voice - Call Scheduling Start\(Orig\)', na=False, regex=True)].index.tolist()
    print(f"Found {len(start_indices)} 'Voice - Call Scheduling Start(Orig)' events at indices: {start_indices}")

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
            print(f"Marking rows from index {start_idx} to {end_idx} for exclusion due to '603 Declined' in section.")
        else:
            print(f"Section from index {start_idx} to {end_idx} does not contain '603 Declined'.")

    # Filter out the rows marked for exclusion
    df_filtered = df[~df['exclude_from_stats']]
    print(f"Total rows in original DataFrame: {len(df)}")
    print(f"Total rows marked for exclusion: {df['exclude_from_stats'].sum()}")
    print(f"Total rows after exclusion: {len(df_filtered)}")

    # 1. Total attempts: Count 'INVITE' in cleaned '[Packet Data] [SIP] Request Method'
    total_attempts = df_filtered[packet_data_sip_request_method_col].astype(str).str.contains('INVITE').sum()

    # 2. Success initiation: Count 'Setup Success' in cleaned '[Event] Voice Call Event'
    success_initiation = df_filtered[event_voice_call_event_col].astype(str).str.contains('Setup Success').sum()

    # 3. Mean setup Time: Average of cleaned '[Call Test] [VoNR VoLTE] [Duration] SIP Setup Duration (Invite~200OK)'
    # Convert to numeric, coercing errors to NaN, then drop NaNs before calculating mean
    mean_setup_time = df_filtered[sip_setup_duration_col].apply(pd.to_numeric, errors='coerce').dropna().mean()

    # 4. Success Rate: success initiation / total attempts
    success_rate = (success_initiation / total_attempts) * 100 if total_attempts > 0 else 0

    # 5. Fail attempts: total attempts - success initiation
    fail_attempts = total_attempts - success_initiation

    print(f"Analysis for file: {file_path}")
    print(f"Total attempts (excluding 603 Declined sections): {total_attempts}")
    print(f"Success initiation (excluding 603 Declined sections): {success_initiation}")
    print(f"Fail attempts (excluding 603 Declined sections): {fail_attempts}")
    print(f"Mean setup Time (excluding 603 Declined sections): {mean_setup_time:.2f} (seconds)")
    print(f"Success Rate (excluding 603 Declined sections): {success_rate:.2f}%")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python call_analyze.py <path_to_csv_file>")
    else:
        csv_file_path = sys.argv[1]
        analyze_call_data(csv_file_path)
