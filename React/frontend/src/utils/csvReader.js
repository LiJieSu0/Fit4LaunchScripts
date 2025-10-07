import Papa from 'papaparse'; // Assuming papaparse is installed or will be installed

export const fetchAndParseRsrpData = async (runNumber) => {
  const filePath = `/rsrp_data/Run${runNumber}_PC2_PC3_RSRP_Analysis.csv`;
  try {
    const response = await fetch(filePath);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const csvText = await response.text();

    return new Promise((resolve, reject) => {
      Papa.parse(csvText, {
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true,
        complete: (results) => {
          const pc2Data = [];
          const pc3Data = [];
          results.data.forEach((row, index) => {
            // Ensure data is numeric and not null/undefined before pushing
            const pc2Value = parseFloat(row.PC2);
            const pc3Value = parseFloat(row.PC3);

            if (!isNaN(pc2Value) && pc2Value !== null) {
              pc2Data.push({ x: index + 1, y: pc2Value });
            }
            if (!isNaN(pc3Value) && pc3Value !== null) {
              pc3Data.push({ x: index + 1, y: pc3Value });
            }
          });
          resolve({ pc2: pc2Data, pc3: pc3Data });
        },
        error: (error) => {
          reject(error);
        },
      });
    });
  } catch (error) {
    console.error(`Error fetching or parsing RSRP CSV for Run${runNumber}:`, error);
    return { pc2: [], pc3: [] };
  }
};

export const fetchAndParseTxPowerData = async (runNumber) => {
  const filePath = `/tx_power_data/Run${runNumber}_PC2_PC3_TxPower_Analysis.csv`;
  try {
    const response = await fetch(filePath);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const csvText = await response.text();

    return new Promise((resolve, reject) => {
      Papa.parse(csvText, {
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true,
        complete: (results) => {
          const pc2Data = [];
          const pc3Data = [];
          results.data.forEach((row, index) => {
            // Ensure data is numeric and not null/undefined before pushing
            const pc2Value = parseFloat(row.PC2);
            const pc3Value = parseFloat(row.PC3);

            if (!isNaN(pc2Value) && pc2Value !== null) {
              pc2Data.push({ x: index + 1, y: pc2Value });
            }
            if (!isNaN(pc3Value) && pc3Value !== null) {
              pc3Data.push({ x: index + 1, y: pc3Value });
            }
          });
          resolve({ pc2: pc2Data, pc3: pc3Data });
        },
        error: (error) => {
          reject(error);
        },
      });
    });
  } catch (error) {
    console.error(`Error fetching or parsing Tx Power CSV for Run${runNumber}:`, error);
    return { pc2: [], pc3: [] };
  }
};
