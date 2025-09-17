import os
import subprocess
import sys

def run_analysis_on_all_csvs(data_directory, analysis_script_path):
    """
    Iterates through all CSV files in the specified directory and runs the analysis script on each.
    """
    print(f"Starting analysis for all CSV files in: {data_directory}")
    print(f"Using analysis script: {analysis_script_path}\n")

    csv_files_found = False
    # Only list files in the specified directory, not recursively
    for file in os.listdir(data_directory):
        if file.lower().endswith(".csv"):
            csv_file_path = os.path.join(data_directory, file)
            csv_files_found = True
            print(f"--- Analyzing file: {csv_file_path} ---")
            
            try:
                # Construct the command to run data_performance_statics.py
                # Ensure the script path is relative to the current working directory
                # and the CSV file path is also correctly handled (with quotes for spaces)
                command = [
                    sys.executable, # Use the current Python interpreter
                    analysis_script_path,
                    csv_file_path
                ]
                
                # Execute the command and capture output
                result = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
                print(result.stdout)
                if result.stderr:
                    print(f"Error output for {csv_file_path}:\n{result.stderr}")
            except subprocess.CalledProcessError as e:
                print(f"Error running analysis for {csv_file_path}:")
                print(f"Command: {' '.join(e.cmd)}")
                print(f"Return Code: {e.returncode}")
                print(f"Output:\n{e.stdout}")
                print(f"Error:\n{e.stderr}")
            except FileNotFoundError:
                print(f"Error: The analysis script '{analysis_script_path}' was not found.")
                return
            print("-" * 50 + "\n") # Separator for readability

    if not csv_files_found:
        print(f"No CSV files found in the directory: {data_directory}")

if __name__ == "__main__":
    # Assuming the new script is in Scripts/DataPerformance/
    # and data_performance_statics.py is in the same directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    analysis_script_path = os.path.join(script_dir, "data_performance_statics.py")
    
    # The user specified D:\Fit4Launch\RawData\Data.
    data_to_analyze_dir = os.path.join("RawData", "Data") # Relative path from d:\Fit4Launch

    if not os.path.exists(analysis_script_path):
        print(f"Error: Analysis script not found at {analysis_script_path}")
        sys.exit(1)
    if not os.path.isdir(data_to_analyze_dir):
        print(f"Error: Data directory not found at {data_to_analyze_dir}")
        sys.exit(1)

    run_analysis_on_all_csvs(data_to_analyze_dir, analysis_script_path)
