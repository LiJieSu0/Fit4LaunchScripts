import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
import data_performance_statics

def create_pdf_report(all_results, output_filename="Data_Performance_Report.pdf"):
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    styles = getSampleStyleSheet()

    # Define custom colors for performance evaluation
    PERFORMANCE_COLORS = {
        "Excellent": colors.magenta,
        "Pass": colors.Color(0.6, 0.98, 0.6), # Custom light green
        "Marginal Fail": colors.yellow,
        "Fail": colors.red,
        "Cannot evaluate: Reference throughput is zero.": colors.lightgrey,
        "Unknown": colors.lightgrey
    }
    story = []

    # Title Page
    story.append(Paragraph("Data Performance Analysis Report", styles['h1']))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("Comparison of DUT and REF Devices", styles['h2']))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph(f"Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 1 * inch))

    for subdir_name, results in all_results.items():
        story.append(Paragraph(f"Analysis for: {subdir_name}", styles['h2']))
        story.append(Spacer(1, 0.2 * inch))

        dut_data = results.get("DUT", {})
        ref_data = results.get("REF", {})

        # Prepare data for the table
        table_data = [["Metric", "Statistic", "DUT Value", "REF Value"]]
        
        metrics = set(list(dut_data.keys()) + list(ref_data.keys()))
        metrics_to_display = ["Throughput", "Jitter", "Error Ratio"] # Order of display

        # List to hold additional styles for coloring
        additional_styles = []
        
        for metric in metrics_to_display:
            if metric in dut_data or metric in ref_data:
                dut_metric_stats = dut_data.get(metric, {})
                ref_metric_stats = ref_data.get(metric, {})

                # Handle Throughput (Mean, Std Dev, Min, Max)
                if metric == "Throughput":
                    dut_mean_tput = dut_metric_stats.get('Mean')
                    ref_mean_tput = ref_metric_stats.get('Mean')
                    
                    # Evaluate performance and get color
                    performance_result = "Unknown"
                    if dut_mean_tput is not None and ref_mean_tput is not None:
                        performance_result = data_performance_statics.evaluate_performance(dut_mean_tput, ref_mean_tput, "throughput")
                    
                    result_color = PERFORMANCE_COLORS.get(performance_result, colors.black) # Default to black if not found

                    # Add Throughput Mean row
                    current_row_idx = len(table_data) # Get current row index before appending
                    table_data.append([metric, "Mean", f"{dut_mean_tput:.2f}" if dut_mean_tput is not None else 'N/A', f"{ref_mean_tput:.2f}" if ref_mean_tput is not None else 'N/A'])
                    
                    # Apply color to DUT Value and REF Value cells for Throughput Mean
                    additional_styles.append(('BACKGROUND', (2, current_row_idx), (2, current_row_idx), result_color))
                    additional_styles.append(('BACKGROUND', (3, current_row_idx), (3, current_row_idx), result_color))
                    
                    table_data.append(["", "Standard Deviation", f"{dut_metric_stats.get('Standard Deviation', 'N/A'):.2f}", f"{ref_metric_stats.get('Standard Deviation', 'N/A'):.2f}"])
                    table_data.append(["", "Minimum", f"{dut_metric_stats.get('Minimum', 'N/A'):.2f}", f"{ref_metric_stats.get('Minimum', 'N/A'):.2f}"])
                    table_data.append(["", "Maximum", f"{dut_metric_stats.get('Maximum', 'N/A'):.2f}", f"{ref_metric_stats.get('Maximum', 'N/A'):.2f}"])
                # Handle Jitter (Mean)
                elif metric == "Jitter":
                    dut_mean_jitter = dut_metric_stats.get('Mean')
                    ref_mean_jitter = ref_metric_stats.get('Mean')

                    # Evaluate performance and get color
                    performance_result = "Unknown"
                    if dut_mean_jitter is not None and ref_mean_jitter is not None:
                        performance_result = data_performance_statics.evaluate_performance(dut_mean_jitter, ref_mean_jitter, "jitter")
                    
                    result_color = PERFORMANCE_COLORS.get(performance_result, colors.black) # Default to black if not found

                    # Add Jitter Mean row
                    current_row_idx = len(table_data) # Get current row index before appending
                    table_data.append([metric, "Mean", f"{dut_mean_jitter:.2f} ms" if dut_mean_jitter is not None else 'N/A', f"{ref_mean_jitter:.2f} ms" if ref_mean_jitter is not None else 'N/A'])
                    
                    # Apply color to DUT Value and REF Value cells for Jitter Mean
                    additional_styles.append(('BACKGROUND', (2, current_row_idx), (2, current_row_idx), result_color))
                    additional_styles.append(('BACKGROUND', (3, current_row_idx), (3, current_row_idx), result_color))

                # Handle Error Ratio (Mean)
                elif metric == "Error Ratio":
                    table_data.append([metric, "Mean", f"{dut_metric_stats.get('Mean', 'N/A'):.2f} %", f"{ref_metric_stats.get('Mean', 'N/A'):.2f} %"])
        
        if len(table_data) > 1: # If there's actual data beyond the header
            table = Table(table_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            
            # Base style
            base_style = [
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]
            
            # Combine base style with additional styles
            table.setStyle(TableStyle(base_style + additional_styles))
            story.append(table)
        else:
            story.append(Paragraph("No comparable data found for this subdirectory.", styles['Normal']))
        
        story.append(Spacer(1, 0.5 * inch)) # Space after each table

    doc.build(story)
    print(f"\nPDF report generated: {output_filename}")
