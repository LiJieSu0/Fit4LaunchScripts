import React, { useEffect, useRef, useState } from 'react';
import Chart from 'chart.js/auto';
import ChartDataLabels from 'chartjs-plugin-datalabels';
import data from './data_analysis_results.json';
import './PingBarChart.css';

Chart.register(ChartDataLabels);

const PingBarChart = () => {
  const chartRefs = useRef({});
  const chartInstances = useRef({});
  const [pingChartData, setPingChartData] = useState([]);

  useEffect(() => {
    processPingChartData(data);
    return () => {
      Object.values(chartInstances.current).forEach(chart => chart.destroy());
    };
  }, []);

  useEffect(() => {
    pingChartData.forEach((chartDataItem, index) => {
      const chartId = `pingChart-${index}`;
      const ctx = chartRefs.current[chartId]?.getContext('2d');

      if (ctx) {
        if (chartInstances.current[chartId]) {
          chartInstances.current[chartId].destroy();
        }

        const labels = ['DUT', 'REF'];
        const dutValue = chartDataItem.dutAvg;
        const refValue = chartDataItem.refAvg;

        const maxDataValue = Math.max(dutValue, refValue);
        const minGridLines = 4;
        const pingStepSizes = [100, 50, 25, 5, 1];

        let tickStep;
        let yAxisMax;

        if (maxDataValue === 0) {
          yAxisMax = minGridLines * pingStepSizes[pingStepSizes.length - 1];
          tickStep = pingStepSizes[pingStepSizes.length - 1];
        } else {
          for (let step of pingStepSizes) {
            const numIntervalsIfMaxIsYMax = maxDataValue / step;
            if (numIntervalsIfMaxIsYMax >= 1) {
              if (minGridLines * step >= maxDataValue) {
                tickStep = step;
                break;
              }
            }
          }
          yAxisMax = Math.ceil(maxDataValue / tickStep) * tickStep;
          if (yAxisMax / tickStep < minGridLines) {
            yAxisMax = minGridLines * tickStep;
          }
        }

        const chartLabel = 'Mean Ping RTT (ms)';
        const yAxisTitle = 'Time (ms)';
        const unit = 'ms';

        const chartData = {
          labels: labels,
          datasets: [
            {
              label: chartLabel,
              data: [dutValue, refValue],
              backgroundColor: [
                'rgba(75, 192, 192, 0.6)', // Color for DUT
                'rgba(255, 159, 64, 0.6)', // Color for REF
              ],
              borderColor: [
                'rgba(75, 192, 192, 1)',
                'rgba(255, 159, 64, 1)',
              ],
              borderWidth: 1,
              barThickness: 30,
            },
          ],
        };

        const config = {
          type: 'bar',
          data: chartData,
          options: {
            responsive: true,
            maintainAspectRatio: false,
            aspectRatio: 1.5,
            layout: {
              padding: {
                left: 10,
                right: 10,
                top: 20,
                bottom: 10
              }
            },
            plugins: {
              title: {
                display: true,
                text: chartDataItem.testName, // Display test name as chart title
                font: {
                  size: 14,
                  weight: 'bold'
                }
              },
              legend: {
                display: true
              },
              datalabels: {
                anchor: 'end',
                align: 'top',
                color: 'black',
                font: {
                  weight: 'bold',
                  size: 12
                },
                formatter: (value) => (value > 0 ? `${value.toFixed(2)} ${unit}` : ''),
                display: true,
                clamp: true
              }
            },
            scales: {
              y: {
                beginAtZero: true,
                max: yAxisMax,
                ticks: {
                  stepSize: tickStep,
                  callback: function(value) {
                    return value;
                  }
                },
                title: {
                  display: true,
                  text: yAxisTitle
                }
              },
              x: {
                title: {
                  display: false
                }
              }
            }
          },
        };

        chartInstances.current[chartId] = new Chart(ctx, config);
      }
    });
  }, [pingChartData]);

  const processPingChartData = (jsonData) => {
    const processedCharts = [];

    Object.keys(jsonData).forEach(category => {
      Object.keys(jsonData[category]).forEach(testName => {
        const testData = jsonData[category][testName];
        let dutAvg = 0;
        let refAvg = 0;
        let hasPingData = false;

        const dutRefEntries = Object.keys(testData).filter(key => key.includes('DUT') || key.includes('REF'));

        dutRefEntries.forEach(dutRefKey => {
          const deviceData = testData[dutRefKey];
          if (deviceData["Ping RTT"]) {
            hasPingData = true;
            if (deviceData["Device Type"] === "DUT") {
              dutAvg = deviceData["Ping RTT"].avg || 0;
            } else if (deviceData["Device Type"] === "REF") {
              refAvg = deviceData["Ping RTT"].avg || 0;
            }
          }
        });

        if (hasPingData) {
          processedCharts.push({
            testName: testName,
            dutAvg: dutAvg,
            refAvg: refAvg,
          });
        }
      });
    });
    setPingChartData(processedCharts);
  };

  return (
    <div className="ping-bar-charts-container">
      <h2>Ping RTT Bar Charts</h2>
      <div className="charts-grid">
        {pingChartData.map((chartDataItem, index) => (
          <div key={index} className="chart-item">
            <canvas id={`pingChart-${index}`} ref={el => chartRefs.current[`pingChart-${index}`] = el}></canvas>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PingBarChart;
