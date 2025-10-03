import React from 'react';
import './table-styles.css'; // Assuming a shared CSS for tables
import MapComponent from './MapComponent'; // Import the MapComponent

const processData = (rawCoverageData, metricKey) => {
    const devices = ["DUT1", "DUT2", "DUT3", "REF1", "REF2", "REF3"];
    const runs = ["Run1", "Run2", "Run3", "Run4", "Run5"];
    const tableData = {};

    devices.forEach(device => {
        tableData[device] = {};
        let sumDistance = 0;
        let runCount = 0;

        runs.forEach(run => {
            const key = `${device}_${run}`;
            if (rawCoverageData[key] && rawCoverageData[key][metricKey]) {
                const distance = parseFloat(rawCoverageData[key][metricKey].distance_to_base_station_km);
                tableData[device][run] = distance.toFixed(3);
                sumDistance += distance;
                runCount++;
            } else {
                tableData[device][run] = 'N/A';
            }
        });

        tableData[device].Average = runCount > 0 ? (sumDistance / runCount).toFixed(3) : 'N/A';
    });
    return tableData;
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
                            <td>{data[device].Average}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

const CoverageTables = ({ categoryName, testCaseName, rawCoverageData, avgDutMosCoords, avgRefMosCoords, avgDutDropCoords, avgRefDropCoords, avgDutDlTpCoords, avgRefDlTpCoords, avgDutUlTpCoords, avgRefUlTpCoords, baseStationCoords }) => {
    const lastMosData = processData(rawCoverageData, "last_mos_value_coords");
    const voiceCallDropData = processData(rawCoverageData, "voice_call_drop_coords");
    const dlTpData = processData(rawCoverageData, "first_dl_tp_gt_1_coords");
    const ulTpData = processData(rawCoverageData, "first_ul_tp_gt_1_coords");

    return (
        <div className="category-section">
            <h2 className="text-2xl font-bold mb-6 text-blue-700">{categoryName}</h2>
            <h3 className="text-xl font-bold mb-4 text-gray-800">{testCaseName}</h3>
            {renderTable("Last MOS Value Distance (km)", lastMosData)}
            <MapComponent
                dutCoords={avgDutMosCoords}
                refCoords={avgRefMosCoords}
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
            {renderTable("Voice Call Drop Distance (km)", voiceCallDropData)}
            <MapComponent
                dutCoords={avgDutDropCoords}
                refCoords={avgRefDropCoords}
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
            {renderTable("DL TP < 1 Distance (km)", dlTpData)}
            <MapComponent
                dutCoords={avgDutDlTpCoords}
                refCoords={avgRefDlTpCoords}
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
            {renderTable("UL TP < 1 Distance (km)", ulTpData)}
            <MapComponent
                dutCoords={avgDutUlTpCoords}
                refCoords={avgRefUlTpCoords}
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
        </div>
    );
};

export default CoverageTables;
