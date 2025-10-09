import React from 'react';

function DirectoryPage() {
  return (
    <div className="directory-page">
      <h1 className="text-center">Contents</h1>
      <p></p>
      <ul>
        <li><a href="#data-performance">Data Performance</a>
          <ul style={{ paddingLeft: '20px' }}>
            <li><a href="#5g-auto-dp">5G AUTO DP</a>
              <ul style={{ paddingLeft: '20px' }}>
                <li><a href="#5g-auto-data-test-drive">5G Auto Data Test Drive</a></li>
                <li><a href="#5g-auto-data-test-mhs-drive">5G Auto Data Test MHS Drive</a></li>
                <li><a href="#5g-auto-data-test-mhs-stationary-location-1-dl">5G Auto Data Test MHS Stationary Location 1 DL</a></li>
                <li><a href="#5g-auto-data-test-mhs-stationary-location-1-ul">5G Auto Data Test MHS Stationary Location 1 UL</a></li>
                <li><a href="#5g-auto-data-test-mhs-stationary-location-2-dl">5G Auto Data Test MHS Stationary Location 2 DL</a></li>
                <li><a href="#5g-auto-data-test-mhs-stationary-location-2-ul">5G Auto Data Test MHS Stationary Location 2 UL</a></li>
                <li><a href="#5g-auto-data-test-stationary-location-1-dl">5G Auto Data Test Stationary Location 1 DL</a></li>
                <li><a href="#5g-auto-data-test-stationary-location-1-ul">5G Auto Data Test Stationary Location 1 UL</a></li>
                <li><a href="#5g-auto-data-test-stationary-location-2-dl">5G Auto Data Test Stationary Location 2 DL</a></li>
                <li><a href="#5g-auto-data-test-stationary-location-2-ul">5G Auto Data Test Stationary Location 2 UL</a></li>
                <li><a href="#5g-auto-data-test-stationary-location-3-dl">5G Auto Data Test Stationary Location 3 DL</a></li>
                <li><a href="#5g-auto-data-test-stationary-location-3-ul">5G Auto Data Test Stationary Location 3 UL</a></li>
                <li><a href="#5g-auto-data-web-kepler">5G Auto Data Web-Kepler</a></li>
                <li><a href="#5g-vonr-mrab-stationary">5G VoNR MRAB Stationary</a></li>
                <li><a href="#5g-auto-data-play-store-app-dl-stationary">5G Auto Data Play-store app DL Stationary</a></li>
              </ul>
            </li>
            <li><a href="#5g-nsa-dp">5G NSA DP</a>
              <ul style={{ paddingLeft: '20px' }}>
                <li><a href="#5g-nsa-data-test-drive">5G NSA Data Test Drive</a></li>
                <li><a href="#5g-nsa-data-test-stationary-moderate-rf-dl">5G NSA Data Test Stationary Moderate RF DL</a></li>
                <li><a href="#5g-nsa-data-test-stationary-moderate-rf-ul">5G NSA Data Test Stationary Moderate RF UL</a></li>
                <li><a href="#5g-nsa-data-test-stationary-poor-rf-dl">5G NSA Data Test Stationary Poor RF DL</a></li>
                <li><a href="#5g-nsa-data-test-stationary-poor-rf-ul">5G NSA Data Test Stationary Poor RF UL</a></li>
              </ul>
            </li>
          </ul>
        </li>
        <li>
          <a href="#call-performance">Call Performance</a>
          <ul style={{ paddingLeft: '20px' }}>
            <li><a href="#5g-auto-vonr-disabled-cp-mo-drive">5G Auto VoNR Disabled CP MO Drive</a></li>
            <li><a href="#5g-auto-vonr-disabled-cp-mt-drive">5G Auto VoNR Disabled CP MT Drive</a></li>
            <li><a href="#5g-auto-vonr-enabled-cp-mo-drive">5G Auto VoNR Enabled CP MO Drive</a></li>
            <li><a href="#5g-auto-vonr-enabled-cp-mt-drive">5G Auto VoNR Enabled CP MT Drive</a></li>
          </ul>
        </li>
        <li><a href="#voice-quality">Voice Quality</a>
          <ul style={{ paddingLeft: '20px' }}>
            <li><a href="#5g-auto-vonr-enabled-amr-nb-vq">5G Auto VoNR Enabled AMR NB VQ</a></li>
            <li><a href="#5g-auto-vonr-enabled-amr-wb-vq">5G Auto VoNR Enabled AMR WB VQ</a></li>
            <li><a href="#5g-auto-vonr-disabled-evs-wb-vq">5G Auto VoNR Disabled EVS WB VQ</a></li>
            <li><a href="#5g-auto-vonr-enabled-evs-wb-vq">5G Auto VoNR Enabled EVS WB VQ</a></li>
            <li><a href="#5g-auto-vonr-disabled-audio-delay">5G Auto VoNR Disabled Audio Delay</a></li>
            <li><a href="#5g-auto-vonr-enabled-audio-delay">5G Auto VoNR Enabled Audio Delay</a></li>
          </ul>
        </li>
        <li><a href="#coverage-performance">Coverage Performance</a>
          <ul style={{ paddingLeft: '20px' }}>
            <li><a href="#5g-vonr-coverage-test">5G VoNR Coverage Test</a>
              <ul style={{ paddingLeft: '20px' }}>
                <li><a href="#n25">n25</a></li>
                <li><a href="#n41">n41</a></li>
                <li><a href="#n71">n71</a></li>
              </ul>
            </li>
            <li><a href="#5g-n41-hpue-coverage-test">5G n41 HPUE Coverage Test</a>
            </li>
          </ul>
        </li>
      </ul>
    </div>
  );
}

export default DirectoryPage;
