import React from 'react';

const VQAmrSummaryTable = ({ data, testName }) => {
  if (!data) {
    return <div>No data available for {testName}</div>;
  }

  const devices = Object.keys(data);
  const metricMap = {
    "MOS Average": "mean",
    "MOS Stdev": "std_dev",
    "Maximum MOS": "max",
    "Count": "count",
    "% MOS < 3.0": "percent_less_than_3",
    "% MOS < 2.0": "percent_less_than_2",
  };

  const metricDisplayNames = Object.keys(metricMap);

  return (
    <div className="voice-quality-nb-table-container mb-8">
      <h3 className="text-xl font-bold mb-4 text-gray-800">{testName} - NB Voice Quality</h3>
      <table className="min-w-full divide-y divide-gray-200 border border-gray-300">
        <thead className="bg-gray-700 text-white">
          <tr>
            <th rowSpan="2" className="px-2 py-1 text-left text-xs font-medium uppercase tracking-wider border border-gray-300"></th>
            <th colSpan={devices.length} className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">Downlink</th>
            <th colSpan={devices.length} className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">Uplink</th>
          </tr>
          <tr>
            {devices.map(device => (
              <th key={`dl-${device}`} className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">{device}</th>
            ))}
            {devices.map(device => (
              <th key={`ul-${device}`} className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">{device}</th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {metricDisplayNames.map((metricName, index) => {
            const originalStatKey = metricMap[metricName];

            return (
              <tr key={metricName} className="bg-yellow-50">
                <td className="px-2 py-1 text-sm text-gray-800 border border-gray-300 text-left">{metricName}</td>
                {/* Downlink Data */}
                {devices.map(device => {
                  const isPerformanceExcellent = ["MOS Average", "% MOS < 3.0", "% MOS < 2.0"].includes(metricName);
                  const cellClassName = `border border-gray-300 text-center text-sm text-gray-700 ${isPerformanceExcellent ? 'bg-[var(--performance-excellent)]' : ''}`;
                  return (
                    <td key={`dl-${device}-${metricName}-data`} className={cellClassName}>
                      {data[device]?.dl_mos_stats?.[originalStatKey] !== undefined
                        ? (originalStatKey.startsWith('percent')
                          ? `${(data[device].dl_mos_stats[originalStatKey]).toFixed(1)}%`
                          : (originalStatKey === 'count'
                            ? parseInt(data[device].dl_mos_stats[originalStatKey]).toString()
                            : data[device].dl_mos_stats[originalStatKey].toFixed(2)))
                        : 'N/A'}
                    </td>
                  );
                })}
                {/* Uplink Data */}
                {devices.map(device => {
                  const isPerformanceExcellent = ["MOS Average", "% MOS < 3.0", "% MOS < 2.0"].includes(metricName);
                  const cellClassName = `border border-gray-300 text-center text-sm text-gray-700 ${isPerformanceExcellent ? 'bg-[var(--performance-excellent)]' : ''}`;
                  return (
                    <td key={`ul-${device}-${metricName}-data`} className={cellClassName}>
                      {data[device]?.ul_mos_stats?.[originalStatKey] !== undefined
                        ? (originalStatKey.startsWith('percent')
                          ? `${(data[device].ul_mos_stats[originalStatKey]).toFixed(1)}%`
                          : (originalStatKey === 'count'
                            ? parseInt(data[device].ul_mos_stats[originalStatKey]).toString()
                            : data[device].ul_mos_stats[originalStatKey].toFixed(2)))
                        : 'N/A'}
                    </td>
                  );
                })}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default VQAmrSummaryTable;
