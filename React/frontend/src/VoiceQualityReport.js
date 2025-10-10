import React from 'react';
import allResults from './data_analysis_results.json'; // Assuming data_analysis_results.json is the source

import AudioDelayTable from './AudioDelayTable';
import AudioDelaySummaryTable from './AudioDelaySummaryTable';
import VQAMRSummaryTable from './VQAmrSummaryTable';
import VQEVSsummaryTable from './VQEVSsummaryTable'; // Import the new EVS summary table
import VQAmrNBTable from './VQAmrNBTable';
import VQAmrWBTable from './VQAmrWBTable'; // Import the new AMR WB table
import VQEVSDisableTable from './VQEVSDisableTable';
import VQEVSEenableTABLE from './VQEVSEenableTABLE';
import VQAudioDisableTable from './VQAudioDisableTable';
import VQAudioEnableTable from './VQAudioEnableTable';

// Helper function to extract only Voice Quality and Audio Delay test cases
const extractVoiceQualityTestCases = (data, currentPath = []) => {
  let extracted = [];

  // Check if the current data object is a Voice Quality WB test case (AMR or EVS)
  const isVoiceQualityWBTest = (currentPath.includes("5G Auto VoNR Disabled EVS WB VQ") ||
                                currentPath.includes("5G Auto VoNR Enabled EVS WB VQ") ||
                                currentPath.includes("5G Auto VoNR Enabled AMR WB VQ")) &&
                               Object.keys(data).includes("Base") &&
                               Object.keys(data).includes("Mobile") &&
                               Object.values(data.Base || {}).every(deviceData =>
                                 typeof deviceData === 'object' && deviceData !== null &&
                                 deviceData["MOS Average"] !== undefined
                               ) &&
                               Object.values(data.Mobile || {}).every(deviceData =>
                                 typeof deviceData === 'object' && deviceData !== null &&
                                 deviceData["MOS Average"] !== undefined
                               );

  if (isVoiceQualityWBTest) {
    extracted.push({
      name: currentPath.join(" - "),
      data: data,
      isVoiceQuality: false,
      isAudioDelay: false,
      isVoiceQualityNB: false,
      isVoiceQualityWB: true,
    });
    return extracted; // Stop further recursion for this branch
  }

  // Check if the current data object is a Voice Quality NB test case
  const isVoiceQualityNBTest = currentPath.includes("5G Auto VoNR Enabled AMR NB VQ") &&
                               Object.keys(data).some(key => key.startsWith("DUT")) &&
                               Object.keys(data).some(key => key.startsWith("REF")) &&
                               Object.values(data).every(deviceData => 
                                 typeof deviceData === 'object' && deviceData !== null &&
                                 deviceData.ul_mos_stats && deviceData.dl_mos_stats
                               );

  if (isVoiceQualityNBTest) {
    extracted.push({
      name: currentPath.join(" - "),
      data: data,
      isVoiceQuality: false,
      isAudioDelay: false,
      isVoiceQualityNB: true,
      isVoiceQualityWB: false,
    });
    return extracted; // Stop further recursion for this branch
  }

  const isVoiceQualityTest = Object.keys(data).some(key => key.startsWith("DUT")) &&
                             Object.keys(data).some(key => key.startsWith("REF")) &&
                             Object.values(data).every(deviceData => 
                               typeof deviceData === 'object' && deviceData !== null &&
                               deviceData.ul_mos_stats && deviceData.dl_mos_stats
                             );

  if (isVoiceQualityTest) {
    extracted.push({
      name: currentPath.join(" - "),
      data: data,
      isVoiceQuality: true,
      isAudioDelay: false,
      isVoiceQualityNB: false,
      isVoiceQualityWB: false,
    });
    return extracted; // Stop further recursion for this branch
  }

  // Check if the current data object is an Audio Delay test case
  const isAudioDelayTest = Object.keys(data).includes("DUT1") &&
                           Object.keys(data).includes("REF1") &&
                           Object.keys(data).includes("DUT2") &&
                           Object.keys(data).includes("REF2") &&
                           Object.values(data).every(deviceData =>
                               typeof deviceData === 'object' && deviceData !== null &&
                               deviceData.mean !== undefined &&
                               deviceData.std_dev !== undefined &&
                               deviceData.min !== undefined &&
                               deviceData.max !== undefined &&
                               deviceData.occurrences !== undefined
                           );

  if (isAudioDelayTest) {
    extracted.push({
      name: currentPath.join(" - "),
      data: data,
      isVoiceQuality: false,
      isAudioDelay: true,
      isVoiceQualityNB: false,
      isVoiceQualityWB: false,
    });
    return extracted; // Stop further recursion for this branch
  }

  // Recurse into children
  for (const key in data) {
    if (typeof data[key] === 'object' && data[key] !== null) {
      const result = extractVoiceQualityTestCases(data[key], [...currentPath, key]);
      extracted = extracted.concat(result);
    }
  }

  return extracted;
};

const VoiceQualityReport = () => {
  const voiceQualityTestCases = extractVoiceQualityTestCases(allResults);

  // Group test cases by their top-level category for rendering headers
  const groupedByCategories = voiceQualityTestCases.reduce((acc, testCase) => {
    const category = testCase.name.split(' - ')[0];
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(testCase);
    return acc;
  }, {});

  return (
    <>
      <img src="/voice_quality_criteria1.png" alt="Voice Quality Criteria 1" className="mx-auto block mb-8" style={{ width: '110%' }} />
      <img src="/voice_quality_criteria3.png" alt="Voice Quality Criteria 2" className="mx-auto block mb-8" style={{ width: '110%' }} />
      <img src="/voice_quality_criteria2.png" alt="Voice Quality Criteria 2" className="mx-auto block mb-8" style={{ width: '110%' }} />

      <h2>Voice Quality Summary - Seattle Market</h2>
      <VQAMRSummaryTable />
      <VQEVSsummaryTable /> {/* Render the new EVS summary table */}
      <AudioDelaySummaryTable />
      <h2>Voice Quality - 3.1 5G Auto VoNR Enabled AMR NB VQ </h2>
      <VQAmrNBTable/>
      <h2>Voice Quality - 3.2 5G Auto VoNR Enabled AMR WB VQ </h2>
      <VQAmrWBTable/>
      <h2>Voice Quality - 3.3 5G Auto VoNR Disabled EVS WB VQ </h2>
      <VQEVSDisableTable/>
      <h2>Voice Quality - 3.4 5G Auto VoNR Enabled EVS WB VQ </h2>
      <VQEVSEenableTABLE/>
      <h2>Voice Quality - 3.5 5G Auto VoNR Disabled Audio Delay </h2>
      <VQAudioDisableTable/>
      <h2>Voice Quality - 3.6 5G Auto VoNR Enabled Audio Delay </h2>
      <VQAudioEnableTable/>
      {Object.entries(groupedByCategories).map(([categoryName, testCases]) => (
        <div key={categoryName} className="category-section">
          {testCases.map(testCase => {
            if (testCase.isAudioDelay) {
              return (
                <div key={testCase.name} className="report-section">
                  <h3 className="text-xl font-bold mb-4 text-gray-800">{testCase.name}</h3>
                  <AudioDelayTable data={testCase.data} testName={testCase.name} />
                </div>
              );
            }
            return null;
          })}
        </div>
      ))}
    </>
  );
};

export default VoiceQualityReport;
