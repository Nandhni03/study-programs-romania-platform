// Initialize map centered on Timisoara
const map = L.map('map').setView([45.75, 21.23], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

const sidebar = document.getElementById('sidebar');

// Load programs JSON
fetch('/data/uvt_programs_raw.json')
  .then(res => res.json())
  .then(programs => {

    // Single marker for Timisoara
    const marker = L.marker([45.75, 21.23]).addTo(map);
    marker.bindPopup("Click to see all UVT programs");

    marker.on('click', () => {
      sidebar.classList.toggle('active');

      // Clear old cards except header
      sidebar.querySelectorAll('.program-card').forEach(c => c.remove());

      programs.forEach(prog => {
        const card = document.createElement('div');
        card.className = 'program-card';
        card.innerHTML = `
          <h4>${prog.title}</h4>
          <p>${prog.faculty || ''}</p>
          <div class="details">
            ${prog.link ? `<p><a href="${prog.link}" target="_blank">Program link</a></p>` : ''}
            ${prog.phone ? `<p>Phone: ${prog.phone}</p>` : ''}
            ${prog.email ? `<p>Email: ${prog.email}</p>` : ''}
          </div>
          <span class="see-more">See more</span>
        `;
        sidebar.appendChild(card);

        // Toggle details
        const seeMore = card.querySelector('.see-more');
        seeMore.addEventListener('click', () => card.classList.toggle('active'));
      });
    });

  })
  .catch(err => console.error(err));