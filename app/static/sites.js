document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("site-search");
    const categoryFilter = document.getElementById("category-filter");
    const siteCards = document.querySelectorAll(".site-card");
    const noResults = document.getElementById("no-results");

    function filterSites() {
        const searchText = searchInput.value.toLowerCase().trim();
        const selectedCategory = categoryFilter.value;

        let visibleCount = 0;

        siteCards.forEach(function (card) {
            const siteName = card.querySelector("h3").textContent.toLowerCase();
            const siteDescription = card.querySelector("p").textContent.toLowerCase();
            const siteCategory = card.dataset.category;

            const matchesSearch =
                siteName.includes(searchText) ||
                siteDescription.includes(searchText);

            const matchesCategory =
                selectedCategory === "all" ||
                siteCategory === selectedCategory;

            if (matchesSearch && matchesCategory) {
                card.style.display = "";
                visibleCount++;
            } else {
                card.style.display = "none";
            }
        });
        
        noResults.style.display = visibleCount === 0 ? "block" : "none";
    }

    searchInput.addEventListener("input", filterSites);
    categoryFilter.addEventListener("change", filterSites);
});

