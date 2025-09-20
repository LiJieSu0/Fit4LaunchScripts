import os

def get_csv_file_paths(base_raw_data_dir, directories_config):
    """
    Collects all CSV file paths from the specified directories.

    Args:
        base_raw_data_dir (str): The base directory where raw data is located.
        directories_config (list): A list of dictionaries, where each dictionary
                                   contains "path" (relative to base_raw_data_dir)
                                   and "analysis_type".

    Returns:
        list: A sorted list of absolute paths to all CSV files found.
    """
    all_csv_files = []
    
    for dir_info in directories_config:
        current_dir_relative_path = dir_info["path"]
        current_dir_full_path = os.path.join(base_raw_data_dir, current_dir_relative_path)
        
        if os.path.isdir(current_dir_full_path):
            for root, _, files in os.walk(current_dir_full_path):
                for file in files:
                    if file.lower().endswith(".csv"):
                        csv_file_path = os.path.join(root, file)
                        all_csv_files.append(csv_file_path)
        else:
            print(f"Warning: Directory not found at {current_dir_full_path}. Skipping.")
            
    return sorted(all_csv_files)

def print_csv_paths_with_two_parents(csv_file_paths, base_raw_data_dir):
    """
    Prints each CSV file's name along with its two parent directories.
    
    Args:
        csv_file_paths (list): A list of absolute paths to CSV files.
        base_raw_data_dir (str): The base directory to consider for relative paths.
    """
    if csv_file_paths:
        print("\n--- CSV files with their two parent directories: ---")
        for csv_file_path in csv_file_paths:
            # Make path relative to base_raw_data_dir first for consistent output
            relative_path = os.path.relpath(csv_file_path, base_raw_data_dir)
            
            # Split the relative path into components
            path_components = relative_path.split(os.sep)
            
            # Get the filename
            file_name = path_components[-1]
            
            # Get the immediate parent directory name
            immediate_parent_dir = path_components[-2] if len(path_components) >= 2 else ""
            
            # Get the grandparent directory name
            grandparent_dir = path_components[-3] if len(path_components) >= 3 else ""
            
            # Construct the desired output string
            if grandparent_dir:
                print(f"- {grandparent_dir}\\{immediate_parent_dir}\\{file_name}")
            elif immediate_parent_dir:
                print(f"- {immediate_parent_dir}\\{file_name}")
            else:
                print(f"- {file_name}")
    else:
        print("\nNo CSV files were found in the specified directories.")

if __name__ == "__main__":
    # Example usage (for testing the script independently)
    base_dir = "Raw Data"
    config = [
        {"path": os.path.join(base_dir, "5G AUTO DP"), "analysis_type": "data_performance"},
        {"path": os.path.join(base_dir, "5G NSA DP"), "analysis_type": "data_performance"},
    ]
    
    # Ensure the base_dir exists for testing
    if not os.path.exists(base_dir):
        print(f"Creating dummy directory: {base_dir}")
        os.makedirs(os.path.join(base_dir, "5G AUTO DP", "Test1"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, "5G NSA DP", "Test2"), exist_ok=True)
        with open(os.path.join(base_dir, "5G AUTO DP", "Test1", "dummy_auto.csv"), "w") as f:
            f.write("header\n1,2,3")
        with open(os.path.join(base_dir, "5G NSA DP", "Test2", "dummy_nsa.csv"), "w") as f:
            f.write("header\n4,5,6")
        print("Dummy CSV files created for testing.")

    csv_files = get_csv_file_paths(base_dir, config)
    print_csv_paths_with_two_parents(csv_files, base_dir)
