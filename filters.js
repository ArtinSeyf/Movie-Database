document.addEventListener("DOMContentLoaded", function () {
    const applyBtn = document.getElementById("applyFiltersBtn");
    const clearBtn = document.getElementById("clearFiltersBtn");
    const container = document.querySelector(".movie-grid");

    // Helper to clear results area
    function clearResults() {
        if (container) container.innerHTML = "";
    }

    // Apply filters / search
    if (applyBtn) {
        applyBtn.addEventListener("click", function () {
            const yearMin = document.getElementById("yearMin").value;
            const yearMax = document.getElementById("yearMax").value;

            if (yearMin === "" && yearMax === "") {
                alert("Please enter a minimum or maximum year.");
                return;
            }

            // clear previous results while fetching
            clearResults();

            // Determine backend URL. Live Server usually serves the frontend on a
            // different port, so construct a backend host on the same machine.
            // Update backendPort if your Flask app runs on a different port.
            const backendPort = 5001; // <-- keep in sync with app.py
            const backendBase = `http://${location.hostname}:${backendPort}`;

            // Build query params depending on which fields are present
            const params = [];
            if (yearMin !== "") params.push(`yearMin=${encodeURIComponent(yearMin)}`);
            if (yearMax !== "") params.push(`yearMax=${encodeURIComponent(yearMax)}`);

            const url = `${backendBase}/filter?${params.join("&")}`;

            fetch(url)
                .then(response => response.json())
                .then(data => {
                    if (!container) return;

                    if (!Array.isArray(data) || data.length === 0) {
                        container.innerHTML = "<p>No movies found for that year.</p>";
                        return;
                    }

                    data.forEach(movie => {
                        const card = document.createElement("div");
                        card.classList.add("movie-card");

                        card.innerHTML = `
                            <h3>${movie.title}</h3>
                            <p>Year: ${movie.release_year || "N/A"}</p>
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
