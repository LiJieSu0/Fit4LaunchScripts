import React, { useState, useEffect } from 'react';
import './PingStatisticsTable.css';
import data from './data_analysis_results.json';

const PingStatisticsTable = () => {
  const [pingData, setPingData] = useState([]);

  useEffect(() => {
    processPingData(data);
  }, []);

  const processPingData = (jsonData) => {
    const processedPingRows = [];

    Object.keys(jsonData).forEach(category => {
      Object.keys(jsonData[category]).forEach(testName => {
        const testData = jsonData[category][testName];
        const dutRefEntries = Object.keys(testData).filter(key => key.includes('DUT') || key.includes('REF'));

        dutRefEntries.forEach(dutRefKey => {
          const deviceData = testData[dutRefKey];
          if (deviceData["Ping RTT"]) {
            processedPingRows.push({
              testName: testName,
              deviceType: deviceData["Device Type"],
              min: deviceData["Ping RTT"].min !== undefined ? deviceData["Ping RTT"].min.toFixed(2) : 'N/A',
              max: deviceData["Ping RTT"].max !== undefined ? deviceData["Ping RTT"].max.toFixed(2) : 'N/A',
              avg: deviceData["Ping RTT"].avg !== undefined ? deviceData["Ping RTT"].avg.toFixed(2) : 'N/A',
              std_dev: deviceData["Ping RTT"].std_dev !== undefined ? deviceData["Ping RTT"].std_dev.toFixed(2) : 'N/A',
            });
          }
        });
      });
    });
    setPingData(processedPingRows);
  };

  return (
    <div className="ping-statistics-table-container">
      <h2>Ping RTT Statistics</h2>
      <table className="ping-statistics-table">
        <thead>
          <tr>
            <th className="header-cell">Test Name</th>
            <th className="header-cell">Device Type</th>
            <th className="header-cell">Min (ms)</th>
            <th className="header-cell">Max (ms)</th>
            <th className="header-cell">Avg (ms)</th>
            <th className="header-cell">Std Dev (ms)</th>
          </tr>
        </thead>
        <tbody>
          {pingData.map((row, rowIndex) => (
            <tr key={rowIndex}>
              <td className="test-name-cell">{row.testName}</td>
              <td className="data-cell">{row.deviceType}</td>
              <td className="data-cell">{row.min}</td>
              <td className="data-cell">{row.max}</td>
              <td className="data-cell">{row.avg}</td>
              <td className="data-cell">{row.std_dev}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default PingStatisticsTable;
