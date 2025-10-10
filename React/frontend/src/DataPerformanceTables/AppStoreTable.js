import React from 'react';

const AppStoreTable = () => {
  return (
    <div className="overflow-x-auto mb-6 table-container">
      <table className="min-w-full border border-table-grid">
        <thead>
          <tr className="bg-gray-600 text-white font-bold">
            <th className="py-2 px-4 border border-table-grid">5G Auto Data Play-store app DL Stationary</th>
            <th className="py-2 px-4 border border-table-grid">DUT Avg. (Mbps)</th>
            <th className="py-2 px-4 border border-table-grid">REF Avg. (Mbps)</th>
          </tr>
        </thead>
        <tbody>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G Auto Data Test Stationary - Good -30M</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold" style={{ backgroundColor: 'var(--performance-fail)' }}>77.14</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold" style={{ backgroundColor: 'var(--performance-fail)' }}>104.79</td>

          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G Auto Data Test Stationary - Moderate -30M</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold" style={{ backgroundColor: 'var(--performance-excellent)' }}>30.51</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold" style={{ backgroundColor: 'var(--performance-excellent)' }}>23.04</td>
          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G Auto Data Test Stationary - Poor -30M</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-fail)' }}>63.49</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-fail)' }}>102.94</td>
          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G Auto Data Test Stationary - Good -60M</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold" style={{ backgroundColor: 'var(--performance-fail)' }}>218.90</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold" style={{ backgroundColor: 'var(--performance-fail)' }}>302.13</td>

          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G Auto Data Test Stationary - Moderate -60M</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold" style={{ backgroundColor: 'var(--performance-fail)' }}>54.41</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold" style={{ backgroundColor: 'var(--performance-fail)' }}>107.53</td>
          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G Auto Data Test Stationary - Poor -60M</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-fail)' }}>189.93</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-fail)' }}>261.01</td>
          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G Auto Data Test Stationary - Good -100M</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold" style={{ backgroundColor: 'var(--performance-fail)' }}>160.24</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold" style={{ backgroundColor: 'var(--performance-fail)' }}>385.17</td>

          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G Auto Data Test Stationary - Moderate -100M</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold" style={{ backgroundColor: 'var(--performance-fail)' }}>57.23</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold" style={{ backgroundColor: 'var(--performance-fail)' }}>134.85</td>
          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G Auto Data Test Stationary - Poor -100M</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-fail)' }}>176.45</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-fail)' }}>295.14</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default AppStoreTable;
