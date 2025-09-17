import pandas as pd
import matplotlib.pyplot as plt
import sys
from analyze_csv import analyze_csv

def draw_table(metrics, output_path="table.png"):
    """
    Draws a table based on the provided metrics and saves it as an image.
    """
    df = pd.DataFrame([metrics])

    # Manually wrap column labels
    wrapped_col_labels = [
        "Device",
        "Connection\nAttempts",
        "Mean Setup\nTime (s)",
        "Successful\nInitiations",
        "Successful\nInitiations\n(%)",
        "Failed\nInitiations",
        "Failed\nInitiations\n(%)",
        "P - Value"
    ]

    fig, ax = plt.subplots(figsize=(30, 18)) # Adjusted figure size: narrower width, taller height
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=df.values,
                     colLabels=wrapped_col_labels,
                     cellLoc='center',
                     loc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(18) # Keep font size
    table.scale(1.1, 5.5) # Adjusted cell scale: narrower width, taller height

    # Set header background color
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_facecolor("#666666") # Dark grey for header
            cell.set_text_props(color='white') # White text for header
        else:
            cell.set_facecolor("#f2f2f2") # Light grey for data rows

    plt.savefig(output_path)
    print(f"Table saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        device_name = "DUT" # This should ideally come from the CSV or an argument
        
        metrics = analyze_csv(file_path)
        metrics["Device"] = device_name # Assign the device name
        
        # Ensure the order of columns matches the image
        ordered_columns = [
            "Device",
            "Connection Attempts",
            "Mean Setup Time (s)",
            "Successful Initiations",
            "Successful Initiations (%)",
            "Failed Initiations",
            "Failed Initiations (%)",
            "P - Value"
        ]
        
        # Create a new dictionary with ordered columns
        ordered_metrics = {col: metrics.get(col, "N/A") for col in ordered_columns}

        draw_table(ordered_metrics)
    else:
        print("Please provide the path to the CSV file as a command-line argument.")
        print("Usage: python Scripts/draw_plot.py <path_to_your_csv_file>")
