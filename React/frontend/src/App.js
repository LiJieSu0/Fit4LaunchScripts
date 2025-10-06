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
  const coverageData = data["Coverage Performance"]["5G VoNR Coverage Test"];
  const n41HPUECoverageData = data["Coverage Performance"]["5G n41 HPUE Coverage Test"];

  // Helper function to calculate average coordinates for a specific band, device type, and metric
  const calculateAverageCoords = (band, deviceType, metricKey) => {
    let latSum = 0;
    let lonSum = 0;
    let count = 0;

    const bandData = coverageData[band];
    if (!bandData || !bandData[deviceType]) {
      return [0, 0];
    }

    // Iterate through runs (Run1 to Run5)
    for (let i = 1; i <= 5; i++) {
      const runKey = `Run${i}`;
      const runData = bandData[deviceType][runKey];
      if (runData && runData[metricKey]) {
        latSum += parseFloat(runData[metricKey].latitude);
        lonSum += parseFloat(runData[metricKey].longitude);
        count++;
      }
    }
    return count > 0 ? [latSum / count, lonSum / count] : [0, 0];
  };

  // Function to prepare data for CoverageTables component for a specific band
  const getCoverageDataForBand = (band) => {
    const bandData = coverageData[band];
    if (!bandData) return null;

    const metrics = {
      "last_mos_value_coords": "Last MOS Value Distance (km)",
      "voice_call_drop_coords": "Voice Call Drop Distance (km)",
      "first_dl_tp_gt_1_coords": "DL TP < 1 Distance (km)",
      "first_ul_tp_gt_1_coords": "UL TP < 1 Distance (km)",
    };

    const processedData = {};
    const avgCoords = {};

    for (const metricKey in metrics) {
      processedData[metricKey] = {
        DUT: {},
        REF: {}
      };
      avgCoords[`avgDut${metricKey.replace(/_coords$/, '').split('_').map(s => s.charAt(0).toUpperCase() + s.slice(1)).join('')}`] = calculateAverageCoords(band, "DUT", metricKey);
      avgCoords[`avgRef${metricKey.replace(/_coords$/, '').split('_').map(s => s.charAt(0).toUpperCase() + s.slice(1)).join('')}`] = calculateAverageCoords(band, "REF", metricKey);

      const runs = ["Run1", "Run2", "Run3", "Run4", "Run5"];
      const devices = ["DUT", "REF"];

      devices.forEach(device => {
        let sumDistance = 0;
        let runCount = 0;
        runs.forEach(run => {
          const runData = bandData[device]?.[run]?.[metricKey];
          if (runData && runData.distance_to_base_station_km !== undefined) {
            const distance = parseFloat(runData.distance_to_base_station_km);
            processedData[metricKey][device][run] = distance.toFixed(3);
            sumDistance += distance;
            runCount++;
          } else {
            processedData[metricKey][device][run] = 'N/A';
          }
        });
        processedData[metricKey][device].Average = runCount > 0 ? (sumDistance / runCount).toFixed(3) : 'N/A';
      });
    }

    return { processedData, avgCoords };
  };

  const bands = ["n25", "n41", "n71"];
  const coverageReports = bands.map(band => ({
    bandName: band,
    data: getCoverageDataForBand(band)
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
      <h1 className="text-4xl font-bold text-center my-8">ATMCL Field Performance Test Report</h1>
      <SummaryTable summaryData={summaryTableData} />
      <CallPerformanceReport /> {/* Render the CallPerformanceReport component */}
      <DataPerformanceReport />
      <VoiceQualityReport /> {/* Render the VoiceQualityReport component */}
      
      {coverageReports.map((report, index) => (
        <CoverageTables
          key={report.bandName}
          categoryName="Coverage Performance"
          testCaseName={`5G VoNR Coverage Test - ${report.bandName.toUpperCase()}`}
          processedCoverageData={report.data.processedData}
          avgCoords={report.data.avgCoords}
          baseStationCoords={baseStationCoords}
          displayCategoryTitle={index === 0} // Only display for the first band (N25)
        />
      ))}

      {/* 5G n41 HPUE Coverage Test - Placeholder, no action for now */}
      {n41HPUECoverageData && (
        <div className="category-section">
          <h3 className="text-xl font-bold mb-4 text-gray-800">5G n41 HPUE Coverage Test</h3>
          <p>Data for 5G n41 HPUE Coverage Test will be displayed here later.</p>
        </div>
      )}

      {/* <BlankTable /> BlankTable component here don't touch*/}
    </div>
  );
}

export default App;
