import React from 'react';

const PingTable = () => {
  return (
    <div className="overflow-x-auto mb-6 table-container">
      <table className="min-w-full border border-table-grid">
        <thead>
          <tr className="bg-gray-600 text-white font-bold">
            <th className="py-2 px-4 border border-table-grid">25x64 bytes PING (ICMP) Cases</th>
            <th className="py-2 px-4 border border-table-grid">DUT Avg. (ms)</th>
            <th className="py-2 px-4 border border-table-grid">REF Avg. (ms)</th>
          </tr>
        </thead>
        <tbody>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G Auto Data Test Stationary Location 1</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-fail)' }}>54.76</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-fail)' }}>42.74</td>

          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G Auto Data Test Stationary Location 2</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-fail)' }}>87.10</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-fail)' }}>56.48</td>
          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G Auto Data Test Stationary Location 3</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-fail)' }}>55.12</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-fail)' }}>41.10</td>
          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G Auto Data Test MHS Stationary Location 1</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-excellent)' }}>115.56</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-excellent)' }}>148.09</td>
          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G Auto Data Test MHS Stationary Location 2</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-excellent)' }}>82.61</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-excellent)' }}>164.05</td>
          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G NSA Data Test Stationary Moderate RF</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-excellent)' }}>53.81</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-excellent)' }}>81.33</td>
          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G NSA Data Test Stationary Poor RF</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-pass)' }}>52.52</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-pass)' }}>54.39</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default PingTable;