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

    # 1. Total attempts: Count 'INVITE' in cleaned '[Packet Data] [SIP] Request Method'
    total_attempts = df[packet_data_sip_request_method_col].astype(str).str.contains('INVITE').sum()

    # 2. Success initiation: Count 'Setup Success' in cleaned '[Event] Voice Call Event'
    success_initiation = df[event_voice_call_event_col].astype(str).str.contains('Setup Success').sum()

    # 3. Mean setup Time: Average of cleaned '[Call Test] [VoNR VoLTE] [Duration] SIP Setup Duration (Invite~200OK)'
    # Convert to numeric, coercing errors to NaN, then drop NaNs before calculating mean
    mean_setup_time = df[sip_setup_duration_col].apply(pd.to_numeric, errors='coerce').dropna().mean()

    # 4. Success Rate: success initiation / total attempts
    success_rate = (success_initiation / total_attempts) * 100 if total_attempts > 0 else 0

    # 5. Fail attempts: total attempts - success initiation
    fail_attempts = total_attempts - success_initiation

    print(f"Analysis for file: {file_path}")
    print(f"Total attempts: {total_attempts}")
    print(f"Success initiation: {success_initiation}")
    print(f"Fail attempts: {fail_attempts}")
    print(f"Mean setup Time: {mean_setup_time:.2f} (seconds)")
    print(f"Success Rate: {success_rate:.2f}%")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python call_analyze.py <path_to_csv_file>")
    else:
        csv_file_path = sys.argv[1]
        analyze_call_data(csv_file_path)
