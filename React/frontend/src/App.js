import React from 'react';
import allResults from './data_analysis_results.json';

function App() {
  const renderStatisticsTable = (title, data, isPing = false) => {
    if (!data || Object.keys(data).length === 0) {
      return <p className="text-gray-600">No comparable data found for this subdirectory.</p>;
    }

    const dutData = data.DUT || {};
    const refData = data.REF || {};

    const metricsToDisplay = isPing ? ["Ping RTT"] : ["Throughput", "Jitter", "Error Ratio"];
    const statOrderMap = {
      "Throughput": ["Mean", "Standard Deviation", "Minimum", "Maximum"],
      "Jitter": ["Mean"],
      "Error Ratio": ["Mean"],
      "Ping RTT": ["Mean", "Standard Deviation", "Minimum", "Maximum"],
    };
    const pingStatMap = {
      "Mean": "avg",
      "Standard Deviation": "std_dev",
      "Minimum": "min",
      "Maximum": "max",
    };

    const getPerformanceColor = (dutValue, refValue, metricType) => {
      if (refValue === 0) return "bg-gray-300"; // Cannot evaluate
      
      let performanceResult = "Unknown";
      if (metricType === "throughput") {
        if (dutValue > 1.1 * refValue) performanceResult = "Excellent";
        else if (dutValue >= 0.9 * refValue && dutValue <= 1.1 * refValue) performanceResult = "Pass";
        else if (dutValue >= 0.8 * refValue && dutValue < 0.9 * refValue) performanceResult = "Marginal Fail";
        else if (dutValue < 0.8 * refValue) performanceResult = "Fail";
      } else if (metricType === "jitter" || metricType === "ping_rtt") { // Lower is better
        if (dutValue < 0.9 * refValue) performanceResult = "Excellent";
        else if (dutValue >= 0.9 * refValue && dutValue <= 1.1 * refValue) performanceResult = "Pass";
        else if (dutValue > 1.1 * refValue && dutValue <= 1.20 * refValue) performanceResult = "Marginal Fail";
        else if (dutValue > 1.20 * refValue) performanceResult = "Fail";
      }

      switch (performanceResult) {
        case "Excellent": return "bg-performance-excellent";
        case "Pass": return "bg-performance-pass";
        case "Marginal Fail": return "bg-performance-marginal-fail";
        case "Fail": return "bg-performance-fail";
        case "Cannot evaluate: Reference throughput is zero.": return "bg-performance-cannot-evaluate";
        default: return "bg-performance-unknown";
      }
    };

    return (
      <div className="overflow-x-auto mb-6">
        <table className="min-w-full border border-table-grid">
          <thead>
            <tr className="bg-table-header-bg text-table-header-text font-bold">
              <th className="py-2 px-4 border border-table-grid">Metric</th>
              <th className="py-2 px-4 border border-table-grid">Statistic</th>
              <th className="py-2 px-4 border border-table-grid">DUT Value</th>
              <th className="py-2 px-4 border border-table-grid">REF Value</th>
            </tr>
          </thead>
          <tbody>
            {metricsToDisplay.map((metric, metricIndex) => (
              <React.Fragment key={metric}>
                {(statOrderMap[metric] || []).map((stat, statIndex) => {
                  const dutValue = isPing 
                    ? (metric === "Ping RTT" ? dutData[metric]?.[pingStatMap[stat]] : null)
                    : dutData[metric]?.[stat];
                  const refValue = isPing 
                    ? (metric === "Ping RTT" ? refData[metric]?.[pingStatMap[stat]] : null)
                    : refData[metric]?.[stat];

                  let rowMetric = "";
                  if (statIndex === 0) { // Only show metric name for the first statistic of that metric
                    rowMetric = metric;
                  }

                  let bgColor = "";
                  if (stat === "Mean") { // Apply color only to Mean for all metrics
                    const metricType = metric === "Throughput" ? "throughput" : (metric === "Jitter" ? "jitter" : "ping_rtt");
                    bgColor = getPerformanceColor(dutValue, refValue, metricType);
                  }

                  const unit = (metric === "Jitter" || metric === "Ping RTT") ? "ms" : (metric === "Error Ratio" ? "%" : "");

                  // Check if both DUT and REF values are null/undefined/NaN
                  const isDutNA = typeof dutValue !== 'number';
                  const isRefNA = typeof refValue !== 'number';

                  if (isDutNA && isRefNA) {
                    return null; // Do not render this row if both are N/A
                  }

                  return (
                    <tr key={`${metric}-${stat}`} className="bg-table-body-bg">
                      <td className="py-2 px-4 border border-table-grid text-center">{rowMetric}</td>
                      <td className="py-2 px-4 border border-table-grid text-center">{stat}</td>
                      <td className={`py-2 px-4 border border-table-grid text-center ${bgColor}`}>
                        {typeof dutValue === 'number' ? `${dutValue.toFixed(2)} ${unit}`.trim() : 'N/A'}
                      </td>
                      <td className={`py-2 px-4 border border-table-grid text-center ${bgColor}`}>
                        {typeof refValue === 'number' ? `${refValue.toFixed(2)} ${unit}`.trim() : 'N/A'}
                      </td>
                    </tr>
                  );
                })}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  return (
    <div className="container mx-auto p-4 main-content"> {/* Add a class for easier targeting in CSS */}
      <h1 className="text-4xl font-bold text-center my-8">Data Performance Analysis Report</h1>
      <h2 className="text-2xl font-semibold text-center mb-10">Comparison of DUT and REF Devices</h2>

      {Object.entries(allResults).map(([subdirName, results]) => (
        <div key={subdirName} className="mb-12 p-6 bg-gray-50 rounded-lg shadow-md">
          <h3 className="text-xl font-bold mb-4 text-gray-800">{subdirName}</h3>
          {renderStatisticsTable(subdirName, results, subdirName.startsWith("Ping -"))}
        </div>
      ))}
    </div>
  );
}

export default App;
