import React from 'react';

const VQEVSsummaryTable = () => {
  // This data would typically come from props or a data source
  const data = [
    {
      testCase: "5G Auto VoNR Disabled EVS WB VQ",
      mosAverage: "4.0",
      mosRefAverage: "4.1",
      mosLessThan3_4_DUT: "2.0%",
      mosLessThan3_4_REF: "1.5%",
      mosLessThan3_0_DUT: "0.5%",
      mosLessThan3_0_REF: "0.2%",
      comments: ""
    },
    {
      testCase: "5G Auto VoNR Enabled EVS WB VQ",
      mosAverage: "4.2",
      mosRefAverage: "4.3",
      mosLessThan3_4_DUT: "1.0%",
      mosLessThan3_4_REF: "0.8%",
      mosLessThan3_0_DUT: "0.3%",
      mosLessThan3_0_REF: "0.1%",
      comments: ""
    },
    // Add more data as needed
  ];

  return (
    <div className="audio-delay-summary-table-container mb-8">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200 border border-gray-300">
          <thead className="bg-gray-600 text-white">
            <tr>
              <th rowSpan="2" className="px-2 py-1 text-left text-xs font-medium uppercase tracking-wider border border-gray-300">TEST CASES</th>
              <th colSpan="2" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">MOS Average</th>
              <th colSpan="2" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">% MOS &lt; 3.4</th>
              <th colSpan="2" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">% MOS &lt; 3.0</th>
              <th rowSpan="2" className="px-2 py-1 text-left text-xs font-medium uppercase tracking-wider border border-gray-300">COMMENTS/LINKS</th>
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
            {data.map((row, index) => (
              <tr key={index} className="bg-yellow-50">
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center">{row.testCase}</td>
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center">{row.mosAverage}</td>
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center">{row.mosRefAverage}</td>
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center">{row.mosLessThan3_4_DUT}</td>
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center">{row.mosLessThan3_4_REF}</td>
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center">{row.mosLessThan3_0_DUT}</td>
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center">{row.mosLessThan3_0_REF}</td>
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center">{row.comments}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default VQEVSsummaryTable;
