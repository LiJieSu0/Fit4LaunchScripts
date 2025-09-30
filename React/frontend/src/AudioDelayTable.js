import React from 'react';
import './AudioDelayTable.css';

const AudioDelayTable = ({ data, testName }) => {
    if (!data) {
        return <div>No audio delay data available.</div>;
    }

    const audioDelayData = data;
    const testCategoryDisplayName = testName || "Audio Delay Statistics";

    if (!audioDelayData || Object.keys(audioDelayData).length === 0) {
        return <div>No detailed audio delay data available.</div>;
    }

    const getMetricValue = (deviceData, metricKey) => {
        if (!deviceData) {
            return 'N/A';
        }
        const value = deviceData[metricKey];
        if (value === undefined || value === null) {
            return 'N/A';
        }
        if (typeof value === 'number') {
            if (metricKey === 'occurrences') {
                return parseInt(value);
            }
            return value.toFixed(2);
        }
        return value;
    };

    const metrics = [
        { label: "Mean (ms)", key: "mean" },
        { label: "Std Dev", key: "std_dev" },
        { label: "Minimum (ms)", key: "min" },
        { label: "Maximum (ms)", key: "max" },
        { label: "Counts", key: "occurrences" },
    ];

    const devices = {
        "DUT1": audioDelayData.DUT1,
        "REF1": audioDelayData.REF1,
        "DUT2": audioDelayData.DUT2,
        "REF2": audioDelayData.REF2,
    };

    return (
        <div className="audio-delay-table-container">
            <table className="common-table audio-delay-table">
                <thead>
                    <tr>
                        <th></th>
                        <th>DUT1</th>
                        <th>REF1</th>
                        <th>DUT2</th>
                        <th>REF2</th>
                    </tr>
                </thead>
                <tbody>
                    {metrics.map((metric, index) => (
                        <tr key={index}>
                            <td>{metric.label}</td>
                            <td>{getMetricValue(devices.DUT1, metric.key)}</td>
                            <td>{getMetricValue(devices.REF1, metric.key)}</td>
                            <td>{getMetricValue(devices.DUT2, metric.key)}</td>
                            <td>{getMetricValue(devices.REF2, metric.key)}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default AudioDelayTable;
