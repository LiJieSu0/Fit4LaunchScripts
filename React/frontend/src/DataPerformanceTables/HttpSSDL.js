import React from 'react';

const HttpssDLTable = () => {
  return (
    <div className="overflow-x-auto mb-6 table-container">
      <table className="min-w-full border border-table-grid">
        <thead>
          <tr className="bg-gray-600 text-white font-bold">
            <th className="py-2 px-4 border border-table-grid">File Transfer (HTTP) Single Stream DL Cases</th>
            <th className="py-2 px-4 border border-table-grid">DUT Avg. (Mbps)</th>
            <th className="py-2 px-4 border border-table-grid">REF Avg. (Mbps)</th>
          </tr>
        </thead>
        <tbody>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G Auto Data Test Stationary Location 1</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-marginal-fail)' }}>100.33</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-marginal-fail)' }}>111.51</td>

          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G Auto Data Test Stationary Location 2</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-fail)' }}>15.12</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-fail)' }}>23.94</td>
          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G Auto Data Test Stationary Location 3</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-excellent)' }}>98.08</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-excellent)' }}>82.46</td>
          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G Auto Data Test MHS Stationary Location 1</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-fail)' }}>73.39</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-fail)' }}>122.94</td>
          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G Auto Data Test MHS Stationary Location 2</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-pass)' }}>47.22</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-pass)' }}>50.39</td>
          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G NSA Data Test Stationary Moderate RF</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-excellent)' }}>56.62</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-excellent)' }}>39.23</td>
          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G NSA Data Test Stationary Poor RF</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-excellent)' }}>94.30</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-excellent)' }}>67.69</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default HttpssDLTable;
