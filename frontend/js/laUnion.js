async function fetchLaUnionStatistics() {
  try {
    const provinceId = 'P003';

    // Fetch overall top 10 languages
    await fetchTop10Languages(provinceId);

    // Fetch municipalities for the dropdown
    await fetchAllMunicipalities(provinceId);

  } catch (error) {
    console.error('Error fetching statistics:', error);
  }
}

async function fetchTop10Languages(provinceId) {
  try {
    const response = await fetch(`http://127.0.0.1:8000/provincelanguages/top10/${provinceId}`);
    const data = await response.json();

    const overallTableBody = document.querySelector('#overallTable tbody');
    overallTableBody.innerHTML = ''; // Clear existing rows

    if (data.length === 0) {
      const noDataRow = document.createElement('tr');
      noDataRow.innerHTML = `
        <td colspan="2">No data available.</td>
      `;
      overallTableBody.appendChild(noDataRow);
      return;
    }

    // Populate the table with the top 10 languages
    data.forEach(language => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${language.DIALECT_NAME}</td>
        <td>${language.PERCENTAGE}</td>
      `;
      overallTableBody.appendChild(row);
    });
  } catch (error) {
    console.error('Error fetching top 10 languages:', error);
  }
}

async function fetchAllMunicipalities(provinceId) {
  try {
    const response = await fetch(`http://127.0.0.1:8000/municipalities/province/${provinceId}`);
    const data = await response.json();

    const municipalityDropdown = document.querySelector('#municipalityDropdown');
    municipalityDropdown.innerHTML = ''; // Clear existing options

    if (data.length === 0) {
      const noDataOption = document.createElement('option');
      noDataOption.textContent = 'No municipalities available';
      noDataOption.disabled = true;
      municipalityDropdown.appendChild(noDataOption);
      return;
    }

    // Populate dropdown with municipalities
    data.forEach(municipality => {
      const option = document.createElement('option');
      option.value = municipality.MUNICIPALITY_ID; // Use MUNICIPALITY_ID as the value
      option.textContent = municipality.NAME; // Display the NAME field
      municipalityDropdown.appendChild(option);
    });

    // Fetch Top 3 Dialects for the First Municipality
    if (data.length > 0) {
      fetchMunicipalityTop3Dialects(data[0].MUNICIPALITY_ID);
    }
  } catch (error) {
    console.error('Error fetching municipalities:', error);
  }
}

async function fetchMunicipalityTop3Dialects(municipalityId) {
  try {
    const response = await fetch(`http://127.0.0.1:8000/municipalitylanguages/top3/${municipalityId}`);
    const data = await response.json();

    const municipalityTableBody = document.querySelector('#municipalityTable tbody');
    municipalityTableBody.innerHTML = ''; // Clear existing rows

    if (data.length === 0) {
      const noDataRow = document.createElement('tr');
      noDataRow.innerHTML = `
        <td colspan="2">No data available.</td>
      `;
      municipalityTableBody.appendChild(noDataRow);
      return;
    }

    // Populate the table with the top 3 dialects
    data.forEach(language => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${language.DIALECT_NAME}</td>
        <td>${language.percentage}</td>
      `;
      municipalityTableBody.appendChild(row);
    });
  } catch (error) {
    console.error('Error fetching municipality top 3 dialects:', error);
  }
}

async function fetchLaUnionLanguage() {
  const provinceId = 'P003';
  const response = await fetch(`http://127.0.0.1:8000/phrases/comparison/${provinceId}`);
  const data = await response.json();

  const table = document.getElementById('phraseTable');
  const thead = table.querySelector('thead');
  const tbody = table.querySelector('tbody');

  thead.innerHTML = '';
  tbody.innerHTML = '';

  // Step 1: Collect all unique languages
  const languagesSet = new Set();
  data.forEach(row => {
    Object.keys(row.translations).forEach(lang => languagesSet.add(lang));
  });

  const languages = Array.from(languagesSet).sort();

  // Step 2: Create header row
  const headerRow = document.createElement('tr');
  const englishHeader = document.createElement('th');
  englishHeader.textContent = 'English';
  headerRow.appendChild(englishHeader);

  languages.forEach(lang => {
    const th = document.createElement('th');
    th.textContent = lang;
    headerRow.appendChild(th);
  });

  thead.appendChild(headerRow);

  // Step 3: Group data by English phrase
  const groupedData = {};
  data.forEach(row => {
    const englishPhrase = row.english_translation || '';
    if (!groupedData[englishPhrase]) {
      groupedData[englishPhrase] = {};
    }
    Object.keys(row.translations).forEach(lang => {
      groupedData[englishPhrase][lang] = row.translations[lang];
    });
  });

  // Step 4: Create data rows
  Object.keys(groupedData).forEach(englishPhrase => {
    const tr = document.createElement('tr');

    // Add English phrase
    const englishCell = document.createElement('td');
    englishCell.textContent = englishPhrase;
    tr.appendChild(englishCell);

    // Add translations for each language
    languages.forEach(lang => {
      const td = document.createElement('td');
      td.textContent = groupedData[englishPhrase][lang] || ''; // Leave empty if no translation
      tr.appendChild(td);
    });

    tbody.appendChild(tr);
  });
}

async function fetchLaUnionDelicacies() {
  try {
    const provinceId = 'P003';
    const response = await fetch(`http://127.0.0.1:8000/popular/foods/${provinceId}`);

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.json();

    const delicacySection = document.querySelector('#delicacy');
    const delicacyList = delicacySection.querySelector('.delicacy-list');

    delicacyList.innerHTML = ''; // Clear existing list

    if (data.length === 0) {
      const noDataItem = document.createElement('li');
      noDataItem.textContent = 'No delicacies available.';
      delicacyList.appendChild(noDataItem);
      return;
    }

    // Create list items for each delicacy
    data.forEach(item => {
      const listItem = document.createElement('li');
      listItem.textContent = item.NAME;
      delicacyList.appendChild(listItem);
    });

  } catch (error) {
    console.error('Error fetching La Union delicacy data:', error);
  }
}

async function fetchLaUnionTouristSpots() {
  try {
    const provinceId = 'P003';
    const response = await fetch(`http://127.0.0.1:8000/popular/tourist-spots/${provinceId}`);

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.json();

    const touristSection = document.querySelector('#tourist');
    const touristList = touristSection.querySelector('.tourist-list');

    touristList.innerHTML = ''; // Clear existing list

    if (data.length === 0) {
      const noDataItem = document.createElement('li');
      noDataItem.textContent = 'No tourist spots available.';
      touristList.appendChild(noDataItem);
      return;
    }

    // Create list items for each tourist spot
    data.forEach(item => {
      const listItem = document.createElement('li');
      listItem.innerHTML = `
        <div class="tourist-item">
          <div class="tourist-name">${item.NAME}</div>
          <div class="tourist-location">${item.LOCATION}</div>
        </div>
      `;
      touristList.appendChild(listItem);
    });

  } catch (error) {
    console.error('Error fetching La Union tourist spot data:', error);
  }
}