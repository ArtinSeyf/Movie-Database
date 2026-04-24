document.addEventListener("DOMContentLoaded", function () {
    const applyBtn = document.getElementById("applyFiltersBtn");
    const clearBtn = document.getElementById("clearFiltersBtn");
    const container = document.querySelector(".movie-grid");
    const resultsSubtitle = document.querySelector('.results-subtitle');

    // Helper to clear results area
    function clearResults() {
        if (container) container.innerHTML = "";
    }

    // Apply filters / search
    if (applyBtn) {
        applyBtn.addEventListener("click", function () {
            const yearMin = document.getElementById("yearMin").value;
            const yearMax = document.getElementById("yearMax").value;

            // collect budget & revenue
            const budgetMin = document.getElementById("budgetMin").value;
            const budgetMax = document.getElementById("budgetMax").value;

            const revenueMin = document.getElementById("revenueMin").value;
            const revenueMax = document.getElementById("revenueMax").value;

            // collect selected genres
            const checkedGenres = Array.from(document.querySelectorAll('.checkbox-group input[type="checkbox"]:checked')).map(cb => cb.value);

            // require at least one filter (not just year)
            if (yearMin === "" && yearMax === "" && budgetMin === "" && budgetMax === "" && revenueMin === "" && revenueMax === "" && checkedGenres.length === 0) {
                alert("Please enter at least one filter.");
                return;
            }

            // clear previous results while fetching
            clearResults();

            // Determine backend URL. Live Server usually serves the frontend on a
            // different port, so construct a backend host on the same machine.
            // Update backendPort if your Flask app runs on a different port.
            const backendPort = 5001; // <-- keep in sync with app.py
            // When opening the HTML file directly (file://...) location.hostname is empty.
            // Fall back to localhost so the fetch still targets the local Flask server.
            const host = location.hostname || 'localhost';
            const backendBase = `http://${host}:${backendPort}`;

            // Build query params depending on which fields are present
            const params = [];
            if (yearMin !== "") params.push(`yearMin=${encodeURIComponent(yearMin)}`);
            if (yearMax !== "") params.push(`yearMax=${encodeURIComponent(yearMax)}`);

            if (budgetMin !== "") params.push(`budgetMin=${encodeURIComponent(budgetMin)}`);
            if (budgetMax !== "") params.push(`budgetMax=${encodeURIComponent(budgetMax)}`);

            if (revenueMin !== "") params.push(`revenueMin=${encodeURIComponent(revenueMin)}`);
            if (revenueMax !== "") params.push(`revenueMax=${encodeURIComponent(revenueMax)}`);

            // pass genres as repeated query params, e.g. ?genres=Action&genres=Comedy
            checkedGenres.forEach(g => params.push(`genres=${encodeURIComponent(g)}`));

            const url = `${backendBase}/filter?${params.join("&")}`;

            console.log('Fetching URL:', url);
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    console.log('Filter response:', data);
                    if (resultsSubtitle) {
                        resultsSubtitle.textContent = `Showing ${Array.isArray(data)?data.length:0} results`;
                    }
                    console.log('Filter response:', data);
                    if (!container) return;

                    if (!Array.isArray(data) || data.length === 0) {
                        container.innerHTML = "<p>No movies matched those filters.</p>";
                        return;
                    }

                    // show currently applied filters for clarity
                    const activeFilters = [];
                    if (yearMin) activeFilters.push(`Year: ${yearMin || ''}-${yearMax || ''}`);
                    if (budgetMin || budgetMax) activeFilters.push(`Budget: ${budgetMin || ''}-${budgetMax || ''}`);
                    if (revenueMin || revenueMax) activeFilters.push(`Revenue: ${revenueMin || ''}-${revenueMax || ''}`);
                    if (checkedGenres.length) activeFilters.push(`Genres: ${checkedGenres.join(', ')}`);
                    if (resultsSubtitle && activeFilters.length) {
                        resultsSubtitle.textContent += ' — ' + activeFilters.join(' | ');
                    }

                    data.forEach(movie => {
                        const card = document.createElement("div");
                        card.classList.add("movie-card");

                        card.innerHTML = `
                            <h3>${movie.title}</h3>
                            <p>Year: ${movie.release_year || "N/A"}</p>
                            <p>Budget: ${movie.budget || "N/A"} — Revenue: ${movie.revenue || "N/A"}</p>
                        `;

                        container.appendChild(card);
                    });
                })
                .catch(error => {
                    console.error("Error fetching filtered movies:", error);
                    if (container) container.innerHTML = "<p>Error retrieving results. See console for details.</p>";
                });
        });
    }

    // Clear filters
    if (clearBtn) {
        clearBtn.addEventListener("click", function () {
            // Clear number inputs
            const numberInputs = document.querySelectorAll('input[type="number"]');
            numberInputs.forEach(i => i.value = "");

            // Uncheck any checkboxes in the filters area
            const checkboxes = document.querySelectorAll('.checkbox-group input[type="checkbox"]');
            checkboxes.forEach(cb => cb.checked = false);

            // Clear results area
            clearResults();
        });
    }
});
