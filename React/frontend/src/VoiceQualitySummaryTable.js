import React from 'react';

const VoiceQualitySummaryTable = () => {
  return (
    <div className="voice-quality-summary-table-container mb-8">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Voice Quality Summary</h2>
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
          {[
            "5G Auto VoNR Enabled AMR NB VQ",
            "5G Auto VoNR Enabled AMR WB VQ"
          ].map((testCase, index) => (
            <tr key={index} className="bg-yellow-50">
              <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center">{testCase}</td>
              <td className="border border-gray-300 text-center" style={{ backgroundColor: 'var(--performance-excellent)' }}>4.32</td>
              <td className="border border-gray-300 text-center"style={{ backgroundColor: 'var(--performance-excellent)' }}>4.29</td>
              <td className="border border-gray-300 text-center"style={{ backgroundColor: 'var(--performance-excellent)' }}>0.6%</td>
              <td className="border border-gray-300 text-center"style={{ backgroundColor: 'var(--performance-excellent)' }}>1.0%</td>
              <td className="border border-gray-300 text-center"style={{ backgroundColor: 'var(--performance-excellent)' }}>0.0%</td>
              <td className="border border-gray-300 text-center"style={{ backgroundColor: 'var(--performance-excellent)' }}>0.4%</td>
              <td className="border border-gray-300 text-center"></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default VoiceQualitySummaryTable;
