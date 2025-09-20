import os
import re
from DataPerformance.data_path_reader import get_csv_file_paths

def remove_timestamp_from_filename(filename):
    """
    Removes a timestamp in the format _YYYYMMDD_HHMMSS_ from a filename.
    """
    # Regex to find the timestamp pattern: _YYYYMMDD_HHMMSS_
    # It looks for an underscore, followed by 8 digits (date),
    # another underscore, 6 digits (time), and a final underscore.
    pattern = r"_\d{8}_\d{6}_"
    new_filename = re.sub(pattern, "_", filename)
    return new_filename

if __name__ == "__main__":
    base_dir = "Raw Data"
    config = [
        {"path": "5G AUTO DP", "analysis_type": "data_performance"},
        {"path": "5G NSA DP", "analysis_type": "data_performance"},
        {"path": "Call Performance", "analysis_type": "call_performance"},
    ]

    csv_files_to_rename = get_csv_file_paths(base_dir, config)

    for original_filepath in csv_files_to_rename:
        # Extract just the filename from the full path
        dirpath, filename = os.path.split(original_filepath)

        if re.search(r"_\d{8}_\d{6}_", filename):  # Check if the filename contains a timestamp
            new_filename = remove_timestamp_from_filename(filename)
            new_filepath = os.path.join(dirpath, new_filename)

            if os.path.exists(new_filepath) and original_filepath != new_filepath:
                print(f"Skipping rename for {original_filepath}: Target file {new_filepath} already exists.")
                continue # Skip this file to avoid collision
            
            try:
                os.rename(original_filepath, new_filepath)
                print(f"Renamed: {original_filepath} -> {new_filepath}")
            except OSError as e:
                print(f"Error renaming {original_filepath}: {e}")
