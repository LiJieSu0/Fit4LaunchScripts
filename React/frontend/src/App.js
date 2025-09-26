import React from 'react';
import DataPerformanceReport from './DataPerformanceReport';
import BlankTable from './BlankTable'; // Import the BlankTable component

function App() {
  return (
    <div className="container mx-auto p-4 main-content">
      <h1 className="text-4xl font-bold text-center my-8">Data Performance Analysis Report</h1>
      <h2 className="text-2xl font-semibold text-center mb-10">Comparison of DUT and REF Devices</h2>
      <DataPerformanceReport />
      {/* <BlankTable /> BlankTable component here don't touch*/}
    </div>
  );
}

export default App;
