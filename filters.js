document.getElementById("applyFiltersBtn").addEventListener("click", function () {
    const year = document.getElementById("yearMin").value;

    if (year === "") {
        alert("Please enter a year.");
        return;
    }

    fetch(`http://127.0.0.1:5000/filter/year/${year}`)
        .then(response => response.json())
        .then(data => {
            const container = document.querySelector(".movie-grid");
            container.innerHTML = "";

            if (data.length === 0) {
                container.innerHTML = "<p>No movies found for that year.</p>";
                return;
            }

            data.forEach(movie => {
                const card = document.createElement("div");
                card.classList.add("movie-card");

                card.innerHTML = `
                    <h3>${movie.title}</h3>
                    <p>Year: ${movie.release_date || "N/A"}</p>
                `;

                container.appendChild(card);
            });
        })
        .catch(error => {
            console.error("Error fetching filtered movies:", error);
        });
});
