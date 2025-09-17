import pandas as pd
import matplotlib.pyplot as plt
import sys
from analyze_csv import analyze_csv
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def draw_table(metrics, title, output_path):
    """
    Draws a table based on the provided metrics and saves it as an image.
    """
    df = pd.DataFrame([metrics])

    # Determine column labels based on the metrics provided
    if title == "Table 1: Call Statistics":
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
    elif title == "Table 2: Failed Call Details and Network Types":
        wrapped_col_labels = [
            "Failed\nAttempts",
            "No Service",
            "Access\nTimeout",
            "Voicemail",
            "Busy",
            "Unreachable",
            "VoNR",
            "VoLTE",
            "EPSFB",
            "Unknown"
        ]
    else:
        wrapped_col_labels = list(metrics.keys()) # Fallback

    fig, ax = plt.subplots(figsize=(30, 18))
    ax.axis('tight')
    ax.axis('off')

    # Add title to the plot
    ax.set_title(title, fontsize=24, pad=20)

    table = ax.table(cellText=df.values,
                     colLabels=wrapped_col_labels,
                     cellLoc='center',
                     loc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(18)
    table.scale(1.1, 5.5)

    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_facecolor("#666666")
            cell.set_text_props(color='white')
        else:
            cell.set_facecolor("#f2f2f2")

    plt.savefig(output_path)
    print(f"Table saved to {output_path}")
    plt.close(fig) # Close the figure to free memory

def create_pdf_from_images(image_paths, output_pdf_path):
    """
    Combines multiple image files into a single PDF.
    """
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    width, height = letter

    # Assuming two images for two tables
    if len(image_paths) == 2:
        img1 = Image.open(image_paths[0])
        img2 = Image.open(image_paths[1])

        img1_width, img1_height = img1.size
        img2_width, img2_height = img2.size

        # Calculate scaling factor for both images to fit vertically on one page
        # Calculate scaling factor for both images to fit vertically on one page
        # Allow for some margin and spacing
        top_margin = 50
        bottom_margin = 50
        gap = 30
        
        available_height = height - top_margin - bottom_margin - gap
        max_img_height = available_height / 2

        scale_factor1 = min(width / img1_width, max_img_height / img1_height)
        scaled_width1 = img1_width * scale_factor1
        scaled_height1 = img1_height * scale_factor1

        scale_factor2 = min(width / img2_width, max_img_height / img2_height)
        scaled_width2 = img2_width * scale_factor2
        scaled_height2 = img2_height * scale_factor2

        # Position for the first image (top)
        x1_offset = (width - scaled_width1) / 2
        y1_offset = height - top_margin - scaled_height1

        # Position for the second image (below the first)
        x2_offset = (width - scaled_width2) / 2
        y2_offset = y1_offset - gap - scaled_height2

        c.drawImage(image_paths[0], x1_offset, y1_offset, width=scaled_width1, height=scaled_height1)
        c.drawImage(image_paths[1], x2_offset, y2_offset, width=scaled_width2, height=scaled_height2)
        c.showPage()
    else:
        # Fallback for single or more than two images (original behavior)
        for img_path in image_paths:
            img = Image.open(img_path)
            img_width, img_height = img.size

            scale_factor = min(width / img_width, height / img_height)
            scaled_width = img_width * scale_factor
            scaled_height = img_height * scale_factor

            x_offset = (width - scaled_width) / 2
            y_offset = (height - scaled_height) / 2

            c.drawImage(img_path, x_offset, y_offset, width=scaled_width, height=scaled_height)
            c.showPage()
    
    c.save()
    print(f"PDF saved to {output_pdf_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        device_name = "DUT"
        
        table1_metrics, table2_metrics = analyze_csv(file_path)
        table1_metrics["Device"] = device_name

        # Ensure the order of columns for table1_metrics
        ordered_columns_table1 = [
            "Device",
            "Connection Attempts",
            "Mean Setup Time (s)",
            "Successful Initiations",
            "Successful Initiations (%)",
            "Failed Initiations",
            "Failed Initiations (%)",
            "P - Value"
        ]
        ordered_table1_metrics = {col: table1_metrics.get(col, "N/A") for col in ordered_columns_table1}

        # Ensure the order of columns for table2_metrics
        ordered_columns_table2 = [
            "Failed Attempts",
            "No Service",
            "Access Timeout",
            "Voicemail",
            "Busy",
            "Unreachable",
            "VoNR",
            "VoLTE",
            "EPSFB",
            "Unknown"
        ]
        ordered_table2_metrics = {col: table2_metrics.get(col, "N/A") for col in ordered_columns_table2}

        # Draw tables
        table1_output_path = "table1.png"
        table2_output_path = "table2.png"
        draw_table(ordered_table1_metrics, "Table 1: Call Statistics", table1_output_path)
        draw_table(ordered_table2_metrics, "Table 2: Failed Call Details and Network Types", table2_output_path)

        # Create PDF
        output_pdf_path = "statistical_report.pdf"
        create_pdf_from_images([table1_output_path, table2_output_path], output_pdf_path)
    else:
        print("Please provide the path to the CSV file as a command-line argument.")
        print("Usage: python Scripts/draw_plot.py <path_to_your_csv_file>")
