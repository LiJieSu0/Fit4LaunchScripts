import React from 'react';
import './VoiceQualityTable.css';

const VoiceQualityTable = ({ data, testName }) => { // Accept testName as a prop
    if (!data) {
        return <div>No voice quality data available.</div>;
    }

    // The 'data' prop directly contains the test category data (e.g., { "DUT1": {...}, "DUT2": {...}, "REF": {...} })
    const testCategoryData = data;
    const testCategoryDisplayName = testName || "Voice Quality Statistics"; // Use testName prop or a default

    if (!testCategoryData || Object.keys(testCategoryData).length === 0) {
        return <div>No detailed voice quality data available.</div>;
    }

    // console.log("VoiceQualityTable received data:", testCategoryData); // Debugging line removed

    const getMetricValue = (deviceData, statType, metricKey) => {
        if (!deviceData || !deviceData[statType]) {
            return 'N/A';
        }
        const value = deviceData[statType][metricKey];
        if (value === undefined || value === null) {
            return 'N/A';
        }
        if (metricKey.startsWith('percent_less_than_')) {
            return value.toFixed(2) + '%';
        }
        if (metricKey === 'count') {
            return Math.round(value); // Display as integer
        }
        if (typeof value === 'number') {
            return value.toFixed(2);
        }
        return value;
    };

    const metrics = [
        { label: "MOS Average", ulKey: "mean", dlKey: "mean" },
        { label: "MOS Stdev", ulKey: "std_dev", dlKey: "std_dev" },
        { label: "Maximum MOS", ulKey: "max", dlKey: "max" },
        // { label: "Dropped Calls", ulKey: null, dlKey: null }, // Removed as per user request
        { label: "Count", ulKey: "count", dlKey: "count" },
        { label: "% MOS < 3.0", ulKey: "percent_less_than_3", dlKey: "percent_less_than_3" },
        { label: "% MOS < 2.0", ulKey: "percent_less_than_2", dlKey: "percent_less_than_2" },
    ];

    const devices = {
        "REF": testCategoryData.REF,
        "DUT1": testCategoryData.DUT1,
        "DUT2": testCategoryData.DUT2,
    };

    // Ensure all device data objects exist to prevent errors
    const refData = devices.REF || {};
    const dut1Data = devices.DUT1 || {};
    const dut2Data = devices.DUT2 || {};

    return (
        <div className="voice-quality-table-container">
            {/* <h2>{testCategoryDisplayName}</h2> Removed as per user request */}
            <table className="common-table voice-quality-table">
                <thead>
                    <tr>
                        <th rowSpan="2"></th>
                        <th colSpan="3">Downlink</th>
                        <th colSpan="3">Uplink</th>
                    </tr>
                    <tr>
                        <th>REF</th>
                        <th>DUT1</th>
                        <th>DUT2</th>
                        <th>REF</th>
                        <th>DUT1</th>
                        <th>DUT2</th>
                    </tr>
                </thead>
                <tbody>
                    {metrics.map((metric, index) => (
                        <tr key={index}>
                            <td>{metric.label}</td>
                            {/* Downlink */}
                            <td>{metric.dlKey ? getMetricValue(refData, "dl_mos_stats", metric.dlKey) : 'N/A'}</td>
                            <td>{metric.dlKey ? getMetricValue(dut1Data, "dl_mos_stats", metric.dlKey) : 'N/A'}</td>
                            <td>{metric.dlKey ? getMetricValue(dut2Data, "dl_mos_stats", metric.dlKey) : 'N/A'}</td>
                            {/* Uplink */}
                            <td>{metric.ulKey ? getMetricValue(refData, "ul_mos_stats", metric.ulKey) : 'N/A'}</td>
                            <td>{metric.ulKey ? getMetricValue(dut1Data, "ul_mos_stats", metric.ulKey) : 'N/A'}</td>
                            <td>{metric.ulKey ? getMetricValue(dut2Data, "ul_mos_stats", metric.ulKey) : 'N/A'}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default VoiceQualityTable;
