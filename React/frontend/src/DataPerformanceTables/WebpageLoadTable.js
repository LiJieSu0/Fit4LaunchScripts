import React from 'react';

const WebpageLoadTable = () => {
  return (
    <div className="overflow-x-auto mb-6 table-container">
      <table className="min-w-full border border-table-grid">
        <thead>
          <tr className="bg-gray-600 text-white font-bold">
            <th className="py-2 px-4 border border-table-grid">5G Auto Data Web-Kepler</th>
            <th className="py-2 px-4 border border-table-grid">DUT Avg. (s)</th>
            <th className="py-2 px-4 border border-table-grid">REF Avg. (s)</th>
          </tr>
        </thead>
        <tbody>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">Web Page Load Time</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold" style={{ backgroundColor: 'var(--performance-pass)' }}>0.8</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold" style={{ backgroundColor: 'var(--performance-pass)' }}>0.83</td>

          </tr>
          
        </tbody>
      </table>
    </div>
  );
};

export default WebpageLoadTable;
