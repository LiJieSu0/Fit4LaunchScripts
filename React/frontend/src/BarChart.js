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

    // 計算 Y 軸的最大值，略高於最大數據值
    const maxThroughput = Math.max(dutThroughput, refThroughput);
    let yAxisMax = Math.ceil(maxThroughput / 100) * 100 + 100; // 初始最大值作為緩衝

    // 定義可能的步長，從大到小
    const stepSizes = [200, 100, 50, 25, 10, 5, 1];
    let tickStep = 100; // 預設步長

    // 選擇最適合的步長，確保至少 4 格 (5 個刻度點)
    for (let step of stepSizes) {
      const tickCount = Math.ceil(yAxisMax / step) + 1; // 包括 0 在內的總刻度數
      if (tickCount >= 5) { // 至少 4 格 (5 個刻度點)
        tickStep = step;
        break;
      }
    }

    // 調整 yAxisMax 為步長的倍數，確保至少 4 格
    const minTicks = 4;
    const requiredRange = minTicks * tickStep;
    yAxisMax = Math.max(yAxisMax, requiredRange); // 確保範圍足夠支持 4 格
    yAxisMax = Math.ceil(yAxisMax / tickStep) * tickStep; // 調整為步長倍數

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
              display: true,
              text: 'Device'
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
    <div className="BarChart-container" style={{ maxWidth: '400px', margin: 'auto' }}>
      <canvas ref={chartRef}></canvas>
    </div>
  );
};

export default BarChart;