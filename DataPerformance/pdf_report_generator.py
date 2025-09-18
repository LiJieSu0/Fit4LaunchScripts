import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch

def create_pdf_report(all_results, output_filename="Data_Performance_Report.pdf"):
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    styles = getSampleStyleSheet()
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

        for metric in metrics_to_display:
            if metric in dut_data or metric in ref_data:
                dut_metric_stats = dut_data.get(metric, {})
                ref_metric_stats = ref_data.get(metric, {})

                # Handle Throughput (Mean, Std Dev, Min, Max)
                if metric == "Throughput":
                    table_data.append([metric, "Mean", f"{dut_metric_stats.get('Mean', 'N/A'):.2f}", f"{ref_metric_stats.get('Mean', 'N/A'):.2f}"])
                    table_data.append(["", "Standard Deviation", f"{dut_metric_stats.get('Standard Deviation', 'N/A'):.2f}", f"{ref_metric_stats.get('Standard Deviation', 'N/A'):.2f}"])
                    table_data.append(["", "Minimum", f"{dut_metric_stats.get('Minimum', 'N/A'):.2f}", f"{ref_metric_stats.get('Minimum', 'N/A'):.2f}"])
                    table_data.append(["", "Maximum", f"{dut_metric_stats.get('Maximum', 'N/A'):.2f}", f"{ref_metric_stats.get('Maximum', 'N/A'):.2f}"])
                # Handle Jitter (Mean)
                elif metric == "Jitter":
                    table_data.append([metric, "Mean", f"{dut_metric_stats.get('Mean', 'N/A'):.2f} ms", f"{ref_metric_stats.get('Mean', 'N/A'):.2f} ms"])
                # Handle Error Ratio (Mean)
                elif metric == "Error Ratio":
                    table_data.append([metric, "Mean", f"{dut_metric_stats.get('Mean', 'N/A'):.2f} %", f"{ref_metric_stats.get('Mean', 'N/A'):.2f} %"])
        
        if len(table_data) > 1: # If there's actual data beyond the header
            table = Table(table_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            story.append(table)
        else:
            story.append(Paragraph("No comparable data found for this subdirectory.", styles['Normal']))
        
        story.append(Spacer(1, 0.5 * inch)) # Space after each table

    doc.build(story)
    print(f"\nPDF report generated: {output_filename}")
