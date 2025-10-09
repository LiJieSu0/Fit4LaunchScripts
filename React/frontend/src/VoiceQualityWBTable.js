import React from 'react';

const VoiceQualityWBTable = ({ data, testName }) => {
  if (!data) {
    return <div>No data available for {testName}</div>;
  }

  // Transform the data to match the expected structure for WB tables
  const transformedData = {};
  const deviceKeys = ["DUT1", "DUT2", "REF1", "REF2"]; // Order of devices

  deviceKeys.forEach(device => {
    transformedData[device] = {
      dl_mos_stats: {}, // Corresponds to Mobile
      ul_mos_stats: {}  // Corresponds to Base
    };

    // Extract data for Mobile (Downlink)
    const mobileDataKey = Object.keys(data.Mobile || {}).find(key => key.includes(device));
    if (mobileDataKey && data.Mobile[mobileDataKey]) {
      transformedData[device].dl_mos_stats = {
        mean: data.Mobile[mobileDataKey]["MOS Average"],
        std_dev: data.Mobile[mobileDataKey]["MOS Stdev"],
        max: data.Mobile[mobileDataKey]["Maximum MOS"],
        count: data.Mobile[mobileDataKey]["Counts"],
        percent_less_than_3: data.Mobile[mobileDataKey]["% MOS < 3.0"],
        percent_less_than_2: data.Mobile[mobileDataKey]["% MOS < 2.0"],
      };
    }

    // Extract data for Base (Uplink)
    const baseDataKey = Object.keys(data.Base || {}).find(key => key.includes(device));
    if (baseDataKey && data.Base[baseDataKey]) {
      transformedData[device].ul_mos_stats = {
        mean: data.Base[baseDataKey]["MOS Average"],
        std_dev: data.Base[baseDataKey]["MOS Stdev"],
        max: data.Base[baseDataKey]["Maximum MOS"],
        count: data.Base[baseDataKey]["Counts"],
        percent_less_than_3: data.Base[baseDataKey]["% MOS < 3.0"],
        percent_less_than_2: data.Base[baseDataKey]["% MOS < 2.0"],
      };
    }
  });

  const devices = Object.keys(transformedData);
  const metricMap = {
    "MOS Average": "mean",
    "MOS Stdev": "std_dev",
    "Maximum MOS": "max",
    "Counts": "count", // Changed from "Count" to "Counts" to match JSON
    "% MOS < 3.0": "percent_less_than_3",
    "% MOS < 2.0": "percent_less_than_2",
  };

  const metricDisplayNames = Object.keys(metricMap);

  return (
    <div className="voice-quality-nb-table-container mb-8">
      <h3 className="text-xl font-bold mb-4 text-gray-800">{testName} - WB Voice Quality</h3>
      <table className="min-w-full divide-y divide-gray-200 border border-gray-300">
        <thead className="bg-gray-700 text-white">
          <tr>
            <th rowSpan="2" className="px-2 py-1 text-left text-xs font-medium uppercase tracking-wider border border-gray-300"></th>
            <th colSpan={devices.length} className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">Mobile</th>
            <th colSpan={devices.length} className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">Base</th>
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
              <tr key={metricName}>
                <td className="px-2 py-1 text-sm text-gray-800 border border-gray-300 text-left bg-yellow-50">{metricName}</td>
                {/* Mobile Data (Downlink) */}
                {devices.map(device => {
                  const cellClassName = `border border-gray-300 text-center text-sm text-gray-700 bg-yellow-50`;
                  return (
                    <td key={`dl-${device}-${metricName}-data`} className={cellClassName}>
                      {transformedData[device]?.dl_mos_stats?.[originalStatKey] !== undefined
                        ? (originalStatKey.startsWith('percent')
                          ? `${(transformedData[device].dl_mos_stats[originalStatKey]).toFixed(1)}%`
                          : (originalStatKey === 'count'
                            ? parseInt(transformedData[device].dl_mos_stats[originalStatKey]).toString()
                            : transformedData[device].dl_mos_stats[originalStatKey].toFixed(2)))
                        : 'N/A'}
                    </td>
                  );
                })}
                {/* Base Data (Uplink) */}
                {devices.map(device => (
                  <td key={`ul-${device}-${metricName}-data`} className="border border-gray-300 text-center text-sm text-gray-700 bg-yellow-50">
                    {transformedData[device]?.ul_mos_stats?.[originalStatKey] !== undefined
                      ? (originalStatKey.startsWith('percent')
                        ? `${(transformedData[device].ul_mos_stats[originalStatKey]).toFixed(1)}%`
                        : (originalStatKey === 'count'
                          ? parseInt(transformedData[device].ul_mos_stats[originalStatKey]).toString()
                          : transformedData[device].ul_mos_stats[originalStatKey].toFixed(2)))
                      : 'N/A'}
                  </td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default VoiceQualityWBTable;
