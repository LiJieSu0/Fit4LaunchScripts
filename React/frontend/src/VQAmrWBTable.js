import React from 'react';
import data_analysis_results from './data_analysis_results.json';

const VQAmrWBTable = () => {
  const getCellColorStyle = (row, key) => {
    if (row.cellColors && row.cellColors[key]) {
      return { backgroundColor: row.cellColors[key] };
    }
    return {};
  };

  const amrWbData = data_analysis_results["Voice Quality"]["5G Auto VoNR Enabled AMR WB VQ"];

  const formatPercentage = (value) => `${(value ).toFixed(1)}%`;
  const formatNumber = (value) => value.toFixed(2);

  const tableData = [
    {
      metric: "MOS Average",
      downlinkReference: formatNumber(amrWbData["Base"]["vonr enable amr wb REF base"]["MOS Average"]),
      downlinkWingtech1: formatNumber(amrWbData["Base"]["vonr enable amr wb DUT1 base"]["MOS Average"]),
      downlinkWingtech2: formatNumber(amrWbData["Base"]["vonr enable amr wb DUT2 base"]["MOS Average"]),
      uplinkReference: formatNumber(amrWbData["Mobile"]["vonr enable amr wb REF mobile"]["MOS Average"]),
      uplinkWingtech1: formatNumber(amrWbData["Mobile"]["vonr enable amr wb DUT1 mobile"]["MOS Average"]),
      uplinkWingtech2: formatNumber(amrWbData["Mobile"]["vonr enable amr wb DUT2 mobile"]["MOS Average"]),
      cellColors: {}
    },
    {
      metric: "MOS Stdev",
      downlinkReference: formatNumber(amrWbData["Base"]["vonr enable amr wb REF base"]["MOS Stdev"]),
      downlinkWingtech1: formatNumber(amrWbData["Base"]["vonr enable amr wb DUT1 base"]["MOS Stdev"]),
      downlinkWingtech2: formatNumber(amrWbData["Base"]["vonr enable amr wb DUT2 base"]["MOS Stdev"]),
      uplinkReference: formatNumber(amrWbData["Mobile"]["vonr enable amr wb REF mobile"]["MOS Stdev"]),
      uplinkWingtech1: formatNumber(amrWbData["Mobile"]["vonr enable amr wb DUT1 mobile"]["MOS Stdev"]),
      uplinkWingtech2: formatNumber(amrWbData["Mobile"]["vonr enable amr wb DUT2 mobile"]["MOS Stdev"]),
      cellColors: {}
    },
    {
      metric: "Maximum MOS",
      downlinkReference: formatNumber(amrWbData["Base"]["vonr enable amr wb REF base"]["Maximum MOS"]),
      downlinkWingtech1: formatNumber(amrWbData["Base"]["vonr enable amr wb DUT1 base"]["Maximum MOS"]),
      downlinkWingtech2: formatNumber(amrWbData["Base"]["vonr enable amr wb DUT2 base"]["Maximum MOS"]),
      uplinkReference: formatNumber(amrWbData["Mobile"]["vonr enable amr wb REF mobile"]["Maximum MOS"]),
      uplinkWingtech1: formatNumber(amrWbData["Mobile"]["vonr enable amr wb DUT1 mobile"]["Maximum MOS"]),
      uplinkWingtech2: formatNumber(amrWbData["Mobile"]["vonr enable amr wb DUT2 mobile"]["Maximum MOS"]),
      cellColors: {}
    },
    {
      metric: "Count",
      downlinkReference: amrWbData["Base"]["vonr enable amr wb REF base"]["Counts"].toString(),
      downlinkWingtech1: amrWbData["Base"]["vonr enable amr wb DUT1 base"]["Counts"].toString(),
      downlinkWingtech2: amrWbData["Base"]["vonr enable amr wb DUT2 base"]["Counts"].toString(),
      uplinkReference: amrWbData["Mobile"]["vonr enable amr wb REF mobile"]["Counts"].toString(),
      uplinkWingtech1: amrWbData["Mobile"]["vonr enable amr wb DUT1 mobile"]["Counts"].toString(),
      uplinkWingtech2: amrWbData["Mobile"]["vonr enable amr wb DUT2 mobile"]["Counts"].toString(),
      cellColors: {}
    },
    {
      metric: "% MOS < 3.0",
      downlinkReference: formatPercentage(amrWbData["Base"]["vonr enable amr wb REF base"]["% MOS < 3.0"]),
      downlinkWingtech1: formatPercentage(amrWbData["Base"]["vonr enable amr wb DUT1 base"]["% MOS < 3.0"]),
      downlinkWingtech2: formatPercentage(amrWbData["Base"]["vonr enable amr wb DUT2 base"]["% MOS < 3.0"]),
      uplinkReference: formatPercentage(amrWbData["Mobile"]["vonr enable amr wb REF mobile"]["% MOS < 3.0"]),
      uplinkWingtech1: formatPercentage(amrWbData["Mobile"]["vonr enable amr wb DUT1 mobile"]["% MOS < 3.0"]),
      uplinkWingtech2: formatPercentage(amrWbData["Mobile"]["vonr enable amr wb DUT2 mobile"]["% MOS < 3.0"]),
      cellColors: {}
    },
    {
      metric: "% MOS < 2.0",
      downlinkReference: formatPercentage(amrWbData["Base"]["vonr enable amr wb REF base"]["% MOS < 2.0"]),
      downlinkWingtech1: formatPercentage(amrWbData["Base"]["vonr enable amr wb DUT1 base"]["% MOS < 2.0"]),
      downlinkWingtech2: formatPercentage(amrWbData["Base"]["vonr enable amr wb DUT2 base"]["% MOS < 2.0"]),
      uplinkReference: formatPercentage(amrWbData["Mobile"]["vonr enable amr wb REF mobile"]["% MOS < 2.0"]),
      uplinkWingtech1: formatPercentage(amrWbData["Mobile"]["vonr enable amr wb DUT1 mobile"]["% MOS < 2.0"]),
      uplinkWingtech2: formatPercentage(amrWbData["Mobile"]["vonr enable amr wb DUT2 mobile"]["% MOS < 2.0"]),
      cellColors: {}
    },
  ];

  return (
    <div className="audio-delay-summary-table-container mb-8">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200 border border-gray-300">
          <thead className="bg-gray-600 text-white">
            <tr>
              <th rowSpan="2" className="px-2 py-1 text-left text-xs font-medium uppercase tracking-wider border border-gray-300"></th>
              <th colSpan="3" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">Mobile</th>
              <th colSpan="3" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">Base</th>
            </tr>
            <tr>
              <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">REF</th>
              <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">DUT 1</th>
              <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">DUT 2</th>
              <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">REF</th>
              <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">DUT 1</th>
              <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">DUT 2</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {tableData.map((row, index) => (
              <tr key={index} className="bg-yellow-50">
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-left" style={getCellColorStyle(row, 'metric')}>{row.metric}</td>
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'downlinkReference')}>{row.downlinkReference}</td>
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'downlinkWingtech1')}>{row.downlinkWingtech1}</td>
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'downlinkWingtech2')}>{row.downlinkWingtech2}</td>
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'uplinkReference')}>{row.uplinkReference}</td>
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'uplinkWingtech1')}>{row.uplinkWingtech1}</td>
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'uplinkWingtech2')}>{row.uplinkWingtech2}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default VQAmrWBTable;
