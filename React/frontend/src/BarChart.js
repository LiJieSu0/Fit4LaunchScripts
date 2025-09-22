import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';
import ChartDataLabels from 'chartjs-plugin-datalabels'; // 確保導入插件

// 註冊插件
Chart.register(ChartDataLabels);

const BarChart = ({ testCaseData, testCaseName, isPing }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (chartInstance.current) {
      chartInstance.current.destroy();
    }

    const ctx = chartRef.current.getContext('2d');

    const labels = ['DUT', 'REF'];
    const isWebKepler = testCaseName.includes("Web-Kepler");
    console.log("BarChart - testCaseName:", testCaseName, "isWebKepler:", isWebKepler);

    let dutValue, refValue;
    if (isWebKepler) {
      dutValue = testCaseData?.DUT?.["Web Page Load Time"]?.Mean || 0;
      refValue = testCaseData?.REF?.["Web Page Load Time"]?.Mean || 0;
    } else {
      dutValue = isPing ? testCaseData?.DUT?.["Ping RTT"]?.avg || 0 : testCaseData?.DUT?.Throughput?.Mean || 0;
      refValue = isPing ? testCaseData?.REF?.["Ping RTT"]?.avg || 0 : testCaseData?.REF?.Throughput?.Mean || 0;
    }

    const maxDataValue = Math.max(dutValue, refValue);
    const minGridLines = 4; // 最少顯示4格
    const throughputStepSizes = [250, 100, 50, 25, 10, 5, 1];
    const pingStepSizes = [100, 50, 25, 5, 1];
    const webKeplerStepSizes = [0.5, 0.2, 0.1, 0.05]; // New step sizes for Web-Kepler
    
    const currentStepSizes = isWebKepler 
      ? webKeplerStepSizes 
      : (isPing ? pingStepSizes : throughputStepSizes);
    
    let tickStep;
    let yAxisMax;

    if (isWebKepler) {
      tickStep = 0.5;
      yAxisMax = Math.ceil(maxDataValue / tickStep) * tickStep;
      if (yAxisMax < minGridLines * tickStep) {
        yAxisMax = minGridLines * tickStep;
      }
    } else {
      if (maxDataValue === 0) {
        yAxisMax = minGridLines * currentStepSizes[currentStepSizes.length - 1];
        tickStep = currentStepSizes[currentStepSizes.length - 1];
      } else {
        // Find the largest step that results in a reasonable number of intervals
        for (let step of currentStepSizes) {
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
    }

    const chartLabel = isWebKepler ? 'Web Page Load Time (s)' : (isPing ? 'Mean Ping RTT (ms)' : 'Mean Throughput (Mbps)');
    const yAxisTitle = isWebKepler ? 'Time (s)' : (isPing ? 'Time (ms)' : 'Throughput (Mbps)');
    const unit = isWebKepler ? 's' : (isPing ? 'ms' : 'Mbps');

    const data = {
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
          barThickness: 30, // Reduced thickness for narrower bars
        },
      ],
    };

    const config = {
      type: 'bar',
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        aspectRatio: 1.5, // Adjusted to make chart narrower
        layout: {
          padding: {
            left: 10,
            right: 10,
            top: 20, // 增加頂部 padding 確保數值有空間
            bottom: 10
          }
        },
        plugins: {
          title: {
            display: false // 保持移除標題
          },
          legend: {
            display: true // 保持圖例顯示
          },
          datalabels: {
            anchor: 'end', // 數值顯示在柱子頂部
            align: 'top', // 數值在上方
            color: 'black', // 數值顏色
            font: {
              weight: 'bold', // 數值字體加粗
              size: 12 // 設置字體大小
            },
            formatter: (value) => (value > 0 ? `${value.toFixed(2)} ${unit}` : ''), // 僅在數值大於0時顯示，並添加單位
            display: true, // 確保顯示數據標籤
            clamp: true // 防止標籤超出圖表範圍
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            max: yAxisMax, // 動態設置最大值
            ticks: {
              stepSize: tickStep, // 動態設置每格單位
              callback: function(value) {
                return value; // 確保顯示整數
              }
            },
            title: {
              display: true,
              text: yAxisTitle
            }
          },
          x: {
            title: {
              display: false // Removed 'Device' label
            }
          }
        }
      },
    };

    chartInstance.current = new Chart(ctx, config);

    // 診斷：檢查是否成功創建圖表
    if (!chartInstance.current) {
      console.error('Chart instance failed to create');
    }

    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
    };
  }, [testCaseData, testCaseName, isPing]);

  return (
    <div className="BarChart-container" style={{ maxWidth: '400px' }}> {/* Removed margin: 'auto' */}
      <canvas ref={chartRef}></canvas>
    </div>
  );
};

export default BarChart;
