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
import TestDriveTable from './DataPerformanceTables/TestDrive';
import WebpageLoadTable from './DataPerformanceTables/WebpageLoadTable';
import MrabTable from './DataPerformanceTables/Mrab';
import MHSDriveTable from './DataPerformanceTables/MHSDrive';

const DataPerformanceSummary = () => {
  return (
    <div className="data-performance-summary">
      <h2>Data Performance Summary- Seattle Market</h2>
      <HttpssDLTable />
      <HttpMsDLTable />
      <UDPDL200Table />
      <UDPDL400Table/>
      <HttpssULTable />
      <HttpMsULTable />
      <UDPUL10Table />
      <UDPUL20Table />
      <PingTable />
      <TestDriveTable />
      <WebpageLoadTable />
      <MrabTable />
      <MHSDriveTable />
    </div>
  );
};

export default DataPerformanceSummary;
