const searchBtn = document.getElementById("searchBtn");
const searchInput = document.getElementById("searchInput");
const resultsGrid = document.getElementById("resultsGrid");

function searchMovies() {
    const query = searchInput.value.trim();

    if (query === "") {
        alert("Please enter something to search.");
        return;
    }

    fetch(`http://127.0.0.1:5000/search/${query}`)
        .then(response => response.json())
        .then(data => {

            resultsGrid.innerHTML = "";

            if (data.length === 0) {
                resultsGrid.innerHTML = "<p>No results found.</p>";
                return;
            }

            data.forEach(movie => {

                const card = document.createElement("div");
                card.classList.add("movie-card");

                card.innerHTML = `
                    <h3>${movie.title}</h3>
                    <p>Year: ${movie.release_date || "N/A"}</p>
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