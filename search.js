const searchBtn = document.getElementById("searchBtn");
const searchInput = document.getElementById("searchInput");
const resultsGrid = document.getElementById("resultsGrid");

function searchMovies() {
    const query = searchInput.value.trim();

    if (query === "") {
        alert("Please enter something to search.");
        return;
    }

    // backend runs on port 5001; use hostname fallback for file:// cases
    const backendPort = 5001;
    const host = location.hostname || 'localhost';
    const url = `http://${host}:${backendPort}/search?q=${encodeURIComponent(query)}`;
    console.log('Searching URL:', url);

    fetch(url)
        .then(response => response.json())
        .then(data => {

            resultsGrid.innerHTML = "";

            if (!data || data.length === 0) {
                resultsGrid.innerHTML = "<p>No results found.</p>";
                return;
            }

            data.forEach(movie => {

                const card = document.createElement("div");
                card.classList.add("movie-card");

                card.innerHTML = `
                    <h3>${movie.title}</h3>
                    <p>Year: ${movie.release_year || "N/A"}</p>
                `;

                resultsGrid.appendChild(card);

            });
        })
        .catch(error => {
            console.error("Search error:", error);
        });
}

searchBtn.addEventListener("click", searchMovies);

searchInput.addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        searchMovies();
    }
});
