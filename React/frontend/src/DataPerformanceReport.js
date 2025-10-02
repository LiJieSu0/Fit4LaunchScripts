import React from 'react';
import allResults from './data_analysis_results.json';
import BarChart from './BarChart';
import MrabStatisticsTable from './MrabStatisticsTable'; // Import MrabStatisticsTable
import CallPerformanceTable from './CallPerformanceTable'; // New import
import CallCategoriesChart from './CallCategoriesChart'; // New import
import VoiceQualityTable from './VoiceQualityTable'; // New import
import AudioDelayTable from './AudioDelayTable'; // New import
import PValueTable from './PValueTable'; // Import PValueTable

// Helper function to recursively extract test cases
const extractTestCases = (data, currentPath = []) => {
  let extracted = [];

  // Check if the current data object is an MRAB test case
  if (data["DUT MRAB"] && data["REF MRAB"] && data["DUT MRAB"]["Analysis Type"] === "mrab_performance") {
    extracted.push({
      name: currentPath.join(" - "),
      data: data, // Pass the entire MRAB data object
      isMrab: true,
      isCallPerformance: false,
      isVoiceQuality: false,
    });
    return extracted; // Stop further recursion for this branch as we've found the MRAB data
  }

  // Check if the current data object is a Call Performance test case
  if (data.DUT && data.REF && typeof data.initiation_p_value === 'number' && typeof data.retention_p_value === 'number') {
    extracted.push({
      name: currentPath.join(" - "),
      data: data, // Pass the entire Call Performance data object
      isMrab: false,
      isCallPerformance: true,
      isVoiceQuality: false,
    });
    return extracted; // Stop further recursion for this branch as we've found the Call Performance data
  }

  // Check if the current data object is a Voice Quality test case
  const isVoiceQualityTest = Object.keys(data).some(key => key.startsWith("DUT")) &&
                             Object.keys(data).some(key => key.startsWith("REF")) &&
                             Object.values(data).every(deviceData => 
                               typeof deviceData === 'object' && deviceData !== null &&
                               deviceData.ul_mos_stats && deviceData.dl_mos_stats
                             );

  if (isVoiceQualityTest) {
    extracted.push({
      name: currentPath.join(" - "),
      data: data,
      isMrab: false,
      isCallPerformance: false,
      isVoiceQuality: true,
      isAudioDelay: false,
    });
    return extracted; // Stop further recursion for this branch
  }

  // Check if the current data object is an Audio Delay test case
  const isAudioDelayTest = Object.keys(data).includes("DUT1") &&
                           Object.keys(data).includes("REF1") &&
                           Object.keys(data).includes("DUT2") &&
                           Object.keys(data).includes("REF2") &&
                           Object.values(data).every(deviceData =>
                               typeof deviceData === 'object' && deviceData !== null &&
                               deviceData.mean !== undefined &&
                               deviceData.std_dev !== undefined &&
                               deviceData.min !== undefined &&
                               deviceData.max !== undefined &&
                               deviceData.occurrences !== undefined
                           );

  if (isAudioDelayTest) {
    extracted.push({
      name: currentPath.join(" - "),
      data: data,
      isMrab: false,
      isCallPerformance: false,
      isVoiceQuality: false,
      isAudioDelay: true,
    });
    return extracted; // Stop further recursion for this branch
  }

  // If the current 'data' object contains DUT/REF keys, it's a regular data performance test case
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
      // Check for Ping RTT within DUT or REF objects
      if (dutObject["Ping RTT"] || refObject["Ping RTT"]) {
        isPingTest = true;
      }
    }
        if (Object.keys(dutObject).length > 0 || Object.keys(refObject).length > 0) {
          extracted.push({
            name: currentPath.join(" - "),
            data: { DUT: dutObject, REF: refObject },
            isPing: isPingTest,
      isMrab: false,
      isCallPerformance: false,
      isVoiceQuality: false,
      isAudioDelay: false,
    });
  }
  }

  // Always recurse into children for other types of data
  for (const key in data) {
    if (typeof data[key] === 'object' && data[key] !== null) {
      const result = extractTestCases(data[key], [...currentPath, key]);
      extracted = extracted.concat(result);
    }
  }

  return extracted;
};

