import React from 'react';
import './SummaryTable.css'; // Assuming we'll create this for styling

const SummaryTable = ({ summaryData }) => {
  return (
    <div className="summary-report-container">
      <div className="table-section">
        <h3 className="table-title">Test Devices</h3>
        <table className="dut-ref-table">
          <thead>
            <tr>
              <th>DUT</th>
              <th>S. No./IMEI</th>
              <th>REF</th>
              <th>S. No./IMEI</th>
            </tr>
          </thead>
          <tbody>
            {/* Static rows for Test Devices, as this data is not in the JSON */}
            <tr><td>Samsung XCover Pro 7</td><td>AP3A.240905.015.A2.G766USQS2AYG1／354877970010297</td><td>Samsung GS25 FE</td><td>BP2A.250605.031.A3.S731USQU1AYH5／358625370021547</td></tr>
            <tr><td>Samsung XCover Pro 7</td><td>AP3A.240905.015.A2.G766USQS2AYG1／354877970011428</td><td>Samsung GS25 FE</td><td>BP2A.250605.031.A3.S731USQU1AYH5／358625370020499</td></tr>
            <tr><td>Samsung XCover Pro 7</td><td>AP3A.240905.015.A2.G766USQS2AYG1／354877970012160</td><td>Samsung GS25 FE</td><td>BP2A.250605.031.A3.S731USQU1AYH5／358625370022602</td></tr>
            <tr><td>Samsung XCover Pro 7</td><td>AP3A.240905.015.A2.G766USQS2AYG1／354877970012335</td><td>Samsung GS25 FE</td><td>BP2A.250605.031.A3.S731USQU1AYH5／358625370021935</td></tr>
            <tr><td>Samsung XCover Pro 7</td><td>AP3A.240905.015.A2.G766USQS2AYG1／354877970011139</td><td>Samsung GS25 FE</td><td>BP2A.250605.031.A3.S731USQU1AYH5／358625370022487</td></tr>
            <tr><td>Samsung XCover Pro 7</td><td>AP3A.240905.015.A2.G766USQS2AYG1／354877970011535</td><td>Samsung GS25 FE</td><td>BP2A.250605.031.A3.S731USQU1AYH5／358625370020408</td></tr>
            <tr><td>Samsung XCover Pro 7</td><td>AP3A.240905.015.A2.G766USQS2AYG1／354877970010388</td><td>Samsung GS25 FE</td><td>BP2A.250605.031.A3.S731USQU1AYH5／358625370022867</td></tr>
            <tr><td>Samsung XCover Pro 7</td><td>AP3A.240905.015.A2.G766USQS2AYG1／354877970012210</td><td>Samsung GS25 FE</td><td>BP2A.250605.031.A3.S731USQU1AYH5／358625370021489</td></tr>
            <tr><td>Samsung XCover Pro 7</td><td>AP3A.240905.015.A2.G766USQS2AYG1／354877970011048</td><td>Samsung GS25 FE</td><td>BP2A.250605.031.A3.S731USQU1AYH5／358625370021489</td></tr>
            <tr><td>Samsung XCover Pro 7</td><td>AP3A.240905.015.A2.G766USQS2AYG1／354877970012475</td><td>Samsung GS25 FE</td><td>BP2A.250605.031.A3.S731USQU1AYH5／358625370021596</td></tr>
          </tbody>
        </table>
      </div>

      <h3 className="report-title">Performance Summary Report</h3>

      <div className="table-section">
        <table className="performance-summary-table">
          <thead>
            <tr>
              <th>Category</th>
              <th>% Completed</th>
              <th>% Passed</th>
              <th>Issues</th>
              <th>Link to Issue Page</th>
              <th>Time to complete</th>
            </tr>
          </thead>
          <tbody>
            {[
              "Call Performance",
              "Data Performance",
              "Voice Quality",
              "Coverage Performance",
              "WFC",
            ].map((category, index) => {
              const item = summaryData.find(dataItem => dataItem.category === category) || {};
              return (
                <tr key={index}>
                  <td>{category}</td>
                  <td>{item.completed ? (item.completed > 0 ? `${item.completed} Test Cases` : 'N/A') : ''}</td>
                  <td>{item.passed || ''}</td>
                  <td>{item.issues || ''}</td>
                  <td>{item.link || ''}</td>
                  <td>{item.time || ''}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      <div className="page-break-always"> </div>
      <div className="submission-approval-section">
        <h3 className="submission-approval-title">Submission Approval</h3>
        <div className="signature-block">
          <p>Signature of Manager Test Team</p>
          <p className="date-field">Date</p>
        </div>
        <div className="signature-block">
          <p>Signature of T-Mobile Device Certification</p>
          <p className="date-field">Date</p>
        </div>
      </div>
      <div className='page-break-always'></div> 
      {/* changing page when printing */}
    </div>
  );
};

export default SummaryTable;
