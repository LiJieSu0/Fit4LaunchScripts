import React from 'react';
import data_analysis_results from './data_analysis_results.json';

const VQAmrNBTable = () => {
  const getCellColorStyle = (row, key) => {
    if (row.cellColors && row.cellColors[key]) {
      return { backgroundColor: row.cellColors[key] };
    }
    return {};
  };

  const amrNbData = data_analysis_results["Voice Quality"]["5G Auto VoNR Enabled AMR NB VQ"];

  const formatPercentage = (value) => `${(value * 100).toFixed(1)}%`;
  const formatNumber = (value) => value.toFixed(2);

  const tableData = [
    {
      metric: "MOS Average",
      downlinkReference: formatNumber(amrNbData["REF"]["dl_mos_stats"]["mean"]),
      downlinkWingtech1: formatNumber(amrNbData["DUT1"]["dl_mos_stats"]["mean"]),
      downlinkWingtech2: formatNumber(amrNbData["DUT2"]["dl_mos_stats"]["mean"]),
      uplinkReference: formatNumber(amrNbData["REF"]["ul_mos_stats"]["mean"]),
      uplinkWingtech1: formatNumber(amrNbData["DUT1"]["ul_mos_stats"]["mean"]),
      uplinkWingtech2: formatNumber(amrNbData["DUT2"]["ul_mos_stats"]["mean"]),
      cellColors: {
        downlinkReference: "#FF00FF",
        downlinkWingtech1: "#FF00FF",
        downlinkWingtech2: "#FF00FF",
      }
    },
    {
      metric: "MOS Stdev",
      downlinkReference: formatNumber(amrNbData["REF"]["dl_mos_stats"]["std_dev"]),
      downlinkWingtech1: formatNumber(amrNbData["DUT1"]["dl_mos_stats"]["std_dev"]),
      downlinkWingtech2: formatNumber(amrNbData["DUT2"]["dl_mos_stats"]["std_dev"]),
      uplinkReference: formatNumber(amrNbData["REF"]["ul_mos_stats"]["std_dev"]),
      uplinkWingtech1: formatNumber(amrNbData["DUT1"]["ul_mos_stats"]["std_dev"]),
      uplinkWingtech2: formatNumber(amrNbData["DUT2"]["ul_mos_stats"]["std_dev"]),
      cellColors: {}
    },
    {
      metric: "Maximum MOS",
      downlinkReference: formatNumber(amrNbData["REF"]["dl_mos_stats"]["max"]),
      downlinkWingtech1: formatNumber(amrNbData["DUT1"]["dl_mos_stats"]["max"]),
      downlinkWingtech2: formatNumber(amrNbData["DUT2"]["dl_mos_stats"]["max"]),
      uplinkReference: formatNumber(amrNbData["REF"]["ul_mos_stats"]["max"]),
      uplinkWingtech1: formatNumber(amrNbData["DUT1"]["ul_mos_stats"]["max"]),
      uplinkWingtech2: formatNumber(amrNbData["DUT2"]["ul_mos_stats"]["max"]),
      cellColors: {}
    },
    {
      metric: "Count",
      downlinkReference: amrNbData["REF"]["dl_mos_stats"]["count"].toString(),
      downlinkWingtech1: amrNbData["DUT1"]["dl_mos_stats"]["count"].toString(),
      downlinkWingtech2: amrNbData["DUT2"]["dl_mos_stats"]["count"].toString(),
      uplinkReference: amrNbData["REF"]["ul_mos_stats"]["count"].toString(),
      uplinkWingtech1: amrNbData["DUT1"]["ul_mos_stats"]["count"].toString(),
      uplinkWingtech2: amrNbData["DUT2"]["ul_mos_stats"]["count"].toString(),
      cellColors: {}
    },
    {
      metric: "% MOS < 3.0",
      downlinkReference: formatPercentage(amrNbData["REF"]["dl_mos_stats"]["percent_less_than_3"] / 100),
      downlinkWingtech1: formatPercentage(amrNbData["DUT1"]["dl_mos_stats"]["percent_less_than_3"] / 100),
      downlinkWingtech2: formatPercentage(amrNbData["DUT2"]["dl_mos_stats"]["percent_less_than_3"] / 100),
      uplinkReference: formatPercentage(amrNbData["REF"]["ul_mos_stats"]["percent_less_than_3"] / 100),
      uplinkWingtech1: formatPercentage(amrNbData["DUT1"]["ul_mos_stats"]["percent_less_than_3"] / 100),
      uplinkWingtech2: formatPercentage(amrNbData["DUT2"]["ul_mos_stats"]["percent_less_than_3"] / 100),
      cellColors: {
        downlinkReference: "#FF00FF",
        downlinkWingtech1: "#FF00FF",
        downlinkWingtech2: "#FF00FF",
      }
    },
    {
      metric: "% MOS < 2.0",
      downlinkReference: formatPercentage(amrNbData["REF"]["dl_mos_stats"]["percent_less_than_2"] / 100),
      downlinkWingtech1: formatPercentage(amrNbData["DUT1"]["dl_mos_stats"]["percent_less_than_2"] / 100),
      downlinkWingtech2: formatPercentage(amrNbData["DUT2"]["dl_mos_stats"]["percent_less_than_2"] / 100),
      uplinkReference: formatPercentage(amrNbData["REF"]["ul_mos_stats"]["percent_less_than_2"] / 100),
      uplinkWingtech1: formatPercentage(amrNbData["DUT1"]["ul_mos_stats"]["percent_less_than_2"] / 100),
      uplinkWingtech2: formatPercentage(amrNbData["DUT2"]["ul_mos_stats"]["percent_less_than_2"] / 100),
      cellColors: {
        downlinkReference: "#FF00FF",
        downlinkWingtech1: "#FF00FF",
        downlinkWingtech2: "#FF00FF",
      }
    },
  ];

  return (
    <div className="audio-delay-summary-table-container mb-8">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200 border border-gray-300">
          <thead className="bg-gray-600 text-white">
            <tr>
              <th rowSpan="2" className="px-2 py-1 text-left text-xs font-medium uppercase tracking-wider border border-gray-300"></th>
              <th colSpan="3" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">Downlink</th>
              <th colSpan="3" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">Uplink</th>
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
                <td className="px-2 py-4 text-sm text-black-500 border border-gray-300 text-left" style={getCellColorStyle(row, 'metric')}>{row.metric}</td>
                <td className="px-2 py-4 text-sm text-black-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'downlinkReference')}>{row.downlinkReference}</td>
                <td className="px-2 py-4 text-sm text-black-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'downlinkWingtech1')}>{row.downlinkWingtech1}</td>
                <td className="px-2 py-4 text-sm text-black-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'downlinkWingtech2')}>{row.downlinkWingtech2}</td>
                <td className="px-2 py-4 text-sm text-black-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'uplinkReference')}>{row.uplinkReference}</td>
                <td className="px-2 py-4 text-sm text-black-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'uplinkWingtech1')}>{row.uplinkWingtech1}</td>
                <td className="px-2 py-4 text-sm text-black-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'uplinkWingtech2')}>{row.uplinkWingtech2}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default VQAmrNBTable;
