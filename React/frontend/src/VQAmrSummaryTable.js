import React from 'react';

const VQAMRSummaryTable = () => {
  // This data would typically come from props or a data source
  const getCellColorStyle = (row, key) => {
    if (row.cellColors && row.cellColors[key]) {
      return { backgroundColor: row.cellColors[key] };
    }
    return {};
  };

  const data = [
    {
      testCase: "5G Auto VoNR Enabled AMR NB VQ",
      mosAverage: "3.5",
      mosRefAverage: "3.6",
      mosLessThan3_4_DUT: "5.0%",
      mosLessThan3_4_REF: "4.5%",
      mosLessThan3_0_DUT: "2.0%",
      mosLessThan3_0_REF: "1.5%",
      comments: "",
      cellColors: {
        mosAverage: "lightsalmon",
        mosLessThan3_4_DUT: "lightcoral"
      }
    },
    {
      testCase: "5G Auto VoNR Enabled AMR WB VQ",
      mosAverage: "3.8",
      mosRefAverage: "3.9",
      mosLessThan3_4_DUT: "3.0%",
      mosLessThan3_4_REF: "2.5%",
      mosLessThan3_0_DUT: "1.0%",
      mosLessThan3_0_REF: "0.5%",
      comments: "",
      cellColors: {
        mosAverage: "lightgreen",
        mosLessThan3_4_DUT: "lightgreen"
      }
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
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'testCase')}>{row.testCase}</td>
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'mosAverage')}>{row.mosAverage}</td>
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'mosRefAverage')}>{row.mosRefAverage}</td>
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'mosLessThan3_4_DUT')}>{row.mosLessThan3_4_DUT}</td>
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'mosLessThan3_4_REF')}>{row.mosLessThan3_4_REF}</td>
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'mosLessThan3_0_DUT')}>{row.mosLessThan3_0_DUT}</td>
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'mosLessThan3_0_REF')}>{row.mosLessThan3_0_REF}</td>
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'comments')}>{row.comments}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default VQAMRSummaryTable;
