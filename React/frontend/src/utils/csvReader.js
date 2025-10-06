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
            if (row.PC2 !== undefined && row.PC2 !== null) {
              pc2Data.push({ x: index + 1, y: row.PC2 });
            }
            if (row.PC3 !== undefined && row.PC3 !== null) {
              pc3Data.push({ x: index + 1, y: row.PC3 });
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
    console.error(`Error fetching or parsing CSV for Run${runNumber}:`, error);
    return { pc2: [], pc3: [] };
  }
};
