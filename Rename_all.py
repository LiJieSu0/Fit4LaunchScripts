import os
import re

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
    root_dir = "Raw Data/"  # Specify the root directory to start renaming from

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if re.search(r"_\d{8}_\d{6}_", filename):  # Check if the filename contains a timestamp
                original_filepath = os.path.join(dirpath, filename)
                new_filename = remove_timestamp_from_filename(filename)
                new_filepath = os.path.join(dirpath, new_filename)

                try:
                    os.rename(original_filepath, new_filepath)
                    print(f"Renamed: {original_filepath} -> {new_filepath}")
                except OSError as e:
                    print(f"Error renaming {original_filepath}: {e}")
