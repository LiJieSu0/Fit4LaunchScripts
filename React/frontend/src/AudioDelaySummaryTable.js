import React from 'react';

const AudioDelaySummaryTable = () => {
  const audioDelayData = [
    {
      testCase: "5G Auto VoNR Disabled Audio Delay",
      dutAvg: 329.85,
      refAvg: 325.76,
      comments: "",
    },
    {
      testCase: "5G Auto VoNR Enabled Audio Delay",
      dutAvg: 305.39,
      refAvg: 333.43,
      comments: "",
    },
  ];

  const getCellColorStyle = (dutAvg, refAvg) => {
    if (refAvg === 0) return { backgroundColor: "var(--performance-unknown)" }; // Avoid division by zero

    const percentage = (dutAvg / refAvg) * 100;

    if (percentage < 90) {
      return { backgroundColor: "var(--performance-excellent)" };
    } else if (percentage >= 90 && percentage <= 110) {
      return { backgroundColor: "var(--performance-pass)" };
    } else if (percentage > 110 && percentage <= 120) {
      return { backgroundColor: "var(--performance-marginal-fail)" };
    } else {
      return { backgroundColor: "var(--performance-fail)" };
    }
  };

  return (
    <div className="audio-delay-summary-table-container mb-8">
      <table className="min-w-full divide-y divide-gray-200 border border-gray-300">
        <thead className="bg-gray-600 text-white">
          <tr>
            <th rowSpan="3" className="px-2 py-1 text-left text-xs font-medium uppercase tracking-wider border border-gray-300">Test Cases</th>
            <th colSpan="2" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">KPI for Voice Quality Performance Mobility</th>
            <th rowSpan="3" className="px-2 py-1 text-left text-xs font-medium uppercase tracking-wider border border-gray-300">Comments/Links</th>
          </tr>
          <tr>
            <th colSpan="2" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">Audio Delay (ms)</th>
          </tr>
          <tr>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">DUT Avg.</th>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">REF Avg.</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {audioDelayData.map((row, index) => (
            <tr key={index} className="bg-yellow-50">
              <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center">{row.testCase}</td>
              <td className="border border-gray-300 text-center" style={getCellColorStyle(row.dutAvg, row.refAvg)}>{row.dutAvg.toFixed(2)}</td>
              <td className="border border-gray-300 text-center" style={getCellColorStyle(row.dutAvg, row.refAvg)}>{row.refAvg.toFixed(2)}</td>
              <td className="border border-gray-300 text-center">{row.comments}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AudioDelaySummaryTable;
