import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
import data_performance_statics
import ping_statics # Import ping_statics for its evaluation logic if needed

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
        
        # Check if it's a Ping analysis result
        if subdir_name.startswith("Ping -"):
            story.append(Paragraph(f"Ping RTT Statistics for: {subdir_name.replace('Ping - ', '')}", styles['h3']))
            
            ping_table_data = [["Device Type", "Statistic", "Value"]]
            
            for device_type, ping_results in results.items():
                ping_rtt_stats = ping_results.get("Ping RTT", {})
                
                min_rtt = ping_rtt_stats.get('min')
                max_rtt = ping_rtt_stats.get('max')
                avg_rtt = ping_rtt_stats.get('avg')
                std_dev_rtt = ping_rtt_stats.get('std_dev')

                # Evaluate performance for Ping RTT
                performance_result = "Unknown"
                if device_type == "DUT" and "REF" in results:
                    ref_ping_rtt_stats = results["REF"].get("Ping RTT", {})
                    ref_avg_rtt = ref_ping_rtt_stats.get('avg')
                    if avg_rtt is not None and ref_avg_rtt is not None:
                        performance_result = data_performance_statics.evaluate_performance(avg_rtt, ref_avg_rtt, "ping_rtt")
                
                result_color = PERFORMANCE_COLORS.get(performance_result, colors.black)

                current_row_idx = len(ping_table_data)
                ping_table_data.append([device_type, "Min RTT", f"{min_rtt:.2f}" if min_rtt is not None else 'N/A'])
                ping_table_data.append(["", "Max RTT", f"{max_rtt:.2f}" if max_rtt is not None else 'N/A'])
                ping_table_data.append(["", "Avg RTT", f"{avg_rtt:.2f}" if avg_rtt is not None else 'N/A'])
                
                # Apply color to Avg RTT row for DUT
                if device_type == "DUT":
                    additional_styles.append(('BACKGROUND', (2, current_row_idx + 2), (2, current_row_idx + 2), result_color))

                ping_table_data.append(["", "Std Dev RTT", f"{std_dev_rtt:.2f}" if std_dev_rtt is not None else 'N/A'])
            
            if len(ping_table_data) > 1:
                ping_table = Table(ping_table_data, colWidths=[1.5*inch, 1.5*inch, 3*inch])
                
                # Base style for ping table
                ping_base_style = [
                    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]
                ping_table.setStyle(TableStyle(ping_base_style + additional_styles))
                story.append(ping_table)
            else:
                story.append(Paragraph("No Ping RTT data found for this subdirectory.", styles['Normal']))
            
            story.append(Spacer(1, 0.5 * inch))
            continue # Move to the next subdir_name

        # Existing data performance analysis logic
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
                    
                    # Helper to format numbers or return 'N/A'
                    def format_stat_value(val):
                        return f"{val:.2f}" if isinstance(val, (int, float)) else 'N/A'

                    table_data.append(["", "Standard Deviation", format_stat_value(dut_metric_stats.get('Standard Deviation')), format_stat_value(ref_metric_stats.get('Standard Deviation'))])
                    table_data.append(["", "Minimum", format_stat_value(dut_metric_stats.get('Minimum')), format_stat_value(ref_metric_stats.get('Minimum'))])
                    table_data.append(["", "Maximum", format_stat_value(dut_metric_stats.get('Maximum')), format_stat_value(ref_metric_stats.get('Maximum'))])
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
