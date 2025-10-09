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
      mosAverage: "4.32",
      mosRefAverage: "4.29",
      mosLessThan3_4_DUT: "0.6%",
      mosLessThan3_4_REF: "1.0%",
      mosLessThan3_0_DUT: "0.0%",
      mosLessThan3_0_REF: "0.4%",
      comments: "",
      cellColors: {
        mosAverage: "#FF00FF",
        mosRefAverage:"#FF00FF",
        mosLessThan3_4_DUT: "#FF00FF",
        mosLessThan3_4_REF: "#FF00FF",
        mosLessThan3_0_DUT: "#FF00FF",
        mosLessThan3_0_REF: "#FF00FF",
      }
    },
    {
      testCase: "5G Auto VoNR Enabled AMR WB VQ",
      mosAverage: "3.52",
      mosRefAverage: "3.36",
      mosLessThan3_4_DUT: "4.4%",
      mosLessThan3_4_REF: "14.7%",
      mosLessThan3_0_DUT: "0.2%",
      mosLessThan3_0_REF: "2.4%",
      comments: "",
      cellColors: {
        mosAverage: "#FF00FF",
        mosRefAverage:"#FF00FF",
        mosLessThan3_4_DUT: "#FF00FF",
        mosLessThan3_4_REF: "#FF00FF",
        mosLessThan3_0_DUT: "#FF00FF",
        mosLessThan3_0_REF: "#FF00FF",
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
              <th colSpan="2" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">% MOS &lt; 3.0</th>
              <th colSpan="2" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">% MOS &lt; 2.0</th>
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
                <td className="px-2 py-4 text-sm text-black-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'testCase')}>{row.testCase}</td>
                <td className="px-2 py-4 text-sm text-black-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'mosAverage')}>{row.mosAverage}</td>
                <td className="px-2 py-4 text-sm text-black-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'mosRefAverage')}>{row.mosRefAverage}</td>
                <td className="px-2 py-4 text-sm text-black-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'mosLessThan3_4_DUT')}>{row.mosLessThan3_4_DUT}</td>
                <td className="px-2 py-4 text-sm text-black-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'mosLessThan3_4_REF')}>{row.mosLessThan3_4_REF}</td>
                <td className="px-2 py-4 text-sm text-black-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'mosLessThan3_0_DUT')}>{row.mosLessThan3_0_DUT}</td>
                <td className="px-2 py-4 text-sm text-black-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'mosLessThan3_0_REF')}>{row.mosLessThan3_0_REF}</td>
                <td className="px-2 py-4 text-sm text-black-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'comments')}>{row.comments}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default VQAMRSummaryTable;
