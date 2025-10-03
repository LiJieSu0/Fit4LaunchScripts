import React from 'react';
import allResults from './data_analysis_results.json'; // Assuming data_analysis_results.json is the source
import CallPerformanceTable from './CallPerformanceTable';
import CallCategoriesChart from './CallCategoriesChart';
import PValueTable from './PValueTable';

// Helper function to extract only Call Performance test cases
const extractCallPerformanceTestCases = (data, currentPath = []) => {
  let extracted = [];

  // Check if the current data object is a Call Performance test case
  if (data.DUT && data.REF && typeof data.initiation_p_value === 'number' && typeof data.retention_p_value === 'number') {
    extracted.push({
      name: currentPath.join(" - "),
      data: data,
      isCallPerformance: true,
    });
    return extracted; // Stop further recursion for this branch
  }

  // Recurse into children
  for (const key in data) {
    if (typeof data[key] === 'object' && data[key] !== null) {
      const result = extractCallPerformanceTestCases(data[key], [...currentPath, key]);
      extracted = extracted.concat(result);
    }
  }

  return extracted;
};

const CallPerformanceReport = () => {
  const callPerformanceTestCases = extractCallPerformanceTestCases(allResults);

  // Group test cases by their top-level category for rendering headers
  const groupedByCategories = callPerformanceTestCases.reduce((acc, testCase) => {
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
            if (testCase.isCallPerformance) {
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
            }
            return null;
          })}
        </div>
      ))}
    </>
  );
};

export default CallPerformanceReport;
