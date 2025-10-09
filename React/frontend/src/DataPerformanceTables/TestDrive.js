import React from 'react';

const TestDriveTable = () => {
  return (
    <div className="overflow-x-auto mb-6 table-container">
      <table className="min-w-full border border-table-grid">
        <thead>
          <tr className="bg-gray-600 text-white font-bold">
            <th className="py-2 px-4 border border-table-grid">UDP Upload Task at 20 Mbps for 10 seconds</th>
            <th className="py-2 px-4 border border-table-grid">DUT Avg. (Mbps)</th>
            <th className="py-2 px-4 border border-table-grid">REF Avg. (Mbps)</th>
            <th className="py-2 px-4 border border-table-grid">DUT Jitter (ms)</th>
            <th className="py-2 px-4 border border-table-grid">REF Jitter (ms)</th>
            <th className="py-2 px-4 border border-table-grid">DUT Error Ratio (%)</th>
            <th className="py-2 px-4 border border-table-grid">DUT Error Ratio (%)</th>
            <th className="py-2 px-4 border border-table-grid">DUT Ping Avg. (ms)</th>
            <th className="py-2 px-4 border border-table-grid">DUT Ping Avg. (ms)</th>
          </tr>
        </thead>
        <tbody>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G Auto Data Test Drive</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-pass)' }}>9.78</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-pass)' }}>9.80</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-pass)' }}>1.99</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-pass)' }}>1.91</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-pass)' }}>3.96</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-pass)' }}>2.35</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-excellent)' }}>115.56</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-excellent)' }}>148.09</td>          
          </tr>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">5G NSA Data Test Drive</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-pass)' }}>9.95</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-pass)' }}>9.82</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-marginal-fail)' }}>1.69</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-marginal-fail)' }}>1.47</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-excellent)' }}>1.04</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-excellent)' }}>1.18</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-excellent)' }}>115.56</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold"style={{ backgroundColor: 'var(--performance-excellent)' }}>148.09</td>    
          </tr>
          
        </tbody>
      </table>
    </div>
  );
};

export default TestDriveTable;