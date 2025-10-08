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

    const calculateAverage = (device1Data, device2Data, metricKey) => {
        const val1 = parseFloat(getMetricValue(device1Data, metricKey));
        const val2 = parseFloat(getMetricValue(device2Data, metricKey));

        const sum = (isNaN(val1) ? 0 : val1) + (isNaN(val2) ? 0 : val2);
        const count = (!isNaN(val1) ? 1 : 0) + (!isNaN(val2) ? 1 : 0);

        if (count === 0) {
            return 'N/A';
        }
        return (sum / count).toFixed(2);
    };

    const getPerformanceColor = (dutAvg, refAvg) => {
        if (isNaN(dutAvg) || isNaN(refAvg) || refAvg === 0) {
            return ''; // No specific color if data is not available or refAvg is zero
        }

        let className = '';
        if (dutAvg < 0.90 * refAvg) {
            className = 'bg-performance-excellent font-bold'; // Excellent
        } else if (dutAvg >= 0.90 * refAvg && dutAvg <= 1.10 * refAvg) {
            className = 'bg-performance-pass font-bold'; // PASS
        } else if (dutAvg > 1.10 * refAvg && dutAvg <= 1.20 * refAvg) {
            className = 'bg-performance-marginal-fail font-bold'; // Marginal Fail
        } else { // dutAvg > 1.20 * refAvg
            className = 'bg-performance-fail font-bold'; // Fail
        }
        return className;
    };

    const metrics = [
        { label: "Mean (ms)", key: "mean" },
        { label: "Average delay of 2 devices", key: "average_delay_2_devices", isSpecial: true },
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
                        <th>DUT2</th>
                        <th>REF1</th>
                        <th>REF2</th>
                    </tr>
                </thead>
                <tbody>
                    {metrics.map((metric, index) => {
                        if (metric.isSpecial) {
                            return (
                                <tr key={index}>
                                    <td>{metric.label}</td>
                                    <td colSpan="2" className={getPerformanceColor(
                                        parseFloat(calculateAverage(devices.DUT1, devices.DUT2, 'mean')),
                                        parseFloat(calculateAverage(devices.REF1, devices.REF2, 'mean'))
                                    )}>
                                        {calculateAverage(devices.DUT1, devices.DUT2, 'mean')}
                                    </td>
                                    <td colSpan="2" className={getPerformanceColor(
                                        parseFloat(calculateAverage(devices.DUT1, devices.DUT2, 'mean')),
                                        parseFloat(calculateAverage(devices.REF1, devices.REF2, 'mean'))
                                    )}>
                                        {calculateAverage(devices.REF1, devices.REF2, 'mean')}
                                    </td>
                                </tr>
                            );
                        }
                        return (
                            <tr key={index}>
                                <td>{metric.label}</td>
                                <td>{getMetricValue(devices.DUT1, metric.key)}</td>
                                <td>{getMetricValue(devices.DUT2, metric.key)}</td>
                                <td>{getMetricValue(devices.REF1, metric.key)}</td>
                                <td>{getMetricValue(devices.REF2, metric.key)}</td>
                            </tr>
                        );
                    })}
                </tbody>
            </table>
        </div>
    );
};

export default AudioDelayTable;
