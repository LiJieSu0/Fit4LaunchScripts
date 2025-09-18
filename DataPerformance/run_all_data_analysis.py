import os
import subprocess
import sys
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch

# Import the analysis functions from data_performance_statics.py
# Assuming data_performance_statics.py is in the same directory
import data_performance_statics

def run_analysis_on_file(file_path, analysis_script_path):
    """
    Runs the analysis script on a single CSV file and returns the collected statistics.
    """
    file_name = os.path.basename(file_path).lower()
    event_col = None
    start_event = None
    end_event = None
    analysis_direction_detected = None
    protocol_type_detected = None
    network_type_detected = None
    device_type_detected = "Unknown"

    if "ul" in file_name:
        analysis_direction_detected = "UL"
    elif "dl" in file_name:
        analysis_direction_detected = "DL"
    
    if "http" in file_name:
        protocol_type_detected = "HTTP"
    elif "udp" in file_name:
        protocol_type_detected = "UDP"
    
    if "5g" in file_name:
        network_type_detected = "5G"
    elif "lte" in file_name:
        network_type_detected = "LTE"

    if "dut" in file_name:
        device_type_detected = "DUT"
    elif "ref" in file_name:
        device_type_detected = "REF"

    if not analysis_direction_detected or not protocol_type_detected or not network_type_detected:
        print(f"Warning: Could not fully determine analysis parameters from filename: {file_name}. Skipping.")
        return None

    all_stats = {}
    all_stats["Device Type"] = device_type_detected
    all_stats["Analysis Direction"] = analysis_direction_detected
    all_stats["Protocol Type"] = protocol_type_detected
    all_stats["Network Type"] = network_type_detected

    if protocol_type_detected == "HTTP":
        event_col = "[Call Test] [HTTP Transfer] HTTP Transfer Call Event"
        if analysis_direction_detected == "DL":
            column_to_analyze = "[Call Test] [Throughput] Application DL TP" if network_type_detected == "5G" else "[LTE] [Data Throughput] [Downlink (All)] [PDSCH] PDSCH TP (Total)"
            start_event = "Download Started"
            end_event = "Download Ended"
            throughput_stats = data_performance_statics.analyze_throughput(file_path, column_to_analyze, event_col, start_event, end_event)
            if throughput_stats:
                all_stats["Throughput"] = throughput_stats
        elif analysis_direction_detected == "UL":
            column_to_analyze = "[LTE] [Data Throughput] [Uplink (All)] [PUSCH] PUSCH TP (Total)"
            start_event = "Upload Started"
            end_event = "Upload Ended"
            throughput_stats = data_performance_statics.analyze_throughput(file_path, column_to_analyze, event_col, start_event, end_event)
            if throughput_stats:
                all_stats["Throughput"] = throughput_stats
    elif protocol_type_detected == "UDP":
        event_col = "[Event] [Data call test detail events] IPERF Call Event"
        start_event = "IPERF_T_Start"
        end_event = "IPERF_T_End"

        if analysis_direction_detected == "DL":
            column_to_analyze_throughput = "[Call Test] [Throughput] Application DL TP" if network_type_detected == "5G" else "[LTE] [Data Throughput] [Downlink (All)] [PDSCH] PDSCH TP (Total)"
            throughput_stats = data_performance_statics.analyze_throughput(file_path, column_to_analyze_throughput, event_col, start_event, end_event)
            if throughput_stats:
                all_stats["Throughput"] = throughput_stats

            column_to_analyze_jitter = "[Call Test] [iPerf] [Throughput] DL Jitter"
            jitter_stats = data_performance_statics.analyze_jitter(file_path, column_to_analyze_jitter, event_col, start_event, end_event)
            if jitter_stats:
                all_stats["Jitter"] = jitter_stats

            column_to_analyze_dl_error_ratio = "[Call Test] [iPerf] [Throughput] DL Error Ratio"
            error_ratio_stats = data_performance_statics.analyze_error_ratio(file_path, column_to_analyze_dl_error_ratio, event_col, start_event, end_event)
            if error_ratio_stats:
                all_stats["Error Ratio"] = error_ratio_stats

        elif analysis_direction_detected == "UL":
            column_to_analyze_throughput = "[LTE] [Data Throughput] [Uplink (All)] [PUSCH] PUSCH TP (Total)"
            throughput_stats = data_performance_statics.analyze_throughput(file_path, column_to_analyze_throughput, event_col, start_event, end_event)
            if throughput_stats:
                all_stats["Throughput"] = throughput_stats

            column_to_analyze_ul_jitter = "[Call Test] [iPerf] [Call Average] [Jitter and Error] UL Jitter"
            jitter_stats = data_performance_statics.analyze_jitter(file_path, column_to_analyze_ul_jitter, event_col, start_event, end_event)
            if jitter_stats:
                all_stats["Jitter"] = jitter_stats

            column_to_analyze_ul_error_ratio = "[Call Test] [iPerf] [Call Average] [Jitter and Error] UL Error Ratio"
            error_ratio_stats = data_performance_statics.analyze_error_ratio(file_path, column_to_analyze_ul_error_ratio, event_col, start_event, end_event)
            if error_ratio_stats:
                all_stats["Error Ratio"] = error_ratio_stats
    
    return all_stats

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


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    analysis_script_path = os.path.join(script_dir, "data_performance_statics.py")
    
    base_data_dir = os.path.join("RawData", "TC91-1")
    
    subdirectories = [
        "UDP Download Task at 400 Mbps for 10 seconds",
        "UDP Download Task at 200 Mbps for 10 seconds",
        "Multi Stream HTTP Download for 30 seconds_Good",
        "Single Stream HTTP Download for 60 seconds_Good"
    ]

    if not os.path.exists(analysis_script_path):
        print(f"Error: Analysis script not found at {analysis_script_path}")
        sys.exit(1)
    if not os.path.isdir(base_data_dir):
        print(f"Error: Base data directory not found at {base_data_dir}")
        sys.exit(1)

    all_collected_results = {}

    for subdir in subdirectories:
        full_subdir_path = os.path.join(base_data_dir, subdir)
        if os.path.isdir(full_subdir_path):
            print(f"\n{'='*100}\nProcessing data in: {full_subdir_path}\n{'='*100}")
            
            subdir_results = {}
            for file in os.listdir(full_subdir_path):
                if file.lower().endswith(".csv"):
                    csv_file_path = os.path.join(full_subdir_path, file)
                    print(f"--- Analyzing file: {csv_file_path} ---")
                    stats = run_analysis_on_file(csv_file_path, analysis_script_path)
                    if stats:
                        device_type = stats.get("Device Type")
                        if device_type:
                            subdir_results[device_type] = stats
            all_collected_results[subdir] = subdir_results
        else:
            print(f"Warning: Subdirectory not found: {full_subdir_path}")
    
    if all_collected_results:
        create_pdf_report(all_collected_results)
    else:
        print("No data collected to generate a report.")
