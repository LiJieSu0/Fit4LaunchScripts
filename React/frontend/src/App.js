import React from 'react';
import DataPerformanceReport from './DataPerformanceReport';
import CallPerformanceReport from './CallPerformanceReport'; // Import the CallPerformanceReport component
import VoiceQualityReport from './VoiceQualityReport'; // Import the VoiceQualityReport component
import BlankTable from './BlankTable'; // Import the BlankTable component
import CoverageTables from './CoverageTables'; // Import the CoverageTables component
import SummaryTable from './SummaryTable'; // Import the SummaryTable component
import data from './data_analysis_results.json'; // Import the JSON data
import './print.css'; // Import print-specific styles

function App() {
  // Base station coordinate
  const baseStationCoords = [47.128234, -122.356792];

  // Calculate average DUT coordinates for Last MOS Value
  let dutMosLatSum = 0;
  let dutMosLonSum = 0;
  let dutMosCount = 0;

  const coverageData = data["Coverage Performance"]["5G VoNR Coverage Test"];

  // Helper function to calculate average coordinates
  const calculateAverageCoords = (devicePrefix, metricKey) => {
    let latSum = 0;
    let lonSum = 0;
    let count = 0;

    for (let i = 1; i <= 3; i++) { // DUT1, DUT2, DUT3 or REF1, REF2, REF3
      for (let j = 1; j <= 5; j++) { // Run1 to Run5
        const key = `${devicePrefix}${i}_Run${j}`;
        const coords = coverageData[key]?.[metricKey];
        if (coords) {
          latSum += parseFloat(coords.latitude);
          lonSum += parseFloat(coords.longitude);
          count++;
        }
      }
    }
    return count > 0 ? [latSum / count, lonSum / count] : [0, 0];
  };

  const avgDutMosCoords = calculateAverageCoords("DUT", "last_mos_value_coords");
  const avgRefMosCoords = calculateAverageCoords("REF", "last_mos_value_coords");
  const avgDutDropCoords = calculateAverageCoords("DUT", "voice_call_drop_coords");
  const avgRefDropCoords = calculateAverageCoords("REF", "voice_call_drop_coords");
  const avgDutDlTpCoords = calculateAverageCoords("DUT", "first_dl_tp_gt_1_coords");
  const avgRefDlTpCoords = calculateAverageCoords("REF", "first_dl_tp_gt_1_coords");
  const avgDutUlTpCoords = calculateAverageCoords("DUT", "first_ul_tp_gt_1_coords");
  const avgRefUlTpCoords = calculateAverageCoords("REF", "first_ul_tp_gt_1_coords");

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
      <h1 className="text-4xl font-bold text-center my-8">ATMCL Field Performance Test Report</h1>
      <SummaryTable summaryData={summaryTableData} />
      <CallPerformanceReport /> {/* Render the CallPerformanceReport component */}
      <DataPerformanceReport />
      <VoiceQualityReport /> {/* Render the VoiceQualityReport component */}
      <CoverageTables
        categoryName="Coverage Performance"
        testCaseName="5G VoNR Coverage Test"
        rawCoverageData={coverageData}
        avgDutMosCoords={avgDutMosCoords}
        avgRefMosCoords={avgRefMosCoords}
        avgDutDropCoords={avgDutDropCoords}
        avgRefDropCoords={avgRefDropCoords}
        avgDutDlTpCoords={avgDutDlTpCoords}
        avgRefDlTpCoords={avgRefDlTpCoords}
        avgDutUlTpCoords={avgDutUlTpCoords}
        avgRefUlTpCoords={avgRefUlTpCoords}
        baseStationCoords={baseStationCoords}
      />
      {/* <BlankTable /> BlankTable component here don't touch*/}
    </div>
  );
}

export default App;
