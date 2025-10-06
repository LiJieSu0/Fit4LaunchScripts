import React, { useEffect, useRef, useState } from 'react';
import Chart from 'chart.js/auto';
import ChartDataLabels from 'chartjs-plugin-datalabels'; // Import the datalabels plugin
import { fetchAndParseRsrpData } from './utils/csvReader';

Chart.register(ChartDataLabels); // Register the plugin globally

const RsrpChart = ({ runNumber }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);
  const [chartData, setChartData] = useState({ pc2: [], pc3: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const getChartData = async () => {
      try {
        setLoading(true);
        const data = await fetchAndParseRsrpData(runNumber);
        setChartData(data);
        setError(null);
      } catch (err) {
        setError("Failed to load RSRP data.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    getChartData();
  }, [runNumber]);

  useEffect(() => {
    if (!loading && chartRef.current && chartData.pc2.length > 0 || chartData.pc3.length > 0) {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }

      const ctx = chartRef.current.getContext('2d');
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
              pointRadius: 0, // Hide points
            },
            {
              label: 'PC3',
              data: chartData.pc3,
              borderColor: 'rgb(54, 162, 235)', // Blue for PC3
              backgroundColor: 'rgba(54, 162, 235, 0.5)',
              tension: 0.1,
              pointRadius: 0, // Hide points
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
  }, [chartData, loading, runNumber]);

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
