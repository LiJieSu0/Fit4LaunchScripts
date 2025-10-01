import React from 'react';
import DataPerformanceReport from './DataPerformanceReport';
import BlankTable from './BlankTable'; // Import the BlankTable component
import CoverageTables from './CoverageTables'; // Import the CoverageTables component
import data from './data_analysis_results.json'; // Import the JSON data

function App() {
  // Base station coordinate
  const baseStationCoords = [47.128234, -122.356792];

  // Calculate average DUT coordinates
  let dutLatSum = 0;
  let dutLonSum = 0;
  let dutCount = 0;

  for (let i = 1; i <= 3; i++) { // DUT1, DUT2, DUT3
    for (let j = 1; j <= 5; j++) { // Run1 to Run5
      const key = `DUT${i}_Run${j}`;
      const coords = data.Coverage["5G VoNR Coverage Test"][key]?.last_mos_value_coords;
      if (coords) {
        dutLatSum += parseFloat(coords.latitude);
        dutLonSum += parseFloat(coords.longitude);
        dutCount++;
      }
    }
  }
  const avgDutCoords = dutCount > 0 ? [dutLatSum / dutCount, dutLonSum / dutCount] : [0, 0];

  // Calculate average REF coordinates
  let refLatSum = 0;
  let refLonSum = 0;
  let refCount = 0;

  for (let i = 1; i <= 3; i++) { // REF1, REF2, REF3
    for (let j = 1; j <= 5; j++) { // Run1 to Run5
      const key = `REF${i}_Run${j}`;
      const coords = data.Coverage["5G VoNR Coverage Test"][key]?.last_mos_value_coords;
      if (coords) {
        refLatSum += parseFloat(coords.latitude);
        refLonSum += parseFloat(coords.longitude);
        refCount++;
      }
    }
  }
  const avgRefCoords = refCount > 0 ? [refLatSum / refCount, refLonSum / refCount] : [0, 0];

  return (
    <div className="container mx-auto p-4 main-content">
      <h1 className="text-4xl font-bold text-center my-8">Data Performance Analysis Report</h1>
      <h2 className="text-2xl font-semibold text-center mb-10">Comparison of DUT and REF Devices</h2>
      <DataPerformanceReport />
      <CoverageTables
        avgDutCoords={avgDutCoords}
        avgRefCoords={avgRefCoords}
        baseStationCoords={baseStationCoords}
      />
      {/* <BlankTable /> BlankTable component here don't touch*/}
    </div>
  );
}

export default App;
