const params = new URLSearchParams(window.location.search);
const movieId = params.get('id');
const contentArea = document.getElementById('movie-content');

if (movieId) {
    fetch(`http://127.0.0.1:5000/movie/${movieId}`)
        .then(response => response.json())
        .then(movie => {
            if (movie.error) {
                contentArea.innerHTML = "<h2>Movie not found!</h2>";
            } else {
                contentArea.innerHTML = `
                    <div style="display: flex; flex-direction: column; gap: 20px; padding: 20px;">
                        <h1 style="color: var(--accent); margin: 0;">${movie.title}</h1>
                        
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                            <p><strong>Year:</strong> ${movie.release_year}</p>
                            <p><strong>Runtime:</strong> ${movie.runtime} min</p>
                            <p><strong>Budget:</strong> $${movie.budget.toLocaleString()}</p>
                            <p><strong>Revenue:</strong> $${movie.revenue.toLocaleString()}</p>
                        </div>

                        <div style="margin-top: 10px;">
                            <h3 style="color: var(--accent);">Overview</h3>
                            <p style="line-height: 1.6; color: var(--text-secondary);">${movie.overview}</p>
                        </div>

                        <button onclick="window.history.back()" class="clear-btn" style="width: fit-content; margin-top: 20px;">
                            ← Go Back
                        </button>
                    </div>
                `;
            }
        })
        .catch(error => {
            console.error("Error:", error);
            contentArea.innerHTML = "<h2>Server Error. Please ensure the backend is running.</h2>";
        });
} else {
    contentArea.innerHTML = "<h2>No movie selected.</h2>";
}
