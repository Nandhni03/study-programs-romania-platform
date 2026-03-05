// Initialize map centered on Timisoara
const map = L.map('map').setView([45.7537, 21.2257], 13);

// OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Fetch programs from backend API
fetch('/programs')
  .then(res => res.json())
  .then(data => {
    data.forEach(prog => {
      // Default location if missing
      const lat = prog.lat || 45.7537;
      const lng = prog.lng || 21.2257;

      const marker = L.marker([lat, lng]).addTo(map);

      const popupContent = `
        <b>${prog.program}</b><br/>
        Faculty: ${prog.faculty}<br/>
        Degree: ${prog.degree}<br/>
        Language: ${prog.language}<br/>
        <a href="${prog.url}" target="_blank">More info</a>
      `;
      marker.bindPopup(popupContent);
    });
  })
  .catch(err => console.error("Failed to load programs:", err));