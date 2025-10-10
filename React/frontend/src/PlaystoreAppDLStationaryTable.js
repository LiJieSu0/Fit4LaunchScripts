import React, { useEffect, useRef, useState } from 'react';
import Chart from 'chart.js/auto';
import ChartDataLabels from 'chartjs-plugin-datalabels';

Chart.register(ChartDataLabels);

const PlaystoreAppDLStationaryTable = ({ data }) => {
  const playstoreData = data["Data Performance"]["5G AUTO DP"]["5G Auto Data Play-store app DL Stationary"];

  if (!playstoreData) {
    return null;
  }

  const locations = ["location1", "location2", "location3"];
  const fileSizes = ["30M", "60M", "100M"];

  const extractThroughput = (location, deviceType, fileSize) => {
    const deviceData = playstoreData[location]?.[deviceType];
    if (deviceData && deviceData[fileSize]) {
      const testCaseKey = Object.keys(deviceData[fileSize])[0];
      return deviceData[fileSize][testCaseKey]?.overall_average_throughput;
    }
    return null;
  };

  const getPerformanceClass = (dutTput, refTput) => {
    if (dutTput === null || refTput === null || isNaN(dutTput) || isNaN(refTput) || refTput === 0) {
      return 'performance-unknown';
    }

    if (dutTput > 1.1 * refTput) {
      return 'performance-excellent';
    } else if (dutTput >= 0.9 * refTput && dutTput <= 1.1 * refTput) {
      return 'performance-pass';
    } else if (dutTput >= 0.8 * refTput && dutTput < 0.9 * refTput) {
      return 'performance-marginal-fail';
    } else { // dutTput < 0.8 * refTput
      return 'performance-fail';
    }
  };


  const renderTable = (fileSize) => {
    return (
      <div className="overflow-x-auto mb-6 table-container">
        <h4 className="text-lg font-semibold mb-2 text-gray-700">File Size: {fileSize}</h4>
        <table className="min-w-full border border-table-grid">
          <thead>
            <tr className="bg-table-header-bg text-table-header-text font-bold">
              <th className="py-2 px-4 border border-table-grid">Location</th>
              <th className="py-2 px-4 border border-table-grid">DUT Average Throughput (Mbps)</th>
              <th className="py-2 px-4 border border-table-grid">REF Average Throughput (Mbps)</th>
            </tr>
          </thead>
          <tbody>
            {locations.map((location, index) => {
              let displayLocation = "";
              if (location === "location1") {
                displayLocation = "Good";
              } else if (location === "location2") {
                displayLocation = "Moderate";
              } else if (location === "location3") {
                displayLocation = "Poor";
              }
              return (
                <tr key={location} className="bg-table-body-bg">
                  <td className="py-2 px-4 border border-table-grid text-center">
                    {displayLocation}
                  </td>
                  <td className={`py-2 px-4 border border-table-grid text-center ${getPerformanceClass(extractThroughput(location, "DUT", fileSize), extractThroughput(location, "REF", fileSize))}`}>
                    {extractThroughput(location, "DUT", fileSize)?.toFixed(2) || 'N/A'}
                  </td>
                  <td className={`py-2 px-4 border border-table-grid text-center ${getPerformanceClass(extractThroughput(location, "DUT", fileSize), extractThroughput(location, "REF", fileSize))}`}>
                    {extractThroughput(location, "REF", fileSize)?.toFixed(2) || 'N/A'}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    );
  };

  const ThroughputBarChart = ({ fileSize, chartData }) => {
    const chartRef = useRef(null);
    const chartInstance = useRef(null);

    useEffect(() => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }

      const ctx = chartRef.current.getContext('2d');

      const labels = ["Good", "Moderate", "Poor"];
      const dutData = labels.map(label => {
        const locationKey = label === "Good" ? "location1" : label === "Moderate" ? "location2" : "location3";
        return extractThroughput(locationKey, "DUT", fileSize);
      });
      const refData = labels.map(label => {
        const locationKey = label === "Good" ? "location1" : label === "Moderate" ? "location2" : "location3";
        return extractThroughput(locationKey, "REF", fileSize);
      });

      chartInstance.current = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'DUT',
              data: dutData,
              backgroundColor: 'rgba(255, 99, 132, 0.5)', // Red for DUT
              borderColor: 'rgb(255, 99, 132)',
              borderWidth: 1,
            },
            {
              label: 'REF',
              data: refData,
              backgroundColor: 'rgba(54, 162, 235, 0.5)', // Blue for REF
              borderColor: 'rgb(54, 162, 235)',
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: {
              display: true,
              text: `Average Throughput for ${fileSize} File Size`,
            },
            datalabels: {
              anchor: 'end',
              align: 'top',
              formatter: (value) => value !== null ? value.toFixed(2) : 'N/A',
              color: '#000',
            },
          },
          scales: {
            x: {
              title: {
                display: true,
                text: 'Performance Category',
              },
            },
            y: {
              title: {
                display: true,
                text: 'Speed (Mbps)',
              },
              beginAtZero: true,
            },
          },
        },
      });

      return () => {
        if (chartInstance.current) {
          chartInstance.current.destroy();
        }
      };
    }, [fileSize, chartData]);

    return (
      <div style={{ width: '80%', height: '400px', marginBottom: '20px' }}>
        <canvas ref={chartRef}></canvas>
      </div>
    );
  };

  return (
    <div className="category-section">
      <h3 className="text-xl font-bold mb-4 text-gray-800">5G Auto Data Play-store app DL Stationary</h3>
      {fileSizes.map(fileSize => renderTable(fileSize))}

      {fileSizes.map(fileSize => (
        <ThroughputBarChart key={fileSize} fileSize={fileSize} chartData={data} />
      ))}
    </div>
  );
};

export default PlaystoreAppDLStationaryTable;
