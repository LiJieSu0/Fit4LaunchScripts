import csv
import argparse

def analyze_coverage_coordinates(file_path):
    """
    Analyzes a CSV file to find the coordinates corresponding to the first
    '[Call Test] [Throughput] Application DL TP' value greater than 1,
    searching from the bottom up.
    """
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # Read the header row

            # Find column indices
            try:
                dl_tp_col_idx = header.index('[Call Test] [Throughput] Application DL TP')
                ul_tp_col_idx = header.index('[Call Test] [Throughput] Application UL TP')
                voice_call_event_col_idx = header.index('[Event] Voice Call Event')
                mos_value_col_idx = header.index('[Call Test] [Voice Quality] [Per Rx Clip] MOS Value')
                latitude_col_idx = header.index('[General] [GPS] Latitude')
                longitude_col_idx = header.index('[General] [GPS] Longitude')
            except ValueError as e:
                print(f"Error: Missing expected header column: {e}")
                return

            rows = list(reader) # Read all rows into a list

            # --- Search for Last MOS Value ---
            found_mos_value = False
            for i in reversed(range(len(rows))):
                row = rows[i]
                if len(row) > mos_value_col_idx:
                    try:
                        mos_value = float(row[mos_value_col_idx])
                        print(f"--- MOS Value Analysis ---")
                        print(f"Found last MOS Value (value: {mos_value}) at row index {i}.")

                        # Check current row for coordinates
                        if len(row) > max(latitude_col_idx, longitude_col_idx) and row[latitude_col_idx] and row[longitude_col_idx]:
                            latitude = row[latitude_col_idx]
                            longitude = row[longitude_col_idx]
                            print(f"Coordinates at last MOS value: Latitude: {latitude}, Longitude: {longitude}")
                            found_mos_value = True
                            break
                        else:
                            print("Coordinates not available in the same row as the last MOS value. Searching upwards for nearest coordinates...")
                            # Search upwards for nearest valid coordinates
                            for j in reversed(range(i)):
                                prev_row = rows[j]
                                if len(prev_row) > max(latitude_col_idx, longitude_col_idx) and prev_row[latitude_col_idx] and prev_row[longitude_col_idx]:
                                    latitude = prev_row[latitude_col_idx]
                                    longitude = prev_row[longitude_col_idx]
                                    print(f"Nearest coordinates found at row index {j}: Latitude: {latitude}, Longitude: {longitude}")
                                    found_mos_value = True
                                    break
                            if not found_mos_value:
                                print("No valid coordinates found upwards from the last MOS value.")
                        break # Exit after finding the last MOS value
                    except ValueError:
                        # Not a valid float, continue searching upwards
                        continue
                else:
                    print(f"Warning: Row has fewer columns than expected for MOS Value: {row}")

            if not found_mos_value:
                print("No '[Call Test] [Voice Quality] [Per Rx Clip] MOS Value' found in the file.")

            print("\n") # Add a newline for separation

            # --- Search for Voice Call Drop Event ---
            found_drop_event = False
            for i in reversed(range(len(rows))):
                row = rows[i]
                if len(row) > voice_call_event_col_idx and row[voice_call_event_col_idx] == '[Tool] Voice - Call Result : Drop':
                    print(f"--- Voice Call Drop Event Analysis ---")
                    print(f"Found '[Tool] Voice - Call Result : Drop' at row index {i}.")

                    # Check current row for coordinates
                    if len(row) > max(latitude_col_idx, longitude_col_idx) and row[latitude_col_idx] and row[longitude_col_idx]:
                        latitude = row[latitude_col_idx]
                        longitude = row[longitude_col_idx]
                        print(f"Coordinates at drop event: Latitude: {latitude}, Longitude: {longitude}")
                        found_drop_event = True
                        break
                    else:
                        print("Coordinates not available in the same row as the drop event. Searching upwards for nearest coordinates...")
                        # Search upwards for nearest valid coordinates
                        for j in reversed(range(i)):
                            prev_row = rows[j]
                            if len(prev_row) > max(latitude_col_idx, longitude_col_idx) and prev_row[latitude_col_idx] and prev_row[longitude_col_idx]:
                                latitude = prev_row[latitude_col_idx]
                                longitude = prev_row[longitude_col_idx]
                                print(f"Nearest coordinates found at row index {j}: Latitude: {latitude}, Longitude: {longitude}")
                                found_drop_event = True
                                break
                        if not found_drop_event:
                            print("No valid coordinates found upwards from the drop event.")
                    break # Exit after finding the first drop event

            if not found_drop_event:
                print("No '[Tool] Voice - Call Result : Drop' event found in the file.")

            print("\n") # Add a newline for separation

            # --- Search for DL TP ---
            found_dl = False
            for row in reversed(rows):
                if len(row) > max(dl_tp_col_idx, latitude_col_idx, longitude_col_idx):
                    try:
                        dl_tp_value = float(row[dl_tp_col_idx])
                        if dl_tp_value > 1:
                            latitude = row[latitude_col_idx]
                            longitude = row[longitude_col_idx]
                            print(f"--- DL TP Analysis ---")
                            print(f"Found first DL TP > 1 (value: {dl_tp_value}):")
                            print(f"Latitude: {latitude}")
                            print(f"Longitude: {longitude}")
                            found_dl = True
                            break
                    except ValueError:
                        continue
                else:
                    print(f"Warning: Row has fewer columns than expected for DL TP: {row}")
            if not found_dl:
                print("No '[Call Test] [Throughput] Application DL TP' value > 1 found in the file.")

            print("\n") # Add a newline for separation

            # --- Search for UL TP ---
            found_ul = False
            for row in reversed(rows):
                if len(row) > max(ul_tp_col_idx, latitude_col_idx, longitude_col_idx):
                    try:
                        ul_tp_value = float(row[ul_tp_col_idx])
                        if ul_tp_value > 1:
                            latitude = row[latitude_col_idx]
                            longitude = row[longitude_col_idx]
                            print(f"--- UL TP Analysis ---")
                            print(f"Found first UL TP > 1 (value: {ul_tp_value}):")
                            print(f"Latitude: {latitude}")
                            print(f"Longitude: {longitude}")
                            found_ul = True
                            break
                    except ValueError:
                        continue
                else:
                    print(f"Warning: Row has fewer columns than expected for UL TP: {row}")
            if not found_ul:
                print("No '[Call Test] [Throughput] Application UL TP' value > 1 found in the file.")


    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze CSV for coverage coordinates based on DL and UL TP.")
    parser.add_argument("file_path", help="Path to the CSV file to analyze.")
    args = parser.parse_args()

    analyze_coverage_coordinates(args.file_path)
