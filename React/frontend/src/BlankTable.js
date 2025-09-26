import React from 'react';
import './BlankTable.css'; // Import a CSS file for styling

const BlankTable = () => {
  const tests = [
    "5G Auto Data Test Stationary Location 1 DL",
    "5G Auto Data Test Stationary Location 2 DL",
    "5G Auto Data Test Stationary Location 3 DL",
    "5G Auto Data Test Stationary Location 1 UL",
    "5G Auto Data Test Stationary Location 2 UL",
    "LTE Data Test Stationary Poor RF UL",
    "LTE Data Test Drive",
    "LTE Data Web-Kepler",
  ];

  const kpis = [
    "HTTP SS Tput-Avg.",
    "Data Tput Avg.HTTP MS",
    "UDP Tput Avg.",
    "UDP Jitter",
    "UDP Latency",
    "UDP Packet Loss",
    "PING",
    "Webpage DL -Load time",
  ];

  return (
    <div className="blank-table-wrapper">
      <h2>Data performance summary</h2>
      <table className="data-performance-table">
        <thead>
          <tr>
            <th rowSpan="3" className="header-cell summary-header">Data Performance Summary</th>
            <th colSpan={kpis.length * 2} className="header-cell kpi-header">KPI for Data Performance</th>
            <th rowSpan="3" className="header-cell">Pass/Fail & Links</th>
          </tr>
          <tr>
            {kpis.map((kpi, index) => (
              <th colSpan="2" key={index} className="header-cell kpi-sub-header">{kpi}</th>
            ))}
          </tr>
          <tr>
            {kpis.map((_, index) => (
              <React.Fragment key={index}>
                <th className="header-cell du-ref-header">DUT</th>
                <th className="header-cell du-ref-header">REF</th>
              </React.Fragment>
            ))}
          </tr>
        </thead>
        <tbody>
          {tests.map((test, rowIndex) => (
            <tr key={rowIndex}>
              <td className="test-name-cell">{test}</td>
              {/* Empty cells for DU/REF */}
              {Array(kpis.length * 2).fill(null).map((_, cellIndex) => (
                <td key={cellIndex} className="data-cell"></td>
              ))}
              <td className="data-cell"></td> {/* Empty cell for Pass/Fail & Links */}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default BlankTable;
