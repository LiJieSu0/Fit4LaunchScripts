import React from 'react';
import { getCallSetupTimeStatusAndClass } from './CallPerformanceSummaryTable'; // Import the helper function

const CallPerformanceTable = ({ callPerformanceData }) => {
  if (!callPerformanceData) {
    return <p>No Call Performance data available.</p>;
  }

  const { DUT, REF, initiation_p_value, retention_p_value } = callPerformanceData;

  // Calculate percentages for DUT
  const dutTotalAttempts = DUT.total_attempts;
  const dutSuccessfulInitiations = DUT.total_initiation_successes;
  const dutFailedInitiations = DUT.total_initiation_failures;
  const dutSuccessfulInitiationsPercentage = (dutTotalAttempts > 0) ? ((dutSuccessfulInitiations / dutTotalAttempts) * 100).toFixed(2) : "0.00";
  const dutFailedInitiationsPercentage = (dutTotalAttempts > 0) ? ((dutFailedInitiations / dutTotalAttempts) * 100).toFixed(2) : "0.00";

  // Calculate percentages for REF
  const refTotalAttempts = REF.total_attempts;
  const refSuccessfulInitiations = REF.total_initiation_successes;
  const refFailedInitiations = REF.total_initiation_failures;
  const refSuccessfulInitiationsPercentage = (refTotalAttempts > 0) ? ((refSuccessfulInitiations / refTotalAttempts) * 100).toFixed(2) : "0.00";
  const refFailedInitiationsPercentage = (refTotalAttempts > 0) ? ((refFailedInitiations / refTotalAttempts) * 100).toFixed(2) : "0.00";

  const dutAvgSetupTime = callPerformanceData.DUT.mean_setup_time;
  const refAvgSetupTime = callPerformanceData.REF.mean_setup_time;
  const { className: callSetupBgClass } = getCallSetupTimeStatusAndClass(dutAvgSetupTime, refAvgSetupTime);

  return (
    <div className="overflow-x-auto mb-6 table-container">
      <table className="common-table">
        <thead>
          <tr>
            <th>Device</th>
            <th>Connection Attempts</th>
            <th>Mean Setup Time (s)</th>
            <th>Successful Initiations</th>
            <th>Successful Initiations (%)</th>
            <th>Failed Initiations</th>
            <th>Failed Initiations (%)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>DUT</td>
            <td>{dutTotalAttempts}</td>
            <td className={callSetupBgClass}>{DUT.mean_setup_time.toFixed(2)}</td>
            <td>{dutSuccessfulInitiations}</td>
            <td>{dutSuccessfulInitiationsPercentage}%</td>
            <td>{dutFailedInitiations}</td>
            <td>{dutFailedInitiationsPercentage}%</td>
          </tr>
          <tr>
            <td>REF</td>
            <td>{refTotalAttempts}</td>
            <td className={callSetupBgClass}>{REF.mean_setup_time.toFixed(2)}</td>
            <td>{refSuccessfulInitiations}</td>
            <td>{refSuccessfulInitiationsPercentage}%</td>
            <td>{refFailedInitiations}</td>
            <td>{refFailedInitiationsPercentage}%</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default CallPerformanceTable;
