import csv
import argparse
import os

def analyze_coverage_coordinates(file_path):
    """
    Analyzes a CSV file to find the coordinates corresponding to specific events,
    searching from the bottom up. Returns a dictionary of results.
    """
    results = {
        "last_mos_value_coords": None,
        "voice_call_drop_coords": None,
        "first_dl_tp_gt_1_coords": None,
        "first_ul_tp_gt_1_coords": None
    }

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
                print(f"Error: Missing expected header column in {os.path.basename(file_path)}: {e}")
                return results

            rows = list(reader) # Read all rows into a list

            # Helper function to find coordinates
            def _find_coords_in_row_or_upwards(start_index, lat_idx, lon_idx):
                # Check current row
                if len(rows[start_index]) > max(lat_idx, lon_idx) and rows[start_index][lat_idx] and rows[start_index][lon_idx]:
                    return {"latitude": rows[start_index][lat_idx], "longitude": rows[start_index][lon_idx]}
                # Search upwards
                for j in reversed(range(start_index)):
                    prev_row = rows[j]
                    if len(prev_row) > max(lat_idx, lon_idx) and prev_row[lat_idx] and prev_row[lon_idx]:
                        return {"latitude": prev_row[lat_idx], "longitude": prev_row[lon_idx]}
                return None

            # --- Search for Last MOS Value ---
            for i in reversed(range(len(rows))):
                row = rows[i]
                if len(row) > mos_value_col_idx:
                    try:
                        mos_value = float(row[mos_value_col_idx])
                        coords = _find_coords_in_row_or_upwards(i, latitude_col_idx, longitude_col_idx)
                        if coords:
                            results["last_mos_value_coords"] = coords
                        break
                    except ValueError:
                        continue

            # --- Search for Voice Call Drop Event ---
            for i in reversed(range(len(rows))):
                row = rows[i]
                if len(row) > voice_call_event_col_idx and row[voice_call_event_col_idx] == '[Tool] Voice - Call Result : Drop':
                    coords = _find_coords_in_row_or_upwards(i, latitude_col_idx, longitude_col_idx)
                    if coords:
                        results["voice_call_drop_coords"] = coords
                    break

            # --- Search for DL TP ---
            for i in reversed(range(len(rows))):
                row = rows[i]
                if len(row) > dl_tp_col_idx:
                    try:
                        dl_tp_value = float(row[dl_tp_col_idx])
                        if dl_tp_value > 1:
                            coords = _find_coords_in_row_or_upwards(i, latitude_col_idx, longitude_col_idx)
                            if coords:
                                results["first_dl_tp_gt_1_coords"] = coords
                            break
                    except ValueError:
                        continue

            # --- Search for UL TP ---
            for i in reversed(range(len(rows))):
                row = rows[i]
                if len(row) > ul_tp_col_idx:
                    try:
                        ul_tp_value = float(row[ul_tp_col_idx])
                        if ul_tp_value > 1:
                            coords = _find_coords_in_row_or_upwards(i, latitude_col_idx, longitude_col_idx)
                            if coords:
                                results["first_ul_tp_gt_1_coords"] = coords
                            break
                    except ValueError:
                        continue

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred while analyzing {os.path.basename(file_path)}: {e}")

    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze CSV for coverage coordinates based on DL and UL TP.")
    parser.add_argument("file_path", help="Path to the CSV file to analyze.")
    args = parser.parse_args()

    analysis_results = analyze_coverage_coordinates(args.file_path)
    print(json.dumps(analysis_results, indent=4))
