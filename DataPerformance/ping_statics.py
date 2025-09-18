import pandas as pd

def calculate_ping_statistics(file_path):
    """
    Calculates Ping RTT statistics from a given CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        dict: A dictionary containing the calculated statistics (min, max, avg, std dev).
    """
    df = pd.read_csv(file_path)

    rtt_values = []
    in_ping_traffic_block = False

    for index, row in df.iterrows():
        event = row.get('[Event] [Data call test detail events] Ping Call Event')
        rtt = row.get('[Call Test] [PING] [RTT] RTT')

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
