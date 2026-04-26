// 1. Get the movie ID from the URL (e.g., movie.html?id=100)
const params = new URLSearchParams(window.location.search);
const movieId = params.get("id");

// 2. Stop the page from breaking if no ID is provided in the URL
if (!movieId) {
    document.getElementById("title").innerText = "No movie selected";
    document.getElementById("overview").innerText = "Please open this page from search results.";
} else {
    // 3. Fetch the specific movie data from the Flask backend [cite: 8, 92]
    fetch(`http://127.0.0.1:5000/movie/${movieId}`)
        .then(response => response.json())
        .then(movie => {
            // 4. Update the HTML elements with the data from the database
            document.getElementById("title").innerText = movie.title || "N/A";
            document.getElementById("year").innerText = movie.release_year || "N/A";
            document.getElementById("runtime").innerText = movie.runtime || "N/A";
            document.getElementById("budget").innerText = movie.budget || "N/A";
            document.getElementById("revenue").innerText = movie.revenue || "N/A";
            document.getElementById("overview").innerText = movie.overview || "No overview available.";
        })
        .catch(error => {
            // 5. Log errors to the Chrome Console for debugging 
            console.error("Error loading movie:", error);
            document.getElementById("title").innerText = "Error loading movie";
            document.getElementById("overview").innerText = "There was a problem loading the movie details.";
        });
}
