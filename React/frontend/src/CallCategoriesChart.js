import React from 'react';

const CallCategoriesChart = ({ callPerformanceData }) => {
  if (!callPerformanceData) {
    return <p>No Call Categories data available.</p>;
  }

  const { DUT, REF } = callPerformanceData;

  const processRatDistribution = (deviceData) => {
    const ratDistribution = deviceData.rat_distribution;
    const totalRats = Object.values(ratDistribution).reduce((sum, count) => sum + count, 0);

    const categories = {
      "VoLTE": ratDistribution.VoLTE || 0,
      "5G SA": ratDistribution.VoNR || 0, // Assuming VoNR maps to 5G SA
      "EPSFB": ratDistribution.EPSFB || 0,
      "Unknown": (ratDistribution["VoNR-VoLTE"] || 0) + (ratDistribution["Etc."] || 0), // Grouping VoNR-VoLTE and Etc. as Unknown for simplicity based on image
    };

    const categoryPercentages = {};
    for (const key in categories) {
      categoryPercentages[key] = totalRats > 0 ? ((categories[key] / totalRats) * 100).toFixed(1) : "0.0";
    }

    return {
      total: totalRats,
      raw: categories,
      percentages: categoryPercentages,
    };
  };

  const dutCategories = processRatDistribution(DUT);
  const refCategories = processRatDistribution(REF);

  const categoriesOrder = ["VoLTE", "5G SA", "EPSFB", "Unknown"];
  const categoryColors = {
    "VoLTE": "bg-blue-700",
    "5G SA": "bg-blue-400",
    "EPSFB": "bg-green-600",
    "Unknown": "bg-gray-500",
  };

  return (
    <div className="mb-6">
      <h3 className="text-xl font-bold mb-4 text-gray-800">Call Categories</h3>

      {/* Chart */}
      <div className="flex justify-center"> {/* Centered chart */}
        <div className="flex flex-col space-y-4 w-2/3"> {/* Chart container, reduced width */}
          {/* Legend */}
          <div className="flex justify-start space-x-4 mb-4">
            {categoriesOrder.map(category => (
              <div key={category} className="flex items-center">
                <span className={`inline-block w-4 h-4 ${categoryColors[category]} mr-2`}></span>
                <span>{category}</span>
              </div>
            ))}
          </div>
          {/* DUT Bar */}
          <div className="flex items-center">
            <div className="text-left mr-2">DUT</div>
            <div className="flex-1 h-8 bg-gray-200 flex rounded overflow-hidden">
              {categoriesOrder.map(category => {
                const percentage = parseFloat(dutCategories.percentages[category]);
                return percentage > 0 && (
                  <div
                    key={`dut-${category}`}
                    className={`${categoryColors[category]} h-full flex items-center justify-center text-white text-xs`}
                    style={{ width: `${percentage}%` }}
                  >
                    {percentage >= 5.0 ? `${percentage}%` : ''}
                  </div>
                );
              })}
            </div>
          </div>

          {/* Reference Bar */}
          <div className="flex items-center">
            <div className="text-left mr-2">REF</div>
            <div className="flex-1 h-8 bg-gray-200 flex rounded overflow-hidden">
              {categoriesOrder.map(category => {
                const percentage = parseFloat(refCategories.percentages[category]);
                return percentage > 0 && (
                  <div
                    key={`ref-${category}`}
                    className={`${categoryColors[category]} h-full flex items-center justify-center text-white text-xs`}
                    style={{ width: `${percentage}%` }}
                  >
                    {percentage >= 5.0 ? `${percentage}%` : ''}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      {/* Data Table */}
      <div className="overflow-x-auto mt-6 table-container"> {/* Table container, with mt-6 re-added */}
        <table className="min-w-full border border-table-grid">
          <thead>
            <tr className="bg-table-header-bg text-table-header-text font-bold">
              <th className="py-2 px-4 border border-table-grid">Device</th>
              {categoriesOrder.map(category => (
                <th key={category} className="py-2 px-4 border border-table-grid">{category}</th>
              ))}
              <th className="py-2 px-4 border border-table-grid">Total</th>
            </tr>
          </thead>
          <tbody>
            <tr className="bg-table-body-bg">
              <td className="py-2 px-4 border border-table-grid text-center">DUT</td>
              {categoriesOrder.map(category => (
                <td key={`dut-data-${category}`} className="py-2 px-4 border border-table-grid text-center">
                  {dutCategories.raw[category]} ({dutCategories.percentages[category]}%)
                </td>
              ))}
              <td className="py-2 px-4 border border-table-grid text-center">{dutCategories.total}</td>
            </tr>
            <tr className="bg-table-body-bg">
              <td className="py-2 px-4 border border-table-grid text-center">REF</td>
              {categoriesOrder.map(category => (
                <td key={`ref-data-${category}`} className="py-2 px-4 border border-table-grid text-center">
                  {refCategories.raw[category]} ({refCategories.percentages[category]}%)
                </td>
              ))}
              <td className="py-2 px-4 border border-table-grid text-center">{refCategories.total}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default CallCategoriesChart;
