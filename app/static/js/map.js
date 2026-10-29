
document.addEventListener("DOMContentLoaded", function () {
    const mapElement = document.getElementById("heritage-map");

    // Stop if this script is loaded on a page without the map.
    if (!mapElement || typeof L === "undefined") {
        return;
    }

    // Approximate coordinates: latitude, longitude.
    const sites = {
        lalibela: {
            name: "Lalibela",
            coordinates: [12.0319, 39.0419],
            description: "Famous for its medieval rock-hewn churches.",
            url: "/sites/lalibela"
        },
        aksum: {
            name: "Aksum",
            coordinates: [14.1300, 38.7200],
            description: "The center of an ancient Ethiopian kingdom.",
            url: "/sites/aksum"
        },
        gondar: {
            name: "Gondar",
            coordinates: [12.6030, 37.4520],
            description: "Home to the historic Fasil Ghebbi royal complex.",
            url: "/sites/gondar"
        },  
        harar: {
            name: "Harar Jugol",
            coordinates: [9.3117, 42.1270],
            description: "A historic fortified town in eastern Ethiopia.",
            url: "/sites/harar"
        },
        tiya: {
            name: "Tiya",
            coordinates: [8.4333, 38.6167],
            description: "An archaeological site known for carved stone monuments.",
            url: "/sites/tiya"
        }

    };

    // Start the map centered on Ethiopia.
    const map = L.map("heritage-map").setView([9.5, 40.0], 5.5);

    // Add the OpenStreetMap background.
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 18,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    const markers = {};

    // Create a marker and popup for each historical site.
    Object.entries(sites).forEach(function ([key, site]) {
        const marker = L.marker(site.coordinates).addTo(map);

        const popupContent = document.createElement("div");
        const heading = document.createElement("strong");
        const description = document.createElement("p");
        const link = document.createElement("a");

        heading.textContent = site.name;
        description.textContent = site.description;
        link.textContent = "View site details";
        link.href = site.url;

        popupContent.append(heading, description, link);
        marker.bindPopup(popupContent);

        markers[key] = marker;
    });

    // Let visitors locate a site using its card button.
    document.querySelectorAll("[data-site]").forEach(function (button) {
        button.addEventListener("click", function () {
            const siteKey = button.dataset.site;
            const marker = markers[siteKey];

            if (marker) {
                map.flyTo(marker.getLatLng(), 10);
                marker.openPopup();
            }
        });
    });
});
