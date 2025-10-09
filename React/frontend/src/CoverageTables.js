import React from 'react';
import './table-styles.css'; // Assuming a shared CSS for tables
import MapComponent from './MapComponent'; // Import the MapComponent
import haversineDistance from './utils/haversine';
import CoverageSummaryTable from './CoverageSummaryTable';

// Helper function to calculate distances and averages
const calculateDistancesAndAverages = (rawData, baseStationCoords) => {
    const processedData = {};
    const averagedCoords = {};
    const metrics = ["mos_before_drop", "call_drop", "first_dl_tp_gt_1", "first_ul_tp_gt_1"];
    const networks = ["n25", "n41", "n71"];
    const deviceTypes = ["DUT", "REF"];
    const runs = ["Run1", "Run2", "Run3", "Run4", "Run5"];

    networks.forEach(network => {
        processedData[network] = {};
        averagedCoords[network] = {};

        deviceTypes.forEach(deviceType => {
            // Check if the deviceType exists for the current network
            if (!rawData[network] || !rawData[network][deviceType]) {
                processedData[network][deviceType] = {};
                averagedCoords[network][deviceType] = {};
                metrics.forEach(metric => {
                    processedData[network][deviceType][metric] = { Average: "N/A" };
                    averagedCoords[network][deviceType][metric] = [null, null];
                });
                return; // Skip to the next deviceType
            }

            processedData[network][deviceType] = {};
            averagedCoords[network][deviceType] = {};

            metrics.forEach(metric => {
                const allLatitudes = [];
                const allLongitudes = [];
                const distances = {};

                runs.forEach(run => {
                    const coords = rawData[network][deviceType][run]?.[metric]; // Use optional chaining
                    if (coords && coords.length === 2) {
                        const distance = haversineDistance(baseStationCoords, coords);
                        distances[run] = distance.toFixed(2); // Store distance rounded to 2 decimal places
                        allLatitudes.push(coords[0]);
                        allLongitudes.push(coords[1]);
                    } else {
                        distances[run] = "N/A";
                    }
                });

                // Calculate average coordinates for the metric
                if (allLatitudes.length > 0) {
                    const avgLat = allLatitudes.reduce((sum, lat) => sum + lat, 0) / allLatitudes.length;
                    const avgLon = allLongitudes.reduce((sum, lon) => sum + lon, 0) / allLongitudes.length;
                    averagedCoords[network][deviceType][metric] = [avgLat, avgLon];
                } else {
                    averagedCoords[network][deviceType][metric] = [null, null];
                }

                // Calculate overall average distance for the metric
                const validDistances = Object.values(distances).filter(d => d !== "N/A").map(Number);
                if (validDistances.length > 0) {
                    const avgDistance = validDistances.reduce((sum, d) => sum + d, 0) / validDistances.length;
                    distances.Average = avgDistance.toFixed(2);
                } else {
                    distances.Average = "N/A";
                }

                processedData[network][deviceType][metric] = distances;
            });
        });
    });

    return { processedData, averagedCoords };
};

const renderTable = (title, data) => {
    const runs = ["Run1", "Run2", "Run3", "Run4", "Run5"];
    const deviceNames = Object.keys(data);

    return (
        <div className="table-container">
            <h3>{title}</h3>
            <table className="common-table">
                <thead>
                    <tr>
                        <th>Device Name</th>
                        {runs.map(run => <th key={run}>{run}</th>)}
                        <th>Average</th>
                    </tr>
                </thead>
                <tbody>
                    {deviceNames.map(device => (
                        <tr key={device}>
                            <td>{device}</td>
                            {runs.map(run => (
                                <td key={`${device}-${run}`}>{data[device][run]}</td>
                            ))}
                            {(() => {
                                const dutAverage = parseFloat(data.DUT?.Average);
                                const refAverage = parseFloat(data.REF?.Average);
                                const isPass = dutAverage >= 0.95 * refAverage;
                                const bgColor = isPass ? 'var(--performance-pass)' : 'var(--performance-fail)';

                                return (
                                    <td style={{ backgroundColor: bgColor }}>{data[device].Average}</td>
                                );
                            })()}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

const CoverageTables = ({ categoryName, testCaseName, coverageData, baseStationCoords, displayCategoryTitle }) => {
    const { processedData, averagedCoords } = calculateDistancesAndAverages(coverageData, baseStationCoords);

    const metricsMap = {
        "mos_before_drop": "Last MOS Value Distance (km)",
        "call_drop": "Voice Call Drop Distance (km)",
        "first_dl_tp_gt_1": "DL TP > 1 Distance (km)",
        "first_ul_tp_gt_1": "UL TP > 1 Distance (km)",
    };

    const networks = Object.keys(processedData);

    return (
        <div className="">
            <img src="/coverage_criteria.png" alt="Coverage Criteria" className="mx-auto block mb-8" style={{ width: '110%' }} />
            <CoverageSummaryTable summaryData={processedData} /> {/* Add the new table here */}
            {displayCategoryTitle && <h2 className="text-2xl font-bold mb-6 text-blue-700">{categoryName}</h2>}
            <h3 className="text-xl font-bold mb-4 text-gray-800">{testCaseName}</h3>
            
            {networks.map(network => (
                <div key={network} className="network-section">
                    <h4 className="text-lg font-semibold mb-3 text-gray-700">Network: {network.toUpperCase()}</h4>
                    {Object.entries(metricsMap).map(([metricKey, metricTitle]) => (
                        <React.Fragment key={`${network}-${metricKey}`}>
                            {renderTable(metricTitle, {
                                DUT: processedData[network].DUT[metricKey],
                                REF: processedData[network].REF[metricKey]
                            })}
                            <MapComponent
                                dutCoords={averagedCoords[network].DUT[metricKey]}
                                refCoords={averagedCoords[network].REF[metricKey]}
                                baseStationCoords={baseStationCoords}
                            />
                            <div className="map-legend" style={{ display: 'flex', justifyContent: 'flex-start', gap: '20px', marginTop: '10px' }}>
                                <div style={{ display: 'flex', alignItems: 'center' }}>
                                    <div style={{ backgroundColor: 'red', width: '12px', height: '12px', borderRadius: '50%', marginRight: '5px' }}></div>
                                    <span>DUT</span>
                                </div>
                                <div style={{ display: 'flex', alignItems: 'center' }}>
                                    <div style={{ backgroundColor: 'blue', width: '12px', height: '12px', borderRadius: '50%', marginRight: '5px' }}></div>
                                    <span>REF</span>
                                </div>
                                <div style={{ display: 'flex', alignItems: 'center' }}>
                                    <img src="https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png" alt="Base Station Icon" style={{ width: '15px', height: '25px', marginRight: '5px' }} />
                                    <span>Base Station</span>
                                </div>
                            </div>
                        </React.Fragment>
                    ))}
                </div>
            ))}
        </div>
    );
};

export default CoverageTables;
