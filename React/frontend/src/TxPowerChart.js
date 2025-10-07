import React, { useEffect, useRef, useState } from 'react';
import Chart from 'chart.js/auto';
import ChartDataLabels from 'chartjs-plugin-datalabels';
import { fetchAndParseTxPowerData } from './utils/csvReader'; // Import the new Tx Power data fetcher

Chart.register(ChartDataLabels);

const TxPowerChart = ({ runNumber }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);
  const [chartData, setChartData] = useState({ pc2: [], pc3: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const getChartData = async () => {
      try {
        setLoading(true);
        const data = await fetchAndParseTxPowerData(runNumber); // Use Tx Power data fetcher
        setChartData(data);
        setError(null);
      } catch (err) {
        setError("Failed to load Tx Power data.");
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
              pointRadius: 0, // No point markers for Tx Power
            },
            {
              label: 'PC3',
              data: chartData.pc3,
              borderColor: 'rgb(54, 162, 235)', // Blue for PC3
              backgroundColor: 'rgba(54, 162, 235, 0.5)',
              tension: 0.1,
              pointRadius: 0, // No point markers for Tx Power
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          layout: {
            padding: {
              left: 0,
              right: 50, // Adjust this value to move the plot further left or right
            },
          },
          plugins: {
            title: {
              display: true,
              text: `Run ${runNumber} Tx Power Analysis (PC2 vs PC3)`, // Updated title
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
                text: 'Tx Power Value (dBm)', // Updated Y-axis label
              },
              beginAtZero: false,
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
    <div style={{ width: '80%', height: '400px', marginBottom: '20px' }}>
      <canvas ref={chartRef}></canvas>
    </div>
  );
};

export default TxPowerChart;
