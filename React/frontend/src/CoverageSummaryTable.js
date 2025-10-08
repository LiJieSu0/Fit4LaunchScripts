import React from 'react';

const CoverageSummaryTable = () => {
  return (
    <div className="coverage-summary-table-container mb-8">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Coverage Performance Summary</h2>
      <table className="min-w-full divide-y divide-gray-200 border border-gray-300">
        <thead className="bg-gray-600 text-white">
          <tr>
            <th rowSpan="3" className="px-2 py-1 text-left text-xs font-medium uppercase tracking-wider border border-gray-300">Test Cases</th>
            <th colSpan="8" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">KPI for Coverage Performance Mobility</th>
            <th rowSpan="3" className="px-2 py-1 text-left text-xs font-medium uppercase tracking-wider border border-gray-300">Network Tech.</th>
            <th rowSpan="3" className="px-2 py-1 text-left text-xs font-medium uppercase tracking-wider border border-gray-300">Pass/Fail</th>
            <th rowSpan="3" className="px-2 py-1 text-left text-xs font-medium uppercase tracking-wider border border-gray-300">Comments/Links</th>
          </tr>
          <tr>
            <th colSpan="2" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">Last MOS Value Distance (km)</th>
            <th colSpan="2" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">Voice Call Drop Distance (km)</th>
            <th colSpan="2" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">DL TP > 1 Distance (km)</th>
            <th colSpan="2" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">UL TP > 1 Distance (km)</th>
          </tr>
          <tr>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">DUT Avg.</th>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">REF Avg.</th>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">DUT Avg.</th>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">REF Avg.</th>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">DUT Avg.</th>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">REF Avg.</th>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">DUT Avg.</th>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">REF Avg.</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {[
            "5G VoNR Coverage Test n25",
            "5G VoNR Coverage Test n41",
            "5G VoNR Coverage Test n71",
            "5G n41 HPUE Coverage Test Run1",
            "5G n41 HPUE Coverage Test Run2",
            "5G n41 HPUE Coverage Test Run3",
            "5G n41 HPUE Coverage Test Run4",
            "5G n41 HPUE Coverage Test Run5",
          ].map((testCase, index) => (
            <tr key={index} className="bg-yellow-50">
              <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center">{testCase}</td>
              <td className="border border-gray-300 text-center"></td>
              <td className="border border-gray-300 text-center"></td>
              <td className="border border-gray-300 text-center"></td>
              <td className="border border-gray-300 text-center"></td>
              <td className="border border-gray-300 text-center"></td>
              <td className="border border-gray-300 text-center"></td>
              <td className="border border-gray-300 text-center"></td>
              <td className="border border-gray-300 text-center"></td>
              <td className="border border-gray-300 text-center"></td>
              <td className="border border-gray-300 text-center"></td>
              <td className="border border-gray-300 text-center"></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CoverageSummaryTable;
