import React from 'react';

const MHSDriveTable = () => {
  return (
    <div className="overflow-x-auto mb-6 table-container">
      <table className="min-w-full border border-table-grid">
        <thead>
          <tr className="bg-gray-600 text-white font-bold">
            <th className="py-2 px-4 border border-table-grid">MHS Drive Test Metrics</th>
            <th className="py-2 px-4 border border-table-grid">DUT Value</th>
            <th className="py-2 px-4 border border-table-grid">REF Value</th>
          </tr>
        </thead>
        <tbody>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">Throughput DL Mean</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold" style={{ backgroundColor: 'var(--performance-pass)' }}>8.55 Mbps</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold" style={{ backgroundColor: 'var(--performance-pass)' }}>8.96 Mbps</td>

          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">Throughput UL Mean</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold" style={{ backgroundColor: 'var(--performance-pass)' }}>7.56 Mbps</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold" style={{ backgroundColor: 'var(--performance-pass)' }}>7.83 Mbps</td>
          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">Jitter DL Mean</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-fail)' }}>32.18 ms</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-fail)' }}>23.85 ms</td>
          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">Jitter UL Mean</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-excellent)' }}>2.06 ms</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-excellent)' }}>3.43 ms</td>
          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">Error Ratio DL Mean</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold" style={{ backgroundColor: 'var(--performance-pass)' }}>11.70 %</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold" style={{ backgroundColor: 'var(--performance-pass)' }}>9.07 %</td>
          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">Error Ratio UL Mean</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold" style={{ backgroundColor: 'var(--performance-pass)' }}>15.35 %</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold" style={{ backgroundColor: 'var(--performance-pass)' }}>14.53 %</td>
          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">Ping RTT Mean</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-marginal-fail)' }}>117.09 ms</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-marginal-fail)' }}>98.23 ms</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default MHSDriveTable;
