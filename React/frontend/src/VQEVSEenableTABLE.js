import React from 'react';
import data_analysis_results from './data_analysis_results.json';

const VQEVSEenableTABLE = () => {
  const getCellColorStyle = (row, key) => {
    if (row.cellColors && row.cellColors[key]) {
      return { backgroundColor: row.cellColors[key] };
    }
    return {};
  };

  const evsEnableData = data_analysis_results["Voice Quality"]["5G Auto VoNR Enabled EVS WB VQ"];

  const formatPercentage = (value) => `${(value).toFixed(1)}%`;
  const formatNumber = (value) => value.toFixed(2);

  const tableData = [
    {
      metric: "MOS Average",
      downlinkDUT1: formatNumber(evsEnableData["Mobile"]["vonr enable evs wb DUT1 mobile"]["MOS Average"]),
      downlinkDUT2: formatNumber(evsEnableData["Mobile"]["vonr enable evs wb DUT2 mobile"]["MOS Average"]),
      downlinkREF1: formatNumber(evsEnableData["Mobile"]["vonr enable evs wb REF1 mobile"]["MOS Average"]),
      downlinkREF2: formatNumber(evsEnableData["Mobile"]["vonr enable evs wb REF2 mobile"]["MOS Average"]),
      uplinkDUT1: formatNumber(evsEnableData["Base"]["vonr enable evs wb DUT1 base"]["MOS Average"]),
      uplinkDUT2: formatNumber(evsEnableData["Base"]["vonr enable evs wb DUT2 base"]["MOS Average"]),
      uplinkREF1: formatNumber(evsEnableData["Base"]["vonr enable evs wb REF1 base"]["MOS Average"]),
      uplinkREF2: formatNumber(evsEnableData["Base"]["vonr enable evs wb REF2 base"]["MOS Average"]),
      cellColors: {}
    },
    {
      metric: "MOS Stdev",
      downlinkDUT1: formatNumber(evsEnableData["Mobile"]["vonr enable evs wb DUT1 mobile"]["MOS Stdev"]),
      downlinkDUT2: formatNumber(evsEnableData["Mobile"]["vonr enable evs wb DUT2 mobile"]["MOS Stdev"]),
      downlinkREF1: formatNumber(evsEnableData["Mobile"]["vonr enable evs wb REF1 mobile"]["MOS Stdev"]),
      downlinkREF2: formatNumber(evsEnableData["Mobile"]["vonr enable evs wb REF2 mobile"]["MOS Stdev"]),
      uplinkDUT1: formatNumber(evsEnableData["Base"]["vonr enable evs wb DUT1 base"]["MOS Stdev"]),
      uplinkDUT2: formatNumber(evsEnableData["Base"]["vonr enable evs wb DUT2 base"]["MOS Stdev"]),
      uplinkREF1: formatNumber(evsEnableData["Base"]["vonr enable evs wb REF1 base"]["MOS Stdev"]),
      uplinkREF2: formatNumber(evsEnableData["Base"]["vonr enable evs wb REF2 base"]["MOS Stdev"]),
      cellColors: {}
    },
    {
      metric: "Maximum MOS",
      downlinkDUT1: formatNumber(evsEnableData["Mobile"]["vonr enable evs wb DUT1 mobile"]["Maximum MOS"]),
      downlinkDUT2: formatNumber(evsEnableData["Mobile"]["vonr enable evs wb DUT2 mobile"]["Maximum MOS"]),
      downlinkREF1: formatNumber(evsEnableData["Mobile"]["vonr enable evs wb REF1 mobile"]["Maximum MOS"]),
      downlinkREF2: formatNumber(evsEnableData["Mobile"]["vonr enable evs wb REF2 mobile"]["Maximum MOS"]),
      uplinkDUT1: formatNumber(evsEnableData["Base"]["vonr enable evs wb DUT1 base"]["Maximum MOS"]),
      uplinkDUT2: formatNumber(evsEnableData["Base"]["vonr enable evs wb DUT2 base"]["Maximum MOS"]),
      uplinkREF1: formatNumber(evsEnableData["Base"]["vonr enable evs wb REF1 base"]["Maximum MOS"]),
      uplinkREF2: formatNumber(evsEnableData["Base"]["vonr enable evs wb REF2 base"]["Maximum MOS"]),
      cellColors: {}
    },
    {
      metric: "Count",
      downlinkDUT1: evsEnableData["Mobile"]["vonr enable evs wb DUT1 mobile"]["Counts"].toString(),
      downlinkDUT2: evsEnableData["Mobile"]["vonr enable evs wb DUT2 mobile"]["Counts"].toString(),
      downlinkREF1: evsEnableData["Mobile"]["vonr enable evs wb REF1 mobile"]["Counts"].toString(),
      downlinkREF2: evsEnableData["Mobile"]["vonr enable evs wb REF2 mobile"]["Counts"].toString(),
      uplinkDUT1: evsEnableData["Base"]["vonr enable evs wb DUT1 base"]["Counts"].toString(),
      uplinkDUT2: evsEnableData["Base"]["vonr enable evs wb DUT2 base"]["Counts"].toString(),
      uplinkREF1: evsEnableData["Base"]["vonr enable evs wb REF1 base"]["Counts"].toString(),
      uplinkREF2: evsEnableData["Base"]["vonr enable evs wb REF2 base"]["Counts"].toString(),
      cellColors: {}
    },
    {
      metric: "% MOS < 3.0",
      downlinkDUT1: formatPercentage(evsEnableData["Mobile"]["vonr enable evs wb DUT1 mobile"]["% MOS < 3.0"]),
      downlinkDUT2: formatPercentage(evsEnableData["Mobile"]["vonr enable evs wb DUT2 mobile"]["% MOS < 3.0"]),
      downlinkREF1: formatPercentage(evsEnableData["Mobile"]["vonr enable evs wb REF1 mobile"]["% MOS < 3.0"]),
      downlinkREF2: formatPercentage(evsEnableData["Mobile"]["vonr enable evs wb REF2 mobile"]["% MOS < 3.0"]),
      uplinkDUT1: formatPercentage(evsEnableData["Base"]["vonr enable evs wb DUT1 base"]["% MOS < 3.0"]),
      uplinkDUT2: formatPercentage(evsEnableData["Base"]["vonr enable evs wb DUT2 base"]["% MOS < 3.0"]),
      uplinkREF1: formatPercentage(evsEnableData["Base"]["vonr enable evs wb REF1 base"]["% MOS < 3.0"]),
      uplinkREF2: formatPercentage(evsEnableData["Base"]["vonr enable evs wb REF2 base"]["% MOS < 3.0"]),
      cellColors: {}
    },
    {
      metric: "% MOS < 2.0",
      downlinkDUT1: formatPercentage(evsEnableData["Mobile"]["vonr enable evs wb DUT1 mobile"]["% MOS < 2.0"]),
      downlinkDUT2: formatPercentage(evsEnableData["Mobile"]["vonr enable evs wb DUT2 mobile"]["% MOS < 2.0"]),
      downlinkREF1: formatPercentage(evsEnableData["Mobile"]["vonr enable evs wb REF1 mobile"]["% MOS < 2.0"]),
      downlinkREF2: formatPercentage(evsEnableData["Mobile"]["vonr enable evs wb REF2 mobile"]["% MOS < 2.0"]),
      uplinkDUT1: formatPercentage(evsEnableData["Base"]["vonr enable evs wb DUT1 base"]["% MOS < 2.0"]),
      uplinkDUT2: formatPercentage(evsEnableData["Base"]["vonr enable evs wb DUT2 base"]["% MOS < 2.0"]),
      uplinkREF1: formatPercentage(evsEnableData["Base"]["vonr enable evs wb REF1 base"]["% MOS < 2.0"]),
      uplinkREF2: formatPercentage(evsEnableData["Base"]["vonr enable evs wb REF2 base"]["% MOS < 2.0"]),
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
              <th colSpan="4" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">Mobile</th>
              <th colSpan="4" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">Base</th>
            </tr>
            <tr>
              <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">DUT 1</th>
              <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">DUT 2</th>
              <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">REF 1</th>
              <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">REF 2</th>
              <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">DUT 1</th>
              <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">DUT 2</th>
              <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">REF 1</th>
              <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">REF 2</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {tableData.map((row, index) => (
              <tr key={index} className="bg-yellow-50">
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-left" style={getCellColorStyle(row, 'metric')}>{row.metric}</td>
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'downlinkDUT1')}>{row.downlinkDUT1}</td>
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'downlinkDUT2')}>{row.downlinkDUT2}</td>
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'downlinkREF1')}>{row.downlinkREF1}</td>
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'downlinkREF2')}>{row.downlinkREF2}</td>
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'uplinkDUT1')}>{row.uplinkDUT1}</td>
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'uplinkDUT2')}>{row.uplinkDUT2}</td>
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'uplinkREF1')}>{row.uplinkREF1}</td>
                <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'uplinkREF2')}>{row.uplinkREF2}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default VQEVSEenableTABLE;
