import React from 'react';

const DataPerformanceSummaryTable = () => {
  return (
    <div className="data-performance-summary-table-container mb-8">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Data Performance Summary</h2>
      <table className="min-w-full divide-y divide-gray-200 border border-gray-300">
        <thead className="bg-gray-600 text-white">
          <tr>
            <th rowSpan="3" className="px-2 py-1 text-left text-xs font-medium uppercase tracking-wider border border-gray-300">Test Cases</th>
            <th colSpan="16" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">KPI for Data Performance Mobility</th>
            <th rowSpan="3" className="px-2 py-1 text-left text-xs font-medium uppercase tracking-wider border border-gray-300">Pass/Fail & Links</th>
          </tr>
          <tr>
            <th colSpan="2" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">HTTP SS Tput</th>
            <th colSpan="2" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">HTTP MS Tput</th>
            <th colSpan="2" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">UDP Tput</th>
            <th colSpan="2" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">UDP Jitter</th>
            <th colSpan="2" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">UDP Latency</th>
            <th colSpan="2" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">UDP Packet Loss</th>
            <th colSpan="2" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">PING</th>
            <th colSpan="2" className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">Webpage Load time</th>
          </tr>
          <tr>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">DUT</th>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">REF</th>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">DUT</th>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">REF</th>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">DUT</th>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">REF</th>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">DUT</th>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">REF</th>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">DUT</th>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">REF</th>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">DUT</th>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">REF</th>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">DUT</th>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">REF</th>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">DUT</th>
            <th className="px-2 py-1 text-center text-xs font-medium uppercase tracking-wider border border-gray-300">REF</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {/* Rows for Data Performance Test Cases */}
          {[
            "5G Auto Data Test Drive",
            "5G Auto Data Test Stationary Location 1 DL",
            "5G Auto Data Test Stationary Location 1 UL",
            "5G Auto Data Test Stationary Location 2 DL",
            "5G Auto Data Test Stationary Location 2 UL",
            "5G Auto Data Test Stationary Location 3 DL",
            "5G Auto Data Test Stationary Location 3 UL",
            "5G Auto Data Play-store app DL Stationary",
            "5G Auto Data Web-Kepler",
            "5G Auto Data Test MHS Drive",
            "5G Auto Data Test MHS Stationary Location 1 DL",
            "5G Auto Data Test MHS Stationary Location 1 UL",
            "5G Auto Data Test MHS Stationary Location 2 DL",
            "5G Auto Data Test MHS Stationary Location 2 UL",
            "5G NSA Data Test Drive",
            "5G NSA Data Test Stationary Moderate RF DL",
            "5G NSA Data Test Stationary Moderate RF UL",
            "5G NSA Data Test Stationary Poor RF DL",
            "5G NSA Data Test Stationary Poor RF UL",
          ].map((testCase, index) => (
            <tr key={index} className="bg-yellow-50">
              <td className="px-2 py-4 text-sm text-gray-500 border border-gray-300 text-center">{testCase}</td>
              <td className="border border-gray-300 text-center"></td>
              <td className="border border-gray-300 text-center"></td>
              <td className="border border-gray-300 text-center"></td>
              <td className="border border-gray-300 text-center"></td>
              <td className="border border-gray-300 text-center"></td>
              <td className="border border-gray-300 text-center"></td>
              <td className="border border-gray-300 text-center"></td>
              <td className="border border-gray-300 text-center"></td>
              <td className="border border-gray-300 text-center"></td>
              <td className="border border-gray-300 text-center"></td>
              <td className="border border-gray-300 text-center"></td>
              <td className="border border-gray-300 text-center"></td>
              <td className="border border-gray-300 text-center"></td>
              <td className="border border-gray-300 text-center"></td>
              <td className="border border-gray-300 text-center"></td>
              <td className="border border-gray-300 text-center"></td>
              <td className="border border-gray-300 text-center"></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DataPerformanceSummaryTable;
