import React from 'react';

export const getPValueColor = (pValue, dutFailurePercentage) => {
  if (pValue === undefined || pValue === null) {
    return "bg-performance-unknown";
  }

  // Condition for Excellent
  if (pValue > 0.99) {
    return "bg-performance-excellent";
  }
  // Condition for Pass
  if (pValue >= 0.05 && pValue <= 0.99) {
    return "bg-performance-pass";
  }
  // Condition for Fail
  if (pValue < 0.05) {
    // Check for Marginal Fail condition if dutFailurePercentage is provided
    // The user specified: "If Fail condition is satisfied but % MO/MT Failures (DUT) < 1%:Marginal Fail"
    // This implies that pValue < 0.05 AND dutFailurePercentage < 1%
    if (dutFailurePercentage !== undefined && dutFailurePercentage < 1) {
      return "bg-performance-marginal-fail";
    }
    return "bg-performance-fail";
  }
  return "bg-performance-unknown";
};

const PValueTable = ({ callType, initiationPValue, retentionPValue, dutFailurePercentage }) => {

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
            <td className={`w-1/2 px-2 ${getPValueColor(initiationPValue, dutFailurePercentage)}`}>
              {initiationPValue !== undefined ? initiationPValue.toFixed(3) : 'N/A'}
            </td>
          </tr>
          {callType === "MO" && (
            <tr>
              <td className="w-1/2 px-2">Call Retention</td>
              <td className={`w-1/2 px-2 ${getPValueColor(retentionPValue, dutFailurePercentage)}`}>
                {retentionPValue !== undefined ? retentionPValue.toFixed(3) : 'N/A'}
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default PValueTable;
