import React from 'react';

const HttpssULTable = () => {
  return (
    <div className="overflow-x-auto mb-6 table-container">
      <table className="min-w-full border border-table-grid">
        <thead>
          <tr className="bg-gray-600 text-white font-bold">
            <th className="py-2 px-4 border border-table-grid">Single Stream HTTP Upload of a 15 MB file Cases</th>
            <th className="py-2 px-4 border border-table-grid">DUT Avg. (Mbps)</th>
            <th className="py-2 px-4 border border-table-grid">REF Avg. (Mbps)</th>
          </tr>
        </thead>
        <tbody>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G Auto Data Test Stationary Location 1</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold">Results</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold">Results</td>

          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G Auto Data Test Stationary Location 2</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold">Results</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold">Results</td>
          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G Auto Data Test Stationary Location 3</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold">Results</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold">Results</td>
          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G Auto Data Test MHS Stationary Location 1</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold">Results</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold">Results</td>
          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G Auto Data Test MHS Stationary Location 2</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold">Results</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold">Results</td>
          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G NSA Data Test Stationary Moderate RF</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold">Results</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold">Results</td>
          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G NSA Data Test Stationary Poor RF</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold">Results</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold">Results</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default HttpssULTable;
