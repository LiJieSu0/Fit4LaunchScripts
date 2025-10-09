import React from 'react';

function DirectoryPage() {
  return (
    <div className="directory-page container mx-auto p-4">
      <h1 className="text-center text-3xl font-bold mb-4">Contents</h1>
      <p></p>
      <ul className="list-disc pl-5 space-y-2">
        <li><a className="font-bold text-lg">Data Performance</a>
          <ul className="list-disc ml-5 space-y-1">
            <li><a>5G AUTO DP</a>
              <ul className="list-disc ml-5 space-y-1">
                <li><a>5G Auto Data Test Drive</a></li>
                <li><a>5G Auto Data Test MHS Drive</a></li>
                <li><a>5G Auto Data Test MHS Stationary Location 1 DL</a></li>
                <li><a>5G Auto Data Test MHS Stationary Location 1 UL</a></li>
                <li><a>5G Auto Data Test MHS Stationary Location 2 DL</a></li>
                <li><a>5G Auto Data Test MHS Stationary Location 2 UL</a></li>
                <li><a>5G Auto Data Test Stationary Location 1 DL</a></li>
                <li><a>5G Auto Data Test Stationary Location 1 UL</a></li>
                <li><a>5G Auto Data Test Stationary Location 2 DL</a></li>
                <li><a>5G Auto Data Test Stationary Location 2 UL</a></li>
                <li><a>5G Auto Data Test Stationary Location 3 DL</a></li>
                <li><a>5G Auto Data Test Stationary Location 3 UL</a></li>
                <li><a>5G Auto Data Web-Kepler</a></li>
                <li><a>5G VoNR MRAB Stationary</a></li>
                <li><a>5G Auto Data Play-store app DL Stationary</a></li>
              </ul>
            </li>
            <li><a>5G NSA DP</a>
              <ul className="list-disc ml-5 space-y-1">
                <li><a>5G NSA Data Test Drive</a></li>
                <li><a>5G NSA Data Test Stationary Moderate RF DL</a></li>
                <li><a>5G NSA Data Test Stationary Moderate RF UL</a></li>
                <li><a>5G NSA Data Test Stationary Moderate RF UL</a></li>
                <li><a>5G NSA Data Test Stationary Poor RF DL</a></li>
                <li><a>5G NSA Data Test Stationary Poor RF UL</a></li>
              </ul>
            </li>
          </ul>
        </li>
        <li>
          <a className="font-bold text-lg">Call Performance</a>
          <ul className="list-disc ml-5 space-y-1">
            <li><a>5G Auto VoNR Disabled CP MO Drive</a></li>
            <li><a>5G Auto VoNR Disabled CP MT Drive</a></li>
            <li><a>5G Auto VoNR Enabled CP MO Drive</a></li>
            <li><a>5G Auto VoNR Enabled CP MT Drive</a></li>
          </ul>
        </li>
        <li><a className="font-bold text-lg">Voice Quality</a>
          <ul className="list-disc ml-5 space-y-1">
            <li><a>5G Auto VoNR Enabled AMR NB VQ</a></li>
            <li><a>5G Auto VoNR Enabled AMR WB VQ</a></li>
            <li><a>5G Auto VoNR Disabled EVS WB VQ</a></li>
            <li><a>5G Auto VoNR Enabled EVS WB VQ</a></li>
                <li><a>5G Auto VoNR Disabled Audio Delay</a></li>
            <li><a>5G Auto VoNR Enabled Audio Delay</a></li>
          </ul>
        </li>
        <li><a className="font-bold text-lg">Coverage Performance</a>
          <ul className="list-disc ml-5 space-y-1">
            <li><a>5G VoNR Coverage Test</a>
              <ul className="list-disc ml-5 space-y-1">
                <li><a>5G VoNR Coverage Test-n25</a></li>
                <li><a>5G VoNR Coverage Test-n41</a></li>
                <li><a>5G VoNR Coverage Test-n71</a></li>
              </ul>
            </li>
            <li><a>5G n41 HPUE Coverage Test</a>
            </li>
          </ul>
        </li>
      </ul>
    </div>
  );
}

export default DirectoryPage;
