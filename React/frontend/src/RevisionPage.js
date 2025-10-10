import React from 'react';

function RevisionPage() {
    return (
        <div>
            <h1 className="text-3xl font-bold mb-4">Revision Hisitory</h1>
            <div className="overflow-x-auto mb-6 table-container">
      <table className="min-w-full border border-table-grid">
        <thead>
          <tr className="bg-gray-600 text-white font-bold">
            <th className="py-2 px-4 border border-table-grid">Version</th>
            <th className="py-2 px-4 border border-table-grid">Description</th>
            <th className="py-2 px-4 border border-table-grid">Author</th>
            <th className="py-2 px-4 border border-table-grid">Revised On</th>
          </tr>
        </thead>
        <tbody>
          <tr className="bg-yellow-50">
            <td className="py-2 px-4 border border-table-grid text-center align-middle">1.0</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold">First Version</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold">Claude Li</td>
            <td className="py-2 px-4 border border-table-grid text-center bg-yellow-50 text-black-700 font-bold">10/09/2025</td>
          </tr>
          
        </tbody>
      </table>
    </div>
        </div>
    );

}
export default RevisionPage;