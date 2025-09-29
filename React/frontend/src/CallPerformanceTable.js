import React from 'react';

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

  return (
    <div className="overflow-x-auto mb-6 table-container">
      <table className="min-w-full border border-table-grid">
        <thead>
          <tr className="bg-table-header-bg text-table-header-text font-bold">
            <th className="py-2 px-4 border border-table-grid">Device</th>
            <th className="py-2 px-4 border border-table-grid">Connection Attempts</th>
            <th className="py-2 px-4 border border-table-grid">Mean Setup Time (s)</th>
            <th className="py-2 px-4 border border-table-grid">Successful Initiations</th>
            <th className="py-2 px-4 border border-table-grid">Successful Initiations (%)</th>
            <th className="py-2 px-4 border border-table-grid">Failed Initiations</th>
            <th className="py-2 px-4 border border-table-grid">Failed Initiations (%)</th>
            <th className="py-2 px-4 border border-table-grid">P - Value</th>
          </tr>
        </thead>
        <tbody>
          <tr className="bg-table-body-bg">
            <td className="py-2 px-4 border border-table-grid text-center">DUT</td>
            <td className="py-2 px-4 border border-table-grid text-center">{dutTotalAttempts}</td>
            <td className="py-2 px-4 border border-table-grid text-center">{DUT.mean_setup_time.toFixed(2)}</td>
            <td className="py-2 px-4 border border-table-grid text-center">{dutSuccessfulInitiations}</td>
            <td className="py-2 px-4 border border-table-grid text-center">{dutSuccessfulInitiationsPercentage}%</td>
            <td className="py-2 px-4 border border-table-grid text-center">{dutFailedInitiations}</td>
            <td className="py-2 px-4 border border-table-grid text-center">{dutFailedInitiationsPercentage}%</td>
            <td className="py-2 px-4 border border-table-grid text-center">{initiation_p_value.toFixed(3)}</td>
          </tr>
          <tr className="bg-table-body-bg">
            <td className="py-2 px-4 border border-table-grid text-center">REF</td>
            <td className="py-2 px-4 border border-table-grid text-center">{refTotalAttempts}</td>
            <td className="py-2 px-4 border border-table-grid text-center">{REF.mean_setup_time.toFixed(2)}</td>
            <td className="py-2 px-4 border border-table-grid text-center">{refSuccessfulInitiations}</td>
            <td className="py-2 px-4 border border-table-grid text-center">{refSuccessfulInitiationsPercentage}%</td>
            <td className="py-2 px-4 border border-table-grid text-center">{refFailedInitiations}</td>
            <td className="py-2 px-4 border border-table-grid text-center">{refFailedInitiationsPercentage}%</td>
            <td className="py-2 px-4 border border-table-grid text-center">{retention_p_value.toFixed(3)}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default CallPerformanceTable;
