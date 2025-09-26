import React from 'react';
import './MrabStatisticsTable.css';

const MrabStatisticsTable = ({ mrabData }) => {
  if (!mrabData || Object.keys(mrabData).length === 0) {
    return <p className="text-gray-600">No MRAB data available.</p>;
  }

  const getPerformanceColor = (dutValue, refValue, metricType) => {
    // Special handling for Error Ratio when both DUT and REF values are 0
    if (metricType === "error_ratio" && dutValue === 0 && refValue === 0) {
      return "bg-performance-pass"; // Always purple for 0% error
    }

    if (refValue === 0) return "bg-gray-300"; // Cannot evaluate for other metrics

    let performanceResult = "Unknown";
    if (metricType === "throughput" || metricType === "mrab_performance") { // Higher is better for throughput and MRAB
      if (dutValue > 1.1 * refValue) performanceResult = "Excellent";
      else if (dutValue >= 0.9 * refValue && dutValue <= 1.1 * refValue) performanceResult = "Pass";
      else if (dutValue >= 0.8 * refValue && dutValue < 0.9 * refValue) performanceResult = "Marginal Fail";
      else if (dutValue < 0.8 * refValue) performanceResult = "Fail";
    } else if (metricType === "jitter" || metricType === "ping_rtt" || metricType === "web_page_load_time") { // Lower is better
      if (dutValue < 0.9 * refValue) performanceResult = "Excellent";
      else if (dutValue >= 0.9 * refValue && dutValue <= 1.1 * refValue) performanceResult = "Pass";
      else if (dutValue > 1.1 * refValue && dutValue <= 1.20 * refValue) performanceResult = "Marginal Fail";
      else if (dutValue > 1.20 * refValue) performanceResult = "Fail";
    } else if (metricType === "error_ratio") { // Lower is better
      if (dutValue < refValue) performanceResult = "Excellent";
      else if (dutValue <= 5.0 || (dutValue - refValue) <= 10.0) performanceResult = "Pass";
      else if (10.0 < (dutValue - refValue) && (dutValue - refValue) <= 20.0) performanceResult = "Marginal Fail";
      else if ((dutValue - refValue) > 20.0) performanceResult = "Fail";
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

  const categories = ["Pre Call", "In Call", "Post Call"];
  const statistics = ["Mean", "Maximum", "Minimum", "Standard Deviation"];

  const dutMrab = mrabData["DUT MRAB"]?.["MRAB Statistics"] || {};
  const refMrab = mrabData["REF MRAB"]?.["MRAB Statistics"] || {};

  return (
    <div className="overflow-x-auto mb-6 table-container">
      <h3 className="text-xl font-bold mb-4 text-gray-800">MRAB Statistics</h3>
      <table className="min-w-full border border-table-grid">
        <thead>
          <tr className="bg-table-header-bg text-table-header-text font-bold">
            <th className="py-2 px-4 border border-table-grid">Category</th>
            <th className="py-2 px-4 border border-table-grid">Statistic</th>
            <th className="py-2 px-4 border border-table-grid">DUT Value (Mbps)</th>
            <th className="py-2 px-4 border border-table-grid">REF Value (Mbps)</th>
          </tr>
        </thead>
        <tbody>
          {categories.map((category, categoryIndex) => (
            <React.Fragment key={category}>
              {statistics.map((stat, statIndex) => {
                const dutValue = dutMrab[category]?.[stat];
                const refValue = refMrab[category]?.[stat];

                let rowCategory = "";
                if (statIndex === 0) {
                  rowCategory = category;
                }

                let bgColor = "";
                if (stat === "Mean") {
                  bgColor = getPerformanceColor(dutValue, refValue, "mrab_performance");
                } else {
                  bgColor = "bg-table-body-bg"; // Default background for other stats
                }

                // Check if both DUT and REF values are null/undefined/NaN
                const isDutNA = typeof dutValue !== 'number';
                const isRefNA = typeof refValue !== 'number';

                if (isDutNA && isRefNA) {
                  return null; // Do not render this row if both are N/A
                }

                return (
                  <tr key={`${category}-${stat}`} className="bg-table-body-bg">
                    <td className="py-2 px-4 border border-table-grid text-center">{rowCategory}</td>
                    <td className="py-2 px-4 border border-table-grid text-center">{stat}</td>
                    <td className={`py-2 px-4 border border-table-grid text-center ${bgColor}`}>
                      {typeof dutValue === 'number' ? `${dutValue.toFixed(2)} Mbps` : 'N/A'}
                    </td>
                    <td className={`py-2 px-4 border border-table-grid text-center ${bgColor}`}>
                      {typeof refValue === 'number' ? `${refValue.toFixed(2)} Mbps` : 'N/A'}
                    </td>
                  </tr>
                );
              })}
            </React.Fragment>
          ))}
          {mrabData.overallMrabStatus && (
            <tr className="bg-table-body-bg font-bold">
              <td className="py-2 px-4 border border-table-grid text-center" colSpan="2">Overall MRAB Case Status (In Call Mean)</td>
              <td className={`py-2 px-4 border border-table-grid text-center ${getPerformanceColor(
                mrabData["DUT MRAB"]?.["MRAB Statistics"]?.["In Call"]?.["Mean"],
                mrabData["REF MRAB"]?.["MRAB Statistics"]?.["In Call"]?.["Mean"],
                "mrab_performance"
              )}`} colSpan="2">
                {mrabData.overallMrabStatus}
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default MrabStatisticsTable;
