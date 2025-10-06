import React from 'react';
import './table-styles.css'; // Assuming a shared CSS for tables
import MapComponent from './MapComponent'; // Import the MapComponent

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

const CoverageTables = ({ categoryName, testCaseName, processedCoverageData, avgCoords, baseStationCoords, displayCategoryTitle }) => {
    const metrics = {
        "last_mos_value_coords": "Last MOS Value Distance (km)",
        "voice_call_drop_coords": "Voice Call Drop Distance (km)",
        "first_dl_tp_gt_1_coords": "DL TP < 1 Distance (km)",
        "first_ul_tp_gt_1_coords": "UL TP < 1 Distance (km)",
    };

    return (
        <div className="category-section">
            {displayCategoryTitle && <h2 className="text-2xl font-bold mb-6 text-blue-700">{categoryName}</h2>}
            <h3 className="text-xl font-bold mb-4 text-gray-800">{testCaseName}</h3>
            
            {Object.entries(metrics).map(([metricKey, metricTitle]) => (
                <React.Fragment key={metricKey}>
                    {renderTable(metricTitle, processedCoverageData[metricKey])}
                    <MapComponent
                        dutCoords={avgCoords[`avgDut${metricKey.replace(/_coords$/, '').split('_').map(s => s.charAt(0).toUpperCase() + s.slice(1)).join('')}`]}
                        refCoords={avgCoords[`avgRef${metricKey.replace(/_coords$/, '').split('_').map(s => s.charAt(0).toUpperCase() + s.slice(1)).join('')}`]}
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
    );
};

export default CoverageTables;
