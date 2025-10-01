import React from 'react';
import DataPerformanceReport from './DataPerformanceReport';
import BlankTable from './BlankTable'; // Import the BlankTable component
import CoverageTables from './CoverageTables'; // Import the CoverageTables component
import data from './data_analysis_results.json'; // Import the JSON data

function App() {
  // Base station coordinate
  const baseStationCoords = [47.128234, -122.356792];

  // Calculate average DUT coordinates for Last MOS Value
  let dutMosLatSum = 0;
  let dutMosLonSum = 0;
  let dutMosCount = 0;

  for (let i = 1; i <= 3; i++) { // DUT1, DUT2, DUT3
    for (let j = 1; j <= 5; j++) { // Run1 to Run5
      const key = `DUT${i}_Run${j}`;
      const coords = data.Coverage["5G VoNR Coverage Test"][key]?.last_mos_value_coords;
      if (coords) {
        dutMosLatSum += parseFloat(coords.latitude);
        dutMosLonSum += parseFloat(coords.longitude);
        dutMosCount++;
      }
    }
  }
  const avgDutMosCoords = dutMosCount > 0 ? [dutMosLatSum / dutMosCount, dutMosLonSum / dutMosCount] : [0, 0];

  // Calculate average REF coordinates for Last MOS Value
  let refMosLatSum = 0;
  let refMosLonSum = 0;
  let refMosCount = 0;

  for (let i = 1; i <= 3; i++) { // REF1, REF2, REF3
    for (let j = 1; j <= 5; j++) { // Run1 to Run5
      const key = `REF${i}_Run${j}`;
      const coords = data.Coverage["5G VoNR Coverage Test"][key]?.last_mos_value_coords;
      if (coords) {
        refMosLatSum += parseFloat(coords.latitude);
        refMosLonSum += parseFloat(coords.longitude);
        refMosCount++;
      }
    }
  }
  const avgRefMosCoords = refMosCount > 0 ? [refMosLatSum / refMosCount, refMosLonSum / refMosCount] : [0, 0];

  // Calculate average DUT coordinates for Voice Call Drop
  let dutDropLatSum = 0;
  let dutDropLonSum = 0;
  let dutDropCount = 0;

  for (let i = 1; i <= 3; i++) { // DUT1, DUT2, DUT3
    for (let j = 1; j <= 5; j++) { // Run1 to Run5
      const key = `DUT${i}_Run${j}`;
      const coords = data.Coverage["5G VoNR Coverage Test"][key]?.voice_call_drop_coords;
      if (coords) {
        dutDropLatSum += parseFloat(coords.latitude);
        dutDropLonSum += parseFloat(coords.longitude);
        dutDropCount++;
      }
    }
  }
  const avgDutDropCoords = dutDropCount > 0 ? [dutDropLatSum / dutDropCount, dutDropLonSum / dutDropCount] : [0, 0];

  // Calculate average REF coordinates for Voice Call Drop
  let refDropLatSum = 0;
  let refDropLonSum = 0;
  let refDropCount = 0;

  for (let i = 1; i <= 3; i++) { // REF1, REF2, REF3
    for (let j = 1; j <= 5; j++) { // Run1 to Run5
      const key = `REF${i}_Run${j}`;
      const coords = data.Coverage["5G VoNR Coverage Test"][key]?.voice_call_drop_coords;
      if (coords) {
        refDropLatSum += parseFloat(coords.latitude);
        refDropLonSum += parseFloat(coords.longitude);
        refDropCount++;
      }
    }
  }
  const avgRefDropCoords = refDropCount > 0 ? [refDropLatSum / refDropCount, refDropLonSum / refDropCount] : [0, 0];

  // Calculate average DUT coordinates for DL TP < 1
  let dutDlTpLatSum = 0;
  let dutDlTpLonSum = 0;
  let dutDlTpCount = 0;

  for (let i = 1; i <= 3; i++) { // DUT1, DUT2, DUT3
    for (let j = 1; j <= 5; j++) { // Run1 to Run5
      const key = `DUT${i}_Run${j}`;
      const coords = data.Coverage["5G VoNR Coverage Test"][key]?.first_dl_tp_gt_1_coords;
      if (coords) {
        dutDlTpLatSum += parseFloat(coords.latitude);
        dutDlTpLonSum += parseFloat(coords.longitude);
        dutDlTpCount++;
      }
    }
  }
  const avgDutDlTpCoords = dutDlTpCount > 0 ? [dutDlTpLatSum / dutDlTpCount, dutDlTpLonSum / dutDlTpCount] : [0, 0];

  // Calculate average REF coordinates for DL TP < 1
  let refDlTpLatSum = 0;
  let refDlTpLonSum = 0;
  let refDlTpCount = 0;

  for (let i = 1; i <= 3; i++) { // REF1, REF2, REF3
    for (let j = 1; j <= 5; j++) { // Run1 to Run5
      const key = `REF${i}_Run${j}`;
      const coords = data.Coverage["5G VoNR Coverage Test"][key]?.first_dl_tp_gt_1_coords;
      if (coords) {
        refDlTpLatSum += parseFloat(coords.latitude);
        refDlTpLonSum += parseFloat(coords.longitude);
        refDlTpCount++;
      }
    }
  }
  const avgRefDlTpCoords = refDlTpCount > 0 ? [refDlTpLatSum / refDlTpCount, refDlTpLonSum / refDlTpCount] : [0, 0];

  // Calculate average DUT coordinates for UL TP < 1
  let dutUlTpLatSum = 0;
  let dutUlTpLonSum = 0;
  let dutUlTpCount = 0;

  for (let i = 1; i <= 3; i++) { // DUT1, DUT2, DUT3
    for (let j = 1; j <= 5; j++) { // Run1 to Run5
      const key = `DUT${i}_Run${j}`;
      const coords = data.Coverage["5G VoNR Coverage Test"][key]?.first_ul_tp_gt_1_coords;
      if (coords) {
        dutUlTpLatSum += parseFloat(coords.latitude);
        dutUlTpLonSum += parseFloat(coords.longitude);
        dutUlTpCount++;
      }
    }
  }
  const avgDutUlTpCoords = dutUlTpCount > 0 ? [dutUlTpLatSum / dutUlTpCount, dutUlTpLonSum / dutUlTpCount] : [0, 0];

  // Calculate average REF coordinates for UL TP < 1
  let refUlTpLatSum = 0;
  let refUlTpLonSum = 0;
  let refUlTpCount = 0;

  for (let i = 1; i <= 3; i++) { // REF1, REF2, REF3
    for (let j = 1; j <= 5; j++) { // Run1 to Run5
      const key = `REF${i}_Run${j}`;
      const coords = data.Coverage["5G VoNR Coverage Test"][key]?.first_ul_tp_gt_1_coords;
      if (coords) {
        refUlTpLatSum += parseFloat(coords.latitude);
        refUlTpLonSum += parseFloat(coords.longitude);
        refUlTpCount++;
      }
    }
  }
  const avgRefUlTpCoords = refUlTpCount > 0 ? [refUlTpLatSum / refUlTpCount, refUlTpLonSum / refUlTpCount] : [0, 0];

  return (
    <div className="container mx-auto p-4 main-content">
      <h1 className="text-4xl font-bold text-center my-8">Data Performance Analysis Report</h1>
      <h2 className="text-2xl font-semibold text-center mb-10">Comparison of DUT and REF Devices</h2>
      <DataPerformanceReport />
      <CoverageTables
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
