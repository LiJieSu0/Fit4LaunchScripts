import React from 'react';
import allResults from './data_analysis_results.json';
import BarChart from './BarChart';

// Helper function to recursively extract test cases
const extractTestCases = (data, currentPath = []) => {
  let extracted = [];

  // If the current 'data' object contains DUT/REF keys, it's a test case
  const hasDutRefKeys = Object.keys(data).some(key => key.toLowerCase().includes("dut") || key.toLowerCase().includes("ref"));

  if (hasDutRefKeys) {
    let dutObject = {};
    let refObject = {};
    let isPingTest = false;

    for (const key in data) {
      if (key.toLowerCase().includes("dut")) {
        dutObject = data[key];
      } else if (key.toLowerCase().includes("ref")) {
        refObject = data[key];
      }
      if (key.toLowerCase().includes("ping")) {
        isPingTest = true;
      }
    }
    if (Object.keys(dutObject).length > 0 || Object.keys(refObject).length > 0) {
      extracted.push({
        name: currentPath.join(" - "),
        data: { DUT: dutObject, REF: refObject },
        isPing: isPingTest
      });
    }
  }

  // Always recurse into children, regardless of whether the current 'data' was a test case itself
  for (const key in data) {
    if (typeof data[key] === 'object' && data[key] !== null) {
      extracted = extracted.concat(extractTestCases(data[key], [...currentPath, key]));
    }
  }

  return extracted;
};

const DataPerformanceReport = () => {
  const renderStatisticsTable = (title, data, isPing = false) => {
    if (!data || Object.keys(data).length === 0) {
      return <p className="text-gray-600">No comparable data found for this subdirectory.</p>;
    }

    const dutData = data.DUT || {};
    const refData = data.REF || {};

    const metricsToDisplay = isPing 
      ? ["Ping RTT"] 
      : ["Throughput", "Jitter", "Error Ratio", "Web Page Load Time"]; // Added Web Page Load Time
    const statOrderMap = {
      "Throughput": ["Mean", "Standard Deviation", "Minimum", "Maximum"],
      "Jitter": ["Mean"],
      "Error Ratio": ["Mean"],
      "Ping RTT": ["Mean", "Standard Deviation", "Minimum", "Maximum"],
      "Web Page Load Time": ["Mean", "Standard Deviation", "Minimum", "Maximum"], // Added Web Page Load Time stats
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
      } else if (metricType === "jitter" || metricType === "ping_rtt" || metricType === "web_page_load_time") { // Lower is better
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
      <div className="overflow-x-auto mb-6 table-container">
        <table className="min-w-full border border-table-grid">
          <thead>
            <tr className="bg-table-header-bg text-table-header-text font-bold">
              <th className="py-2 px-4 border border-table-grid">Metric</th>
              <th className="py-2 px-4 border border-table-grid">Statistic</th>
              <th className="py-2 px-4 border border-table-grid">DUT Value {isPing ? "(ms)" : (title.includes("Web-Kepler") ? "(s)" : "(Mbps)")}</th>
              <th className="py-2 px-4 border border-table-grid">REF Value {isPing ? "(ms)" : (title.includes("Web-Kepler") ? "(s)" : "(Mbps)")}</th>
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
                    let metricType = "";
                    if (metric === "Throughput") {
                      metricType = "throughput";
                    } else if (metric === "Jitter") {
                      metricType = "jitter";
                    } else if (metric === "Ping RTT") {
                      metricType = "ping_rtt";
                    } else if (metric === "Web Page Load Time") {
                      metricType = "web_page_load_time"; // New metric type
                    }
                    bgColor = getPerformanceColor(dutValue, refValue, metricType);
                  }

                  const unit = (metric === "Jitter" || metric === "Ping RTT") ? "ms" : (metric === "Error Ratio" ? "%" : (metric === "Web Page Load Time" ? "s" : "")); // Added unit for Web Page Load Time

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

  const allFlattenedTestCases = extractTestCases(allResults);

  // Group test cases by their top-level category for rendering headers
  const groupedByCategories = allFlattenedTestCases.reduce((acc, testCase) => {
    const category = testCase.name.split(' - ')[0];
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(testCase);
    return acc;
  }, {});

  return (
    <>
      {Object.entries(groupedByCategories).map(([categoryName, testCases]) => (
        <div key={categoryName} className="category-section">
          <h2 className="text-2xl font-bold mb-6 text-blue-700">{categoryName}</h2>
          {testCases.map(testCase => (
            <div key={testCase.name} className="report-section">
              <h3 className="text-xl font-bold mb-4 text-gray-800">{testCase.name}</h3>
              <div className="table-chart-container">
                {renderStatisticsTable(testCase.name, testCase.data, testCase.isPing)}
                {(Object.keys(testCase.data.DUT).length > 0 || Object.keys(testCase.data.REF).length > 0) && (
                  <BarChart testCaseData={testCase.data} testCaseName={testCase.name} isPing={testCase.isPing} />
                )}
              </div>
            </div>
          ))}
        </div>
      ))}
    </>
  );
};

export default DataPerformanceReport;
