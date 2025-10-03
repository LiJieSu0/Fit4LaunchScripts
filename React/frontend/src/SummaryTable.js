import React from 'react';
import './SummaryTable.css'; // Assuming we'll create this for styling

const SummaryTable = () => {
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
            <tr>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
            </tr>
            <tr>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
            </tr>
            <tr>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
            </tr>
            <tr>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
            </tr>
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
            <tr>
              <td>Call Performance</td>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
            </tr>
            <tr>
              <td>Data Performance</td>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
            </tr>
            <tr>
              <td>Voice Quality</td>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
            </tr>
            <tr>
              <td>Coverage Performance</td>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
            </tr>
            <tr>
              <td>WFC</td>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
            </tr>
          </tbody>
        </table>
      </div>

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
    </div>
  );
};

export default SummaryTable;
