import React from 'react';
import data from './data_analysis_results.json';

const CallPerformanceSummaryTable = () => {
  const callPerformanceData = data['Call Performance'];

  const calculatePercentage = (numerator, denominator) => {
    if (denominator === 0) return 'N/A';
    return ((numerator / denominator) * 100).toFixed(2) + '%';
  };

  return (
    <div className="call-performance-summary-table-container mb-8">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Call Performance Summary -Seattle Market</h2>
      <table className="min-w-full divide-y divide-gray-200 border border-gray-300">
        <thead className="bg-gray-600 text-white">
          <tr>
            <th rowSpan="3" className="px-2 py-1 text-left text-xs font-medium uppercase tracking-wider border border-gray-300">Test Cases</th>
            <th colSpan="6" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">KPI for Call Performance Mobility</th>
            <th rowSpan="3" className="px-2 py-1 text-left text-xs font-medium uppercase tracking-wider border border-gray-300">Network Tech.</th>
            <th rowSpan="3" className="px-2 py-1 text-left text-xs font-medium uppercase tracking-wider border border-gray-300">Pass/Fail</th>
            <th rowSpan="3" className="px-2 py-1 text-left text-xs font-medium uppercase tracking-wider border border-gray-300">Comments/Links</th>
          </tr>
          <tr>
            <th colSpan="2" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">Call Setup Time</th>
            <th colSpan="2" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">Call Initiation Success</th>
            <th colSpan="2" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">Call Retention Success</th>
          </tr>
          <tr>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">DUT Avg.</th>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">REF Avg.</th>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">DUT Avg.</th>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">REF Avg.</th>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">DUT Avg.</th>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">REF Avg.</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {Object.entries(callPerformanceData).map(([testCase, values]) => (
            <tr key={testCase} className="bg-yellow-50">
              <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center">{testCase}</td>
              <td className="border border-gray-300 text-center">{values.DUT.mean_setup_time.toFixed(2)}</td>
              <td className="border border-gray-300 text-center">{values.REF.mean_setup_time.toFixed(2)}</td>
              <td className="border border-gray-300 text-center">{calculatePercentage(values.DUT.total_initiation_successes, values.DUT.total_attempts)}</td>
              <td className="border border-gray-300 text-center">{calculatePercentage(values.REF.total_initiation_successes, values.REF.total_attempts)}</td>
              <td className="border border-gray-300 text-center">{calculatePercentage(values.DUT.total_attempts - values.DUT.total_retention_failures, values.DUT.total_attempts)}</td>
              <td className="border border-gray-300 text-center">{calculatePercentage(values.REF.total_attempts - values.REF.total_retention_failures, values.REF.total_attempts)}</td>
              <td className="border border-gray-300 text-center">5G Auto VoNR</td>
              <td className="border border-gray-300 text-center">PASS</td>
              <td className="border border-gray-300 text-center"></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CallPerformanceSummaryTable;
