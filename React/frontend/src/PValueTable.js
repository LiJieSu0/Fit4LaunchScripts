import React from 'react';

const PValueTable = ({ callType, initiationPValue, retentionPValue }) => {
  return (
    <div className="mb-6 table-container w-1/3">
      <h3 className="text-xl font-bold mb-4 text-gray-800">P-Value Table</h3>
      <table className="common-table w-full table-fixed">
        <thead>
          <tr>
            <th className="w-1/2 px-2">Metrics</th>
            <th className="w-1/2 px-2">P-Value</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td className="w-1/2 px-2">Call Initiation</td>
            <td className="w-1/2 px-2">{initiationPValue !== undefined ? initiationPValue.toFixed(3) : 'N/A'}</td>
          </tr>
          {callType === "MO" && (
            <tr>
              <td className="w-1/2 px-2">Call Retention</td>
              <td className="w-1/2 px-2">{retentionPValue !== undefined ? retentionPValue.toFixed(3) : 'N/A'}</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default PValueTable;
