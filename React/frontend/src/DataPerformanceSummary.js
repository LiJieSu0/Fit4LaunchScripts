import React from 'react';
import HttpssDLTable from './DataPerformanceTables/HttpSSDL';
import HttpMsDLTable from './DataPerformanceTables/HTTPMSDL';
import UDPDL200Table from './DataPerformanceTables/UDPDL200';
import UDPDL400Table from './DataPerformanceTables/UDPDL400';
import HttpssULTable from './DataPerformanceTables/HTTPSSUL';
import HttpMsULTable from './DataPerformanceTables/HTTPMSUL';
import UDPUL10Table from './DataPerformanceTables/UDPUL10';
import UDPUL20Table from './DataPerformanceTables/UDPUL20';
import PingTable from './DataPerformanceTables/PingTable';

const DataPerformanceSummary = () => {
  return (
    <div className="data-performance-summary">
      <HttpssDLTable />
      <HttpMsDLTable />
      <UDPDL200Table />
      <UDPDL400Table/>
      <HttpssULTable />
      <HttpMsULTable />
      <UDPUL10Table />
      <UDPUL20Table />
      <PingTable />
    </div>
  );
};

export default DataPerformanceSummary;
