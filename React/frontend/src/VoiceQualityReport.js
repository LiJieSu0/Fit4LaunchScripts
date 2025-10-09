import React from 'react';
import allResults from './data_analysis_results.json'; // Assuming data_analysis_results.json is the source
import VoiceQualityTable from './VoiceQualityTable';
import AudioDelayTable from './AudioDelayTable';
import VoiceQualitySummaryTable from './VoiceQualitySummaryTable';
import AudioDelaySummaryTable from './AudioDelaySummaryTable';
import VoiceQualityNBTable from './VoiceQualityNBTable';
import VoiceQualityAdditionalTable from './VoiceQualityAdditionalTable';
import VoiceQualityWBTable from './VoiceQualityWBTable'; // Import the new WB table component

// Helper function to extract only Voice Quality and Audio Delay test cases
const extractVoiceQualityTestCases = (data, currentPath = []) => {
  let extracted = [];

  // Check if the current data object is a Voice Quality WB test case
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
      <img src="/voice_quality_criteria2.png" alt="Voice Quality Criteria 2" className="mx-auto block mb-8" style={{ width: '110%' }} />
      <VoiceQualitySummaryTable />
      <VoiceQualityAdditionalTable /> {/* Render the new additional table */}
      <AudioDelaySummaryTable />
      {Object.entries(groupedByCategories).map(([categoryName, testCases]) => (
        <div key={categoryName} className="category-section">
          {testCases.map(testCase => {
            if (testCase.isVoiceQuality) {
              return (
                <div key={testCase.name} className="report-section">
                  <h3 className="text-xl font-bold mb-4 text-gray-800">{testCase.name}</h3>
                  <VoiceQualityTable data={testCase.data} testName={testCase.name} />
                </div>
              );
            } else if (testCase.isAudioDelay) {
              return (
                <div key={testCase.name} className="report-section">
                  <h3 className="text-xl font-bold mb-4 text-gray-800">{testCase.name}</h3>
                  <AudioDelayTable data={testCase.data} testName={testCase.name} />
                </div>
              );
            } else if (testCase.isVoiceQualityWB) { // New condition for WB tables
              return (
                <div key={testCase.name} className="report-section">
                  <VoiceQualityWBTable data={testCase.data} testName={testCase.name} />
                </div>
              );
            } else if (testCase.isVoiceQualityNB) {
              return (
                <div key={testCase.name} className="report-section">
                  <VoiceQualityNBTable data={testCase.data} testName={testCase.name} />
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
