import React, { useState, useEffect } from 'react';
import './DataPerformanceTable.css';
import data from './data_analysis_results.json';

const DataPerformanceTable = () => {
  const [tableData, setTableData] = useState([]);
  const [kpis, setKpis] = useState([]);

  useEffect(() => {
    processData(data);
  }, []);

  const processData = (jsonData) => {
    const processedRows = [];
    const uniqueKpis = new Set();

    Object.keys(jsonData).forEach(category => {
      Object.keys(jsonData[category]).forEach(testName => {
        const testData = jsonData[category][testName];
        const row = { testName: testName };
        const dutRefEntries = Object.keys(testData).filter(key => key.includes('DUT') || key.includes('REF'));

        dutRefEntries.forEach(dutRefKey => {
          const deviceData = testData[dutRefKey];
          const deviceType = deviceData["Device Type"];

          Object.keys(deviceData).forEach(metric => {
            if (typeof deviceData[metric] === 'object' && deviceData[metric] !== null) {
              if (metric === "Throughput" || metric === "Jitter" || metric === "Error Ratio") {
                uniqueKpis.add(metric);
                row[`${metric}_${deviceType}`] = deviceData[metric].Mean !== undefined ? deviceData[metric].Mean.toFixed(2) : 'N/A';
              } else if (metric === "Ping RTT") {
                uniqueKpis.add(metric);
                row[`${metric}_${deviceType}`] = deviceData[metric].avg !== undefined ? deviceData[metric].avg.toFixed(2) : 'N/A';
              } else if (metric === "Web Page Load Time") {
                uniqueKpis.add(metric);
                row[`${metric}_${deviceType}`] = deviceData[metric].Mean !== undefined ? deviceData[metric].Mean.toFixed(2) : 'N/A';
              }
            }
          });
        });
        processedRows.push(row);
      });
    });

    setKpis(Array.from(uniqueKpis));
    setTableData(processedRows);
  };

  return (
    <div className="data-performance-table-container">
      <h2>Data Performance Summary</h2>
      <table className="data-performance-table">
        <thead>
          <tr>
            <th rowSpan="3" className="header-cell summary-header">Test Name</th>
            <th colSpan={kpis.length * 2} className="header-cell kpi-header">KPI for Data Performance</th>
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
          {tableData.map((row, rowIndex) => (
            <tr key={rowIndex}>
              <td className="test-name-cell">{row.testName}</td>
              {kpis.map((kpi, kpiIndex) => (
                <React.Fragment key={kpiIndex}>
                  <td className="data-cell">{row[`${kpi}_DUT`] || 'N/A'}</td>
                  <td className="data-cell">{row[`${kpi}_REF`] || 'N/A'}</td>
                </React.Fragment>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DataPerformanceTable;
