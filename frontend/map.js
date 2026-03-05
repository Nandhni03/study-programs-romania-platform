// map.js
const map = L.map('map').setView([45.75, 21.23], 13); // Timisoara center

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Sidebar container
const sidebar = document.getElementById('sidebar');

// Fetch UVT programs JSON
fetch('/data/uvt_programs_raw.json')
  .then(res => res.json())
  .then(programs => {
    // Add a marker for Timisoara
    const marker = L.marker([45.75, 21.23]).addTo(map);
    marker.bindPopup("Click to see UVT programs");

    marker.on('click', () => {
      // Show sidebar
      sidebar.classList.add('active');

      // Clear existing cards except header
      sidebar.querySelectorAll('.program-card').forEach(el => el.remove());

      programs.forEach(prog => {
        const card = document.createElement('div');
        card.className = 'program-card';

        const title = prog.program || "No title";
        const faculty = prog.faculty || "";
        const url = prog.url || "#"; // <-- use the correct URL from JSON

        // Card content
        card.innerHTML = `
          <h4>${title}</h4>
          <p>${faculty}</p>
          <p><a href="${url}" target="_blank" class="program-link">Go to program page</a></p>
        `;

        sidebar.appendChild(card);
      });
    });
  })
  .catch(err => console.error(err));