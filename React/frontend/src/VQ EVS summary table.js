import React from 'react';

const VQEVSSummaryTable = () => {
  const additionalTestCases = [
    {
      case: "5G Auto VoNR Disabled EVS WB VQ",
      dutAvgMos: "N/A",
      refAvgMos: "N/A",
      dutMosLessThan3: "N/A",
      refMosLessThan3: "N/A",
      dutMosLessThan2: "N/A",
      refMosLessThan2: "N/A",
      comments: ""
    },
    {
      case: "5G Auto VoNR Enabled EVS WB VQ",
      dutAvgMos: "N/A",
      refAvgMos: "N/A",
      dutMosLessThan3: "N/A",
      refMosLessThan3: "N/A",
      dutMosLessThan2: "N/A",
      refMosLessThan2: "N/A",
      comments: ""
    },
  ];

  return (
    <div className="voice-quality-summary-table-container mb-8">
      <table className="min-w-full divide-y divide-gray-200 border border-gray-300">
        <thead className="bg-gray-600 text-white">
          <tr>
            <th rowSpan="3" className="px-2 py-1 text-left text-xs font-medium uppercase tracking-wider border border-gray-300">Test Cases</th>
            <th colSpan="6" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">KPI for Voice Quality Performance Mobility</th>
            <th rowSpan="3" className="px-2 py-1 text-left text-xs font-medium uppercase tracking-wider border border-gray-300">Comments/Links</th>
          </tr>
          <tr>
            <th colSpan="2" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">MOS Average</th>
            <th colSpan="2" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">% MOS &lt; 3.0</th>
            <th colSpan="2" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">% MOS &lt; 2.0</th>
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
          {additionalTestCases.map((row, index) => (
            <tr key={index} className="bg-yellow-50">
              <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center">{row.case}</td>
              <td className="border border-gray-300 text-center" style={{ backgroundColor: 'var(--performance-excellent)' }}>{row.dutAvgMos}</td>
              <td className="border border-gray-300 text-center"style={{ backgroundColor: 'var(--performance-excellent)' }}>{row.refAvgMos}</td>
              <td className="border border-gray-300 text-center"style={{ backgroundColor: 'var(--performance-excellent)' }}>{row.dutMosLessThan3}</td>
              <td className="border border-gray-300 text-center"style={{ backgroundColor: 'var(--performance-excellent)' }}>{row.refMosLessThan3}</td>
              <td className="border border-gray-300 text-center"style={{ backgroundColor: 'var(--performance-excellent)' }}>{row.dutMosLessThan2}</td>
              <td className="border border-gray-300 text-center"style={{ backgroundColor: 'var(--performance-excellent)' }}>{row.refMosLessThan2}</td>
              <td className="border border-gray-300 text-center">{row.comments}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default VQEVSSummaryTable;
