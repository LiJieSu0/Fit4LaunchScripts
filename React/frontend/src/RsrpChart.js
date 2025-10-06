import React, { useEffect, useRef, useState } from 'react';
import Chart from 'chart.js/auto';
import ChartDataLabels from 'chartjs-plugin-datalabels'; // Import the datalabels plugin
import { fetchAndParseRsrpData } from './utils/csvReader';
import dataAnalysisResults from './data_analysis_results.json'; // Import the JSON data

Chart.register(ChartDataLabels); // Register the plugin globally

const RsrpChart = ({ runNumber }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);
  const [chartData, setChartData] = useState({ pc2: [], pc3: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [rsrpMarkers, setRsrpMarkers] = useState({ pc2: [], pc3: [] });

  useEffect(() => {
    const getChartData = async () => {
      try {
        setLoading(true);
        const data = await fetchAndParseRsrpData(runNumber);
        setChartData(data);
        setError(null);

        // Extract RSRP values from JSON for marking
        const coverageTest = dataAnalysisResults["Coverage Performance"]["5G n41 HPUE Coverage Test"];
        const currentRunData = coverageTest[`Run${runNumber}`];

        if (currentRunData) {
          const pc2Markers = currentRunData
            .filter(item => item["Device type"] === "PC2" && item.rsrp_value !== undefined)
            .map(item => item.rsrp_value);
          const pc3Markers = currentRunData
            .filter(item => item["Device type"] === "PC3" && item.rsrp_value !== undefined)
            .map(item => item.rsrp_value);
          setRsrpMarkers({ pc2: pc2Markers, pc3: pc3Markers });
        } else {
          setRsrpMarkers({ pc2: [], pc3: [] });
        }

      } catch (err) {
        setError("Failed to load RSRP data or analysis results.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    getChartData();
  }, [runNumber]);

  useEffect(() => {
    if (!loading && chartRef.current && (chartData.pc2.length > 0 || chartData.pc3.length > 0)) {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }

      const ctx = chartRef.current.getContext('2d');

      // Determine point style based on whether it's a marker
      const getPointStyle = (dataPointY, markers) => {
        return markers.includes(dataPointY) ? 'rect' : 'circle'; // Changed to rect for drop points
      };

      // Prepare point styling for PC2
      const pc2PointRadius = chartData.pc2.map(dataPoint =>
        rsrpMarkers.pc2.includes(dataPoint.y) ? 10 : 0 // Increased radius for drop points
      );
      const pc2PointStyle = chartData.pc2.map(dataPoint =>
        getPointStyle(dataPoint.y, rsrpMarkers.pc2)
      );
      const pc2PointBackgroundColor = chartData.pc2.map(dataPoint =>
        rsrpMarkers.pc2.includes(dataPoint.y) ? 'rgb(255, 99, 132)' : 'rgba(255, 99, 132, 0.5)'
      );
      const pc2PointBorderColor = chartData.pc2.map(dataPoint =>
        rsrpMarkers.pc2.includes(dataPoint.y) ? 'rgb(255, 99, 132)' : 'rgb(255, 99, 132)'
      );

      // Prepare point styling for PC3
      const pc3PointRadius = chartData.pc3.map(dataPoint =>
        rsrpMarkers.pc3.includes(dataPoint.y) ? 10 : 0 // Increased radius for drop points
      );
      const pc3PointStyle = chartData.pc3.map(dataPoint =>
        getPointStyle(dataPoint.y, rsrpMarkers.pc3)
      );
      const pc3PointBackgroundColor = chartData.pc3.map(dataPoint =>
        rsrpMarkers.pc3.includes(dataPoint.y) ? 'rgb(54, 162, 235)' : 'rgba(54, 162, 235, 0.5)'
      );
      const pc3PointBorderColor = chartData.pc3.map(dataPoint =>
        rsrpMarkers.pc3.includes(dataPoint.y) ? 'rgb(54, 162, 235)' : 'rgb(54, 162, 235)'
      );

      chartInstance.current = new Chart(ctx, {
        type: 'line',
        data: {
          labels: chartData.pc2.map(dataPoint => dataPoint.x), // X-axis labels from PC2 data points
          datasets: [
            {
              label: 'PC2',
              data: chartData.pc2,
              borderColor: 'rgb(255, 99, 132)', // Red for PC2
              backgroundColor: 'rgba(255, 99, 132, 0.5)',
              tension: 0.1,
              pointRadius: pc2PointRadius, // Apply dynamic point radius
              pointBackgroundColor: pc2PointBackgroundColor, // Apply dynamic point background color
              pointBorderColor: pc2PointBorderColor, // Apply dynamic point border color
              pointStyle: pc2PointStyle, // Apply dynamic point style
            },
            {
              label: 'PC3',
              data: chartData.pc3,
              borderColor: 'rgb(54, 162, 235)', // Blue for PC3
              backgroundColor: 'rgba(54, 162, 235, 0.5)',
              tension: 0.1,
              pointRadius: pc3PointRadius, // Apply dynamic point radius
              pointBackgroundColor: pc3PointBackgroundColor, // Apply dynamic point background color
              pointBorderColor: pc3PointBorderColor, // Apply dynamic point border color
              pointStyle: pc3PointStyle, // Apply dynamic point style
            },
            {
              label: 'Drop point', // Label for the legend
              data: [], // No actual data, just for legend
              borderColor: 'black', // Color for the legend icon
              pointBackgroundColor: 'black',
              pointBorderColor: 'black',
              pointRadius: 10, // Increased radius for legend icon
              pointStyle: 'rect', // Changed to rect for drop points
              type: 'line', // Ensure it's treated as a line dataset for legend styling
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: {
              display: true,
              text: `Run ${runNumber} RSRP Analysis (PC2 vs PC3)`,
            },
            datalabels: {
              display: false, // Disable datalabels
            },
            legend: {
                display: true,
                labels: {
                    usePointStyle: true, // Use point style for legend items
                }
            }
          },
          scales: {
            x: {
              title: {
                display: true,
                text: 'Data Point Order',
              },
            },
            y: {
              title: {
                display: true,
                text: 'RSRP Value',
              },
              beginAtZero: false, // RSRP values can be negative
            },
          },
        },
      });
    }

    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
    };
  }, [chartData, loading, runNumber, rsrpMarkers]);

  if (loading) return <div>Loading chart for Run {runNumber}...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;
  if (chartData.pc2.length === 0 && chartData.pc3.length === 0) return <div>No data available for Run {runNumber}.</div>;

  return (
    <div style={{ width: '100%', height: '400px', marginBottom: '20px' }}>
      <canvas ref={chartRef}></canvas>
    </div>
  );
};

export default RsrpChart;
