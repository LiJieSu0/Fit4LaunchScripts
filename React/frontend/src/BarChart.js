import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';
import ChartDataLabels from 'chartjs-plugin-datalabels'; // 確保導入插件

// 註冊插件
Chart.register(ChartDataLabels);

const BarChart = ({ testCaseData, testCaseName }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (chartInstance.current) {
      chartInstance.current.destroy();
    }

    const ctx = chartRef.current.getContext('2d');

    const labels = ['DUT', 'REF'];
    const dutThroughput = testCaseData?.DUT?.Throughput?.Mean || 0;
    const refThroughput = testCaseData?.REF?.Throughput?.Mean || 0;

    const maxThroughput = Math.max(dutThroughput, refThroughput);
    const minGridLines = 4; // 最少顯示4格
    const stepSizes = [250, 100, 50, 25, 10, 5, 1];
    let tickStep = 1;
    let yAxisMax = 0;

    if (maxThroughput === 0) {
      yAxisMax = minGridLines * stepSizes[stepSizes.length - 1]; // 4 * 1 = 4
      tickStep = stepSizes[stepSizes.length - 1]; // 1
    } else {
      // Find the largest step that results in a reasonable number of intervals
      for (let step of stepSizes) {
        // Calculate how many intervals this step would create if yAxisMax is maxThroughput
        const numIntervalsIfMaxIsYMax = maxThroughput / step;

        // We want a step where numIntervalsIfMaxIsYMax is not too small (e.g., at least 1)
        // and also ensures that when we scale up to minGridLines, it's still a good step.
        if (numIntervalsIfMaxIsYMax >= 1) { // If maxThroughput is at least one step
            // Check if this step, when scaled to minGridLines, would cover maxThroughput
            if (minGridLines * step >= maxThroughput) {
                tickStep = step;
                break; // Found the largest suitable step
            }
        }
      }

      // Calculate yAxisMax as the smallest multiple of tickStep that is >= maxThroughput
      yAxisMax = Math.ceil(maxThroughput / tickStep) * tickStep;

      // Ensure yAxisMax is large enough to show at least minGridLines
      if (yAxisMax / tickStep < minGridLines) {
        yAxisMax = minGridLines * tickStep;
      }
    }

    const data = {
      labels: labels,
      datasets: [
        {
          label: 'Mean Throughput (Mbps)',
          data: [dutThroughput, refThroughput],
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
            formatter: (value) => (value > 0 ? value.toFixed(2) : ''), // 僅在數值大於0時顯示
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
              text: 'Throughput (Mbps)'
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
  }, [testCaseData, testCaseName]);

  return (
    <div className="BarChart-container" style={{ maxWidth: '400px' }}> {/* Removed margin: 'auto' */}
      <canvas ref={chartRef}></canvas>
    </div>
  );
};

export default BarChart;
