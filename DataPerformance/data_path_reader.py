import os

def get_csv_file_paths(base_raw_data_dir, directories_config, excluded_analysis_types=None):
    """
    Collects all CSV file paths from the specified directories, excluding those
    with analysis types that are handled separately (e.g., directory-level analysis).

    Args:
        base_raw_data_dir (str): The base directory where raw data is located.
        directories_config (list): A list of dictionaries, where each dictionary
                                   contains "path" (relative to base_raw_data_dir)
                                   and "analysis_type".
        excluded_analysis_types (list, optional): A list of analysis types for which
                                                  individual CSV files should not be collected.
                                                  Defaults to None.

    Returns:
        list: A sorted list of absolute paths to all CSV files found.
    """
    if excluded_analysis_types is None:
        excluded_analysis_types = []

    all_csv_files = []
    
    for dir_info in directories_config:
        if dir_info["analysis_type"] in excluded_analysis_types:
            print(f"Skipping individual CSV collection for directory with analysis type: {dir_info['analysis_type']}")
            continue

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

def write_csv_paths_with_two_parents(csv_file_paths, base_raw_data_dir, output_dir):
    """
    Prints each CSV file's name along with its two parent directories.
    
    Args:
        csv_file_paths (list): A list of absolute paths to CSV files.
        base_raw_data_dir (str): The base directory to consider for relative paths.
        output_dir (str): The directory where the output file should be written.
    """
    if csv_file_paths:
        output_file_path = os.path.join(output_dir, "Discovered Raw Data Paths.txt")
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write("--- Discovered Raw Data Paths (CSV files with their two parent directories): ---\n")
            # Sort the list for consistent output
            sorted_csv_files = sorted(csv_file_paths)
            for csv_file_path in sorted_csv_files:
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
                    f.write(f"- {grandparent_dir}\\{immediate_parent_dir}\\{file_name}\n")
                elif immediate_parent_dir:
                    f.write(f"- {immediate_parent_dir}\\{file_name}\n")
                else:
                    f.write(f"- {file_name}\n")
        print(f"\nSuccessfully wrote discovered raw data paths to {output_file_path}")
    else:
        print("\nNo CSV files were found in the specified directories.")
        print("No Discovered Raw Data Paths.txt file was generated.")

if __name__ == "__main__":
    # Example usage (for testing the script independently)
    base_dir = "Raw Data"
    config = [
        {"path": "5G AUTO DP", "analysis_type": "data_performance"},
        {"path": "5G NSA DP", "analysis_type": "data_performance"},
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
    # For independent testing, define a dummy output_dir
    test_output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "TestOutput")
    os.makedirs(test_output_dir, exist_ok=True)
    write_csv_paths_with_two_parents(csv_files, base_dir, test_output_dir) # Call the modified function
