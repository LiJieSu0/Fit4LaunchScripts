import React from 'react';
import { useParams } from 'react-router-dom';
import DataPerformanceReport from './DataPerformanceReport';
import allResults from './data_analysis_results.json';

const extractTestCases = (data, currentPath = []) => {
  let extracted = [];

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

  for (const key in data) {
    if (typeof data[key] === 'object' && data[key] !== null) {
      extracted = extracted.concat(extractTestCases(data[key], [...currentPath, key]));
    }
  }

  return extracted;
};

const CategoryPage = ({ categoryName }) => {
  const allFlattenedTestCases = extractTestCases(allResults);
  const filteredTestCases = allFlattenedTestCases.filter(testCase => {
    if (categoryName === "5G AUTO DP") {
      return testCase.name.startsWith("5G AUTO DP") || testCase.name.startsWith("5G VoNR MRAB Stationary");
    }
    return testCase.name.startsWith(categoryName);
  });

  // Group test cases by their top-level category for rendering headers
  const groupedByCategories = filteredTestCases.reduce((acc, testCase) => {
    let category = testCase.name.split(' - ')[0];
    if (category === "5G VoNR MRAB Stationary") {
      category = "5G AUTO DP"; // Group MRAB under 5G AUTO DP
    }
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(testCase);
    return acc;
  }, {});

  return (
    <div className="container mx-auto p-4 main-content">
      <h1 className="text-4xl font-bold text-center my-8">{categoryName} Data Performance Analysis Report</h1>
      <h2 className="text-2xl font-semibold text-center mb-10">Comparison of DUT and REF Devices</h2>
      {Object.entries(groupedByCategories).map(([currentCategoryName, testCases]) => {
        let sortedTestCases = [...testCases];
        if (currentCategoryName === "5G AUTO DP") {
          // Sort "5G AUTO DP" test cases to put "5G VoNR MRAB Stationary" at the end
          sortedTestCases.sort((a, b) => {
            if (a.name.startsWith("5G VoNR MRAB Stationary")) return 1;
            if (b.name.startsWith("5G VoNR MRAB Stationary")) return -1;
            return 0;
          });
        }

        return (
          <React.Fragment key={currentCategoryName}>
            {/* Only render the category header if it's different from the main categoryName prop */}
            {/* {currentCategoryName !== categoryName && (
              <h2 className="text-2xl font-bold mb-6 text-blue-700">{currentCategoryName}</h2>
            )} */}
            {sortedTestCases.map(testCase => (
              <div key={testCase.name} className="report-section">
                <h3 className="text-xl font-bold mb-4 text-gray-800">{testCase.name.replace(`${categoryName} - `, '')}</h3>
                <div className="table-chart-container">
                  <DataPerformanceReport
                    testCaseName={testCase.name}
                    testCaseData={testCase.data}
                    isPing={testCase.isPing}
                    renderStatisticsTable={DataPerformanceReport.renderStatisticsTable} // Pass down the render function
                  />
                </div>
              </div>
            ))}
          </React.Fragment>
        );
      })}
    </div>
  );
};

export default CategoryPage;
