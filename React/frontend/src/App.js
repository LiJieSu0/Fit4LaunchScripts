import React from 'react';
import DataPerformanceReport from './DataPerformanceReport';
import CallPerformanceReport from './CallPerformanceReport'; // Import the CallPerformanceReport component
import VoiceQualityReport from './VoiceQualityReport'; // Import the VoiceQualityReport component
import BlankTable from './BlankTable'; // Import the BlankTable component
import CoverageTables from './CoverageTables'; // Import the CoverageTables component
import CategoryPage from './CategoryPage'; // Import the CategoryPage component
import SummaryTable from './SummaryTable'; // Import the SummaryTable component
import data from './data_analysis_results.json'; // Import the JSON data
import './print.css'; // Import print-specific styles
import RsrpChart from './RsrpChart'; // Import the RsrpChart component
import TxPowerChart from './TxPowerChart'; // Import the TxPowerChart component
import CoverageDistanceTable from './CoverageDistanceTable'; // Import the new table component
import coverageDistanceData from './coverage_distance_data.json'; // Import the processed data

function App() {
  // Base station coordinate
  const baseStationCoords = [47.128234, -122.356792];

  // Calculate average DUT coordinates for Last MOS Value
  const coverageData = data["Coverage Performance"]["5G VoNR Coverage Test"];
  const n41HPUECoverageData = data["Coverage Performance"]["5G n41 HPUE Coverage Test"];

  const bands = ["n25", "n41", "n71"];
  const coverageReports = bands.map(band => ({
    bandName: band,
    data: coverageData[band] // Pass the raw coverage data for the specific band
  })).filter(report => report.data !== null);

  // Calculate summary data for the SummaryTable
  const calculateSummaryData = () => {
    const summary = [
      { category: "Call Performance", completed: 0, passed: "N/A", issues: "N/A", link: "N/A", time: "N/A" },
      { category: "Data Performance", completed: 0, passed: "N/A", issues: "N/A", link: "N/A", time: "N/A" },
      { category: "Voice Quality", completed: 0, passed: "N/A", issues: "N/A", link: "N/A", time: "N/A" },
      { category: "Coverage Performance", completed: 0, passed: "N/A", issues: "N/A", link: "N/A", time: "N/A" },
      { category: "WFC", completed: 0, passed: "N/A", issues: "N/A", link: "N/A", time: "N/A" },
    ];

    summary.forEach(item => {
      if (data[item.category]) {
        // Count direct sub-objects as completed test cases
        item.completed = Object.keys(data[item.category]).length;
      }
    });
    return summary;
  };

  const summaryTableData = []; // Changed to an empty array as per user's request

  return (
    <div className="container mx-auto p-4 main-content">
      <h1 className="text-4xl font-bold text-center my-8">Samsung Galaxy Fold S34 Performance Test Report</h1>
      <SummaryTable summaryData={summaryTableData} />
      <CategoryPage title="Call Performance Summary" />
      <CallPerformanceReport /> {/* Render the CallPerformanceReport component */}
      <CategoryPage title="Data Performance Summary" />
      <DataPerformanceReport />
      <CategoryPage title="Voice Quality Summary" />
      <VoiceQualityReport /> {/* Render the VoiceQualityReport component */}
      <CategoryPage title="Coverage Performance Summary" />
        <CoverageTables
          categoryName="Coverage Performance"
          testCaseName="5G VoNR Coverage Test - N25, N41, N71"
          coverageData={coverageData}
          baseStationCoords={baseStationCoords}
          displayCategoryTitle={false}
        />

      {/* 5G n41 HPUE Coverage Test */}
      <div className="category-section">
        <h3 className="text-xl font-bold mb-4 text-gray-800">5G n41 HPUE Coverage Test</h3>
        {/* New table for Coverage Distance */}
        <CoverageDistanceTable 
            title="Distance to Base Station (km)" 
            headers={coverageDistanceData.headers} 
            rows={coverageDistanceData.rows} 
        />
        {[1, 2, 3, 4, 5].map(runNum => (
          <RsrpChart key={runNum} runNumber={runNum} />
        ))}
        <h3 className="text-xl font-bold mb-4 text-gray-800 mt-8">Tx Power Analysis</h3>
        {[1, 2, 3, 4, 5].map(runNum => (
          <TxPowerChart key={`tx-${runNum}`} runNumber={runNum} />
        ))}
      </div>

      {/* <BlankTable /> BlankTable component here don't touch*/}
    </div>
  );
}

export default App;
