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
      <table className="common-table">
        <thead>
          <tr>
            <th>Category</th>
            <th>Statistic</th>
            <th>DUT Value (Mbps)</th>
            <th>REF Value (Mbps)</th>
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
                  // Use a default background from common styles or keep it transparent
                  bgColor = ""; 
                }

                // Check if both DUT and REF values are null/undefined/NaN
                const isDutNA = typeof dutValue !== 'number';
                const isRefNA = typeof refValue !== 'number';

                if (isDutNA && isRefNA) {
                  return null; // Do not render this row if both are N/A
                }

                return (
                  <tr key={`${category}-${stat}`}>
                    <td>{rowCategory}</td>
                    <td>{stat}</td>
                    <td className={`${bgColor}`}>
                      {typeof dutValue === 'number' ? `${dutValue.toFixed(2)} Mbps` : 'N/A'}
                    </td>
                    <td className={`${bgColor}`}>
                      {typeof refValue === 'number' ? `${refValue.toFixed(2)} Mbps` : 'N/A'}
                    </td>
                  </tr>
                );
              })}
            </React.Fragment>
          ))}
          {mrabData.overallMrabStatus && (
            <tr className="font-bold">
              <td colSpan="2">Overall MRAB Case Status (In Call Mean)</td>
              <td className={`${getPerformanceColor(
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