const DataPerformanceReport = () => {
  const allFlattenedTestCases = extractTestCases(allResults);

  const renderStatisticsTable = (title, data, metricsToDisplay) => { // Added metricsToDisplay prop
    if (!data || Object.keys(data).length === 0) {
      return <p className="text-gray-600">No comparable data found for this subdirectory.</p>;
    }

    const dutData = data.DUT || {};
    const refData = data.REF || {};

    // metricsToDisplay is now passed as a prop
    // Removed internal definition of metricsToDisplay

    const statOrderMap = {
      "Throughput": ["Mean", "Standard Deviation", "Minimum", "Maximum"],
      "Jitter": ["Mean"],
      "Error Ratio": ["Mean"],
      "Ping RTT": ["Mean", "Standard Deviation", "Minimum", "Maximum"],
      "Web Page Load Time": ["Mean", "Standard Deviation", "Minimum", "Maximum"],
    };
    const pingStatMap = {
      "Mean": "avg",
      "Standard Deviation": "std_dev",
      "Minimum": "min",
      "Maximum": "max",
    };

    const getPerformanceColor = (dutValue, refValue, metricType) => {
      // Special handling for Error Ratio when both DUT and REF values are 0
      if (metricType === "error_ratio" && dutValue === 0 && refValue === 0) {
        return "bg-performance-pass"; // Always purple for 0% error
      }

      if (refValue === 0) return "bg-gray-300"; // Cannot evaluate for other metrics

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

    return (
      <div className="overflow-x-auto mb-6 table-container">
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
                  const isCurrentMetricPing = (metric === "Ping RTT");
                  const isCurrentMetricWebKepler = (metric === "Web Page Load Time");

                  const dutValue = isCurrentMetricPing 
                    ? dutData[metric]?.[pingStatMap[stat]]
                    : dutData[metric]?.[stat];
                  const refValue = isCurrentMetricPing 
                    ? refData[metric]?.[pingStatMap[stat]]
                    : refData[metric]?.[stat];

                  let rowMetric = "";
                  if (statIndex === 0) { // Only show metric name for the first statistic of that metric
                    rowMetric = metric;
                  }

                  let bgColor = "";
                  let metricType = "";
                  let unit = "";

                  if (metric === "Throughput") {
                    metricType = "throughput";
                    unit = "Mbps";
                  } else if (metric === "Jitter") {
                    metricType = "jitter";
                    unit = "ms";
                  } else if (metric === "Ping RTT") {
                    metricType = "ping_rtt";
                    unit = "ms";
                  } else if (metric === "Web Page Load Time") {
                    metricType = "web_page_load_time";
                    unit = "s";
                  } else if (metric === "Error Ratio") {
                    metricType = "error_ratio";
                    unit = "%";
                  }

                  if (stat === "Mean") { // Apply color only to Mean for all metrics
                    bgColor = getPerformanceColor(dutValue, refValue, metricType);
                  }

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
          {testCases.map(testCase => {
            if (testCase.isMrab) {
              // Render MrabStatisticsTable for MRAB test cases
              return (
                <div key={testCase.name} className="report-section">
                  <h3 className="text-xl font-bold mb-4 text-gray-800">{testCase.name}</h3>
                  <MrabStatisticsTable mrabData={testCase.data} />
                </div>
              );
            } else if (testCase.isCallPerformance) { // New condition for Call Performance
              console.log("Call Performance Test Case:", testCase.name, "Initiation P-Value:", testCase.data.initiation_p_value, "Retention P-Value:", testCase.data.retention_p_value);

              const dutTotalAttempts = testCase.data.DUT.total_attempts;
              const dutInitiationFailures = testCase.data.DUT.total_initiation_failures;
              const dutRetentionFailures = testCase.data.DUT.total_retention_failures;

              let dutFailurePercentage = 0;
              if (dutTotalAttempts > 0) {
                dutFailurePercentage = ((dutInitiationFailures + dutRetentionFailures) / dutTotalAttempts) * 100;
              }

              return (
                <div key={testCase.name} className="report-section">
                  <h3 className="text-xl font-bold mb-4 text-gray-800">{testCase.name}</h3>
                  <CallPerformanceTable callPerformanceData={testCase.data} />
                  {testCase.name.includes("CP MO") && (
                    <PValueTable
                      callType="MO"
                      initiationPValue={testCase.data.initiation_p_value}
                      retentionPValue={testCase.data.retention_p_value}
                      dutFailurePercentage={dutFailurePercentage}
                    />
                  )}
                  {testCase.name.includes("CP MT") && (
                    <PValueTable
                      callType="MT"
                      initiationPValue={testCase.data.initiation_p_value}
                      dutFailurePercentage={dutFailurePercentage}
                    />
                  )}
                  <CallCategoriesChart callPerformanceData={testCase.data} />
                </div>
              );
            } else if (testCase.isVoiceQuality) { // New condition for Voice Quality
              return (
                <div key={testCase.name} className="report-section">
                  <h3 className="text-xl font-bold mb-4 text-gray-800">{testCase.name}</h3>
                  <VoiceQualityTable data={testCase.data} testName={testCase.name} />
                </div>
              );
            } else if (testCase.isAudioDelay) { // New condition for Audio Delay
              return (
                <div key={testCase.name} className="report-section">
                  <h3 className="text-xl font-bold mb-4 text-gray-800">{testCase.name}</h3>
                  <AudioDelayTable data={testCase.data} testName={testCase.name} />
                </div>
              );
            } else {
              // Render DataPerformanceReport and BarChart for other test cases
              const dutData = testCase.data.DUT || {};
              const refData = testCase.data.REF || {};

              const hasThroughputData = dutData.Throughput || refData.Throughput;
              const hasJitterData = dutData.Jitter || refData.Jitter;
              const hasErrorRatioData = dutData["Error Ratio"] || refData["Error Ratio"];
              const hasWebPageLoadTimeData = dutData["Web Page Load Time"] || refData["Web Page Load Time"];
              const hasPingRttData = dutData["Ping RTT"] || refData["Ping RTT"];

              let metricsToDisplayForTable = [];
              if (hasThroughputData || hasJitterData || hasErrorRatioData || hasWebPageLoadTimeData) {
                metricsToDisplayForTable.push("Throughput", "Jitter", "Error Ratio", "Web Page Load Time");
              }
              if (hasPingRttData) {
                metricsToDisplayForTable.push("Ping RTT");
              }

              const shouldRenderDetailedTable = categoryName === "5G AUTO DP" || categoryName === "5G NSA DP";

              return (
                <div key={testCase.name} className="report-section">
                  <h3 className="text-xl font-bold mb-4 text-gray-800">{testCase.name}</h3>
                  {shouldRenderDetailedTable && (
                    <div className="table-chart-container">
                      {renderStatisticsTable(testCase.name, testCase.data, metricsToDisplayForTable)}
                      <div className="charts-container">
                        {(hasThroughputData || hasJitterData || hasErrorRatioData || hasWebPageLoadTimeData) && (
                          <BarChart testCaseData={testCase.data} testCaseName={testCase.name} isPing={false} />
                        )}
                        {hasPingRttData && (
                          <BarChart testCaseData={testCase.data} testCaseName={testCase.name} isPing={true} />
                        )}
                      </div>
                    </div>
                  )}
                </div>
              );
            }
          })}
        </div>
      ))}

    </>
  );
};

export default DataPerformanceReport;
