import React from 'react';

const VQAMRSummaryTable = () => {
  // This data would typically come from props or a data source
  const data = [
    {
      testCase: "5G Auto VoNR Enabled AMR NB VQ",
      mosAverage: "3.5",
      mosRefAverage: "3.6",
      mosMin: "2.8",
      mosRefMin: "2.9",
      comments: "5G Auto VoNR"
    },
    {
      testCase: "5G Auto VoNR Enabled AMR WB VQ",
      mosAverage: "3.8",
      mosRefAverage: "3.9",
      mosMin: "3.1",
      mosRefMin: "3.2",
      comments: "5G Auto VoNR"
    },
    // Add more data as needed
  ];

  return (
    <div className="w-full mx-auto">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">VQAMR Summary</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full border-collapse">
          <thead>
            <tr>
              <th rowSpan="3" className="px-2 py-1 text-left text-xs font-medium uppercase tracking-wider border border-gray-300">TEST CASES</th>
              <th colSpan="4" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">KPI FOR VOICE QUALITY PERFORMANCE MOBILITY</th>
              <th rowSpan="3" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">COMMENTS/LINKS</th>
            </tr>
            <tr>
              <th colSpan="4" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">MOS (Mean Opinion Score)</th>
            </tr>
            <tr>
              <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">DUT AVG.</th>
              <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">REF AVG.</th>
              <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">DUT MIN.</th>
              <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">REF MIN.</th>
            </tr>
          </thead>
          <tbody className="text-gray-700 text-sm">
            {data.map((row, index) => (
              <tr key={index} className="bg-yellow-50 border-b border-gray-200">
                <td className="py-3 px-4 text-left whitespace-nowrap border border-gray-300">{row.testCase}</td>
                <td className="py-3 px-4 text-center border border-gray-300">{row.mosAverage}</td>
                <td className="py-3 px-4 text-center border border-gray-300">{row.mosRefAverage}</td>
                <td className="py-3 px-4 text-center border border-gray-300">{row.mosMin}</td>
                <td className="py-3 px-4 text-center border border-gray-300">{row.mosRefMin}</td>
                <td className="py-3 px-4 text-left border border-gray-300">{row.comments}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default VQAMRSummaryTable;
