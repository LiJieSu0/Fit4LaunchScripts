import json
import os

def check_empty_collections(data, path_parts=None, empty_collections_found=None):
    """
    Recursively checks for empty dictionaries or lists within the given data.
    Stores the hierarchical path to any empty collection found.
    """
    if path_parts is None:
        path_parts = []
    if empty_collections_found is None:
        empty_collections_found = []

    if isinstance(data, dict):
        if not data:
            empty_collections_found.append(path_parts + ["Empty Dictionary"])
        for key, value in data.items():
            check_empty_collections(value, path_parts + [key], empty_collections_found)
    elif isinstance(data, list):
        if not data:
            empty_collections_found.append(path_parts + ["Empty List"])
        for index, item in enumerate(data):
            check_empty_collections(item, path_parts + [f"[{index}]"], empty_collections_found)
    return empty_collections_found

def main():
    json_file_path = "React/frontend/src/data_analysis_results.json"
    output_file_path = "Scripts/Empty_Json.txt" # Updated path

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Checking '{json_file_path}' for empty collections...")
        empty_collections = check_empty_collections(data)
        
        if empty_collections:
            with open(output_file_path, 'w', encoding='utf-8') as out_f:
                out_f.write("Empty collections found in JSON:\n")
                for item_path in empty_collections:
                    for i, part in enumerate(item_path):
                        out_f.write("    " * i + f"- {part}\n")
            print(f"Empty collections found. Details written to '{output_file_path}'.")
        else:
            print("No empty collections found.")
        
        print("Check complete.")
        
    except FileNotFoundError:
        print(f"Error: The file '{json_file_path}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{json_file_path}'. Check file format.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
