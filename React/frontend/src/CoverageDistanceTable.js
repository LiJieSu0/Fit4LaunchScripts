import React from 'react';
import './SummaryTable.css'; // Assuming a shared CSS for tables

const CoverageDistanceTable = ({ title, headers, rows }) => {
    if (!headers || !rows || rows.length === 0) {
        return <div>No data available for {title}.</div>;
    }

    return (
        <div className="table-container">
            <h3>{title}</h3>
            <table className="common-table">
                <thead>
                    <tr>
                        {headers.map((header, index) => (
                            <th key={index}>{header}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {rows.map((row, rowIndex) => (
                        <tr key={rowIndex}>
                            {headers.map((header, colIndex) => (
                                <td key={`${rowIndex}-${colIndex}`}>
                                    {typeof row[header] === 'number' ? row[header].toFixed(2) : row[header]}
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default CoverageDistanceTable;
