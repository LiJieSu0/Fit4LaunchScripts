import React from 'react';
import data_analysis_results from './data_analysis_results.json';

const VQAudioEnableTable = () => {
  const getCellColorStyle = (row, key) => {
    if (row.cellColors && row.cellColors[key]) {
      return { backgroundColor: row.cellColors[key] };
    }
    return {};
  };

  const audioEnableData = data_analysis_results["Voice Quality"]["5G Auto VoNR Enabled Audio Delay"];

  const formatNumber = (value) => value.toFixed(2);

  const tableData = [
    {
      metric: "Average (ms)",
      downlinkDUT1: formatNumber(Object.values(audioEnableData["DUT1"]).find(item => item.hasOwnProperty('mean') && Object.keys(audioEnableData["DUT1"])[0].includes('Mobile'))?.mean || 0),
      downlinkDUT2: formatNumber(Object.values(audioEnableData["DUT2"]).find(item => item.hasOwnProperty('mean') && Object.keys(audioEnableData["DUT2"])[0].includes('Mobile'))?.mean || 0),
      downlinkREF1: formatNumber(Object.values(audioEnableData["REF1"]).find(item => item.hasOwnProperty('mean') && Object.keys(audioEnableData["REF1"])[0].includes('Mobile'))?.mean || 0),
      downlinkREF2: formatNumber(Object.values(audioEnableData["REF2"]).find(item => item.hasOwnProperty('mean') && Object.keys(audioEnableData["REF2"])[0].includes('Mobile'))?.mean || 0),
      cellColors: {}
    },
    {
      metric: "Average of 2 Devices (ms)",
      downlinkDUT1: formatNumber((
        (Object.values(audioEnableData["DUT1"]).find(item => item.hasOwnProperty('mean') && Object.keys(audioEnableData["DUT1"])[0].includes('Mobile'))?.mean || 0) +
        (Object.values(audioEnableData["DUT2"]).find(item => item.hasOwnProperty('mean') && Object.keys(audioEnableData["DUT2"])[0].includes('Mobile'))?.mean || 0)
      ) / 2),
      downlinkDUT2: "",
      downlinkREF1: formatNumber((
        (Object.values(audioEnableData["REF1"]).find(item => item.hasOwnProperty('mean') && Object.keys(audioEnableData["REF1"])[0].includes('Mobile'))?.mean || 0) +
        (Object.values(audioEnableData["REF2"]).find(item => item.hasOwnProperty('mean') && Object.keys(audioEnableData["REF2"])[0].includes('Mobile'))?.mean || 0)
      ) / 2),
      downlinkREF2: "",
      cellColors: {
        downlinkDUT1:"#99FA99",
        downlinkREF1:"#99FA99"
      }
    },
    {
      metric: "Stdev (ms)",
      downlinkDUT1: formatNumber(Object.values(audioEnableData["DUT1"]).find(item => item.hasOwnProperty('std_dev') && Object.keys(audioEnableData["DUT1"])[0].includes('Mobile'))?.std_dev || 0),
      downlinkDUT2: formatNumber(Object.values(audioEnableData["DUT2"]).find(item => item.hasOwnProperty('std_dev') && Object.keys(audioEnableData["DUT2"])[0].includes('Mobile'))?.std_dev || 0),
      downlinkREF1: formatNumber(Object.values(audioEnableData["REF1"]).find(item => item.hasOwnProperty('std_dev') && Object.keys(audioEnableData["REF1"])[0].includes('Mobile'))?.std_dev || 0),
      downlinkREF2: formatNumber(Object.values(audioEnableData["REF2"]).find(item => item.hasOwnProperty('std_dev') && Object.keys(audioEnableData["REF2"])[0].includes('Mobile'))?.std_dev || 0),
      cellColors: {}
    },
    {
      metric: "Maximum (ms)",
      downlinkDUT1: formatNumber(Object.values(audioEnableData["DUT1"]).find(item => item.hasOwnProperty('max') && Object.keys(audioEnableData["DUT1"])[0].includes('Mobile'))?.max || 0),
      downlinkDUT2: formatNumber(Object.values(audioEnableData["DUT2"]).find(item => item.hasOwnProperty('max') && Object.keys(audioEnableData["DUT2"])[0].includes('Mobile'))?.max || 0),
      downlinkREF1: formatNumber(Object.values(audioEnableData["REF1"]).find(item => item.hasOwnProperty('max') && Object.keys(audioEnableData["REF1"])[0].includes('Mobile'))?.max || 0),
      downlinkREF2: formatNumber(Object.values(audioEnableData["REF2"]).find(item => item.hasOwnProperty('max') && Object.keys(audioEnableData["REF2"])[0].includes('Mobile'))?.max || 0),
      cellColors: {}
    },
    {
      metric: "Minimum (ms)",
      downlinkDUT1: formatNumber(Object.values(audioEnableData["DUT1"]).find(item => item.hasOwnProperty('min') && Object.keys(audioEnableData["DUT1"])[0].includes('Mobile'))?.min || 0),
      downlinkDUT2: formatNumber(Object.values(audioEnableData["DUT2"]).find(item => item.hasOwnProperty('min') && Object.keys(audioEnableData["DUT2"])[0].includes('Mobile'))?.min || 0),
      downlinkREF1: formatNumber(Object.values(audioEnableData["REF1"]).find(item => item.hasOwnProperty('min') && Object.keys(audioEnableData["REF1"])[0].includes('Mobile'))?.min || 0),
      downlinkREF2: formatNumber(Object.values(audioEnableData["REF2"]).find(item => item.hasOwnProperty('min') && Object.keys(audioEnableData["REF2"])[0].includes('Mobile'))?.min || 0),
      cellColors: {}
    },
    {
      metric: "Count",
      downlinkDUT1: (Object.values(audioEnableData["DUT1"]).find(item => item.hasOwnProperty('occurrences') && Object.keys(audioEnableData["DUT1"])[0].includes('Mobile'))?.occurrences || 0).toString(),
      downlinkDUT2: (Object.values(audioEnableData["DUT2"]).find(item => item.hasOwnProperty('occurrences') && Object.keys(audioEnableData["DUT2"])[0].includes('Mobile'))?.occurrences || 0).toString(),
      downlinkREF1: (Object.values(audioEnableData["REF1"]).find(item => item.hasOwnProperty('occurrences') && Object.keys(audioEnableData["REF1"])[0].includes('Mobile'))?.occurrences || 0).toString(),
      downlinkREF2: (Object.values(audioEnableData["REF2"]).find(item => item.hasOwnProperty('occurrences') && Object.keys(audioEnableData["REF2"])[0].includes('Mobile'))?.occurrences || 0).toString(),
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
              <th colSpan="4" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">KPI For Audio delay</th>
            </tr>
            <tr>
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
                {row.metric === "Average of 2 Devices (ms)" ? (
                  <>
                    <td colSpan="2" className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'downlinkDUT1')}>{row.downlinkDUT1}</td>
                    <td colSpan="2" className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'downlinkREF1')}>{row.downlinkREF1}</td>
                  </>
                ) : (
                  <>
                    <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'downlinkDUT1')}>{row.downlinkDUT1}</td>
                    <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'downlinkDUT2')}>{row.downlinkDUT2}</td>
                    <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'downlinkREF1')}>{row.downlinkREF1}</td>
                    <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center" style={getCellColorStyle(row, 'downlinkREF2')}>{row.downlinkREF2}</td>
                  </>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default VQAudioEnableTable;
