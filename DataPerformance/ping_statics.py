import pandas as pd

def calculate_ping_statistics(file_path):
    """
    Calculates Ping RTT statistics from a given CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        dict: A dictionary containing the calculated statistics (min, max, avg, std dev).
    """
    try:
        # Attempt to read with default comma delimiter
        df = pd.read_csv(file_path)
    except pd.errors.ParserError:
        # If parsing fails, try with whitespace as a delimiter and no header
        print(f"Warning: ParserError with default CSV read for {file_path}. Attempting with whitespace delimiter and no header.")
        try:
            df = pd.read_csv(file_path, sep='\s+', header=None)
            # If successful, we need to re-evaluate column names or indices
            # For now, let's assume RTT is in a known column index if header is None
            # This part might need further refinement based on actual file structure
            # For demonstration, let's assume RTT is in the 5th column (index 4) and event in 1st (index 0)
            # This is a placeholder and might need adjustment based on actual data.
            # If the file has a header but pandas misinterprets it, skiprows might be needed.
            # For now, let's try to proceed with the original column names, hoping the sep='\s+' fixes it.
            # If header=None, then column names will be integers.
            # This is a tricky part without knowing the exact file structure.
            # Let's revert to a more general approach: try to find the columns by name first,
            # if that fails, then try by index if header=None.
            pass # We'll handle column access below
        except Exception as e:
            print(f"Error: Failed to parse {file_path} even with whitespace delimiter: {e}")
            return {"min": None, "max": None, "avg": None, "std_dev": None}
    except Exception as e:
        print(f"Error: An unexpected error occurred while reading {file_path}: {e}")
        return {"min": None, "max": None, "avg": None, "std_dev": None}

    rtt_values = []
    in_ping_traffic_block = False

    # Dynamically determine column names or indices
    event_col_name = '[Event] [Data call test detail events] Ping Call Event'
    rtt_col_name = '[Call Test] [PING] [RTT] RTT'

    # Check if original column names exist
    if event_col_name not in df.columns or rtt_col_name not in df.columns:
        print(f"Warning: Original column names not found in {file_path}. Attempting to infer or use default indices.")
        # This is a heuristic. Without knowing the file structure, this is a guess.
        # Assuming event is first column (index 0) and RTT is second (index 1) if no header.
        if df.shape[1] >= 2: # Ensure there are at least two columns
            event_col_name = df.columns[0]
            rtt_col_name = df.columns[1]
            print(f"Using inferred columns: Event='{event_col_name}', RTT='{rtt_col_name}'")
        else:
            print(f"Error: Could not infer event and RTT columns for {file_path}. Skipping.")
            return {"min": None, "max": None, "avg": None, "std_dev": None}

    for index, row in df.iterrows():
        event = row.get(event_col_name)
        rtt = row.get(rtt_col_name)

        if event == 'PING Traffic Start':
            in_ping_traffic_block = True
        elif event == 'PING Traffic End':
            in_ping_traffic_block = False
        elif in_ping_traffic_block and pd.notna(rtt):
            try:
                rtt_values.append(float(rtt))
            except ValueError:
                # Handle cases where RTT might not be a valid number
                pass

    if not rtt_values:
        return {"min": None, "max": None, "avg": None, "std_dev": None}

    min_rtt = min(rtt_values)
    max_rtt = max(rtt_values)
    avg_rtt = sum(rtt_values) / len(rtt_values)
    std_dev_rtt = pd.Series(rtt_values).std()

    return {
        "min": min_rtt,
        "max": max_rtt,
        "avg": avg_rtt,
        "std_dev": std_dev_rtt
    }

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate Ping RTT statistics from a CSV file.")
    parser.add_argument("file_path", type=str, help="The path to the CSV file.")
    args = parser.parse_args()

    ping_stats = calculate_ping_statistics(args.file_path)

    if ping_stats["min"] is not None:
        print("Ping RTT Statistics:")
        print(f"  Min RTT: {ping_stats['min']:.2f}")
        print(f"  Max RTT: {ping_stats['max']:.2f}")
        print(f"  Avg RTT: {ping_stats['avg']:.2f}")
        print(f"  Std Dev RTT: {ping_stats['std_dev']:.2f}")
    else:
        print(f"No RTT values found within 'PING Traffic Start' and 'PING Traffic End' blocks for file: {args.file_path}")
