(function () {
    const app = window.sanskritiSetu;
    const map = L.map('map', {
        zoomControl: false,
        scrollWheelZoom: true,
        doubleClickZoom: true,
        touchZoom: true,
        boxZoom: true,
        keyboard: true,
        minZoom: 3,
        maxZoom: 18
    }).setView([20.5937, 78.9629], 4);
    const heritageMarkers = new Map();
    const heritageSites = window.heritageSites || [];

    L.control.zoom({ position: 'topright' }).addTo(map);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    function showSiteDetails(site) {
        const details = document.getElementById('mapHeritageDetails');
        const heritage = app.findHeritageEntry(site.query);
        details.innerHTML = `
            <div class="map-detail-image" style="background-image: url('${heritage ? heritage.image : ''}')" role="img" aria-label="${site.name}"></div>
            <div class="map-detail-content">
                <span class="eyebrow">Selected heritage</span>
                <h3>${site.name}</h3>
                <p>${heritage ? heritage.detail : site.detail}</p>
                <div class="map-detail-meta">
                    <span><b>Region</b>${heritage ? heritage.region : site.type}</span>
                    <span><b>Period</b>${heritage ? heritage.era : 'Living heritage'}</span>
                </div>
                <span class="map-detail-type">${site.type}</span>
                ${site.sourceUrl ? `<a class="map-source-link" href="${site.sourceUrl}" target="_blank" rel="noopener noreferrer">Open ${site.sourceLabel || 'online reference'} <span aria-hidden="true">↗</span></a>` : ''}
            </div>
        `;
        app.updateHeritageView(site.query);
    }

    heritageSites.forEach(site => {
        const marker = L.marker([site.lat, site.lng]).addTo(map);
        heritageMarkers.set(site.name, marker);
        marker.bindPopup(`
            <strong>${site.name}</strong>
            <span class="map-popup-type">${site.type}</span>
            <span>${site.detail}</span>
        `);
        marker.on('click', () => showSiteDetails(site));
    });

    function searchHeritageOnMap() {
        const input = document.getElementById('mapHeritageSearchInput');
        const query = input.value.trim();
        if (!query) return;

        const searchWords = app.normalizeQuery(query).split(' ').filter(Boolean);
        const site = heritageSites.find(entry => {
            const searchableText = app.normalizeQuery(`${entry.name} ${entry.type}`);
            return searchWords.every(word => searchableText.includes(word));
        });

        if (!site) {
            document.getElementById('mapHeritageDetails').innerHTML = `
                <span class="eyebrow">Place not found</span>
                <p>Try a name such as Victoria, Bishnupur, Darjeeling, Sundarbans, or Konark.</p>
            `;
            return;
        }

        map.setView([site.lat, site.lng], 8, { animate: true });
        heritageMarkers.get(site.name).fire('click');
        input.value = site.name;
    }

    document.getElementById('mapHeritageSearchBtn').addEventListener('click', searchHeritageOnMap);
    document.getElementById('mapHeritageSearchInput').addEventListener('keydown', event => {
        if (event.key === 'Enter') searchHeritageOnMap();
    });

    app.setupHeritageAutocomplete('mapHeritageSearchInput', 'mapHeritageSuggestions', suggestion => {
        const site = heritageSites.find(entry => entry.name === suggestion.title);
        if (site) {
            map.setView([site.lat, site.lng], 8, { animate: true });
            heritageMarkers.get(site.name).fire('click');
        }
    });
})();
