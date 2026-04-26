const BACKEND = "http://127.0.0.1:5001";
 
const params = new URLSearchParams(window.location.search);
const movieId = params.get("id");
 
// --- State helpers ---
function showLoading() {
    document.getElementById("loadingState").style.display = "block";
    document.getElementById("errorState").style.display = "none";
    document.getElementById("movieDetail").style.display = "none";
    document.getElementById("fallbackSearch").style.display = "none";
}
 
function showError(msg) {
    document.getElementById("loadingState").style.display = "none";
    document.getElementById("errorState").style.display = "block";
    document.getElementById("errorMsg").innerText = msg || "We couldn't load this movie.";
}
 
function showMovie() {
    document.getElementById("loadingState").style.display = "none";
    document.getElementById("movieDetail").style.display = "block";
}
 
function showFallback() {
    document.getElementById("loadingState").style.display = "none";
    document.getElementById("fallbackSearch").style.display = "block";
}
 
// --- Format helpers ---
function formatMoney(val) {
    if (!val || val === 0) return "N/A";
    return "$" + Number(val).toLocaleString();
}
 
function formatRuntime(val) {
    if (!val || val === 0) return "N/A";
    const h = Math.floor(val / 60);
    const m = val % 60;
    return h > 0 ? `${h}h ${m}m` : `${m}m`;
}
 
// --- Load core movie data ---
function loadMovie(id) {
    showLoading();
    fetch(`${BACKEND}/movie/${id}`)
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                showError("This movie doesn't exist in our database.");
                return;
            }
 
            document.title = `${data.title} - MovieHub`;
            document.getElementById("movieTitle").innerText = data.title;
            document.getElementById("movieOverview").innerText = data.overview || "No overview available.";
            document.getElementById("movieYear").innerText = data.release_year || "—";
            document.getElementById("movieRuntime").innerText = formatRuntime(data.runtime);
            document.getElementById("movieBudget").innerText = formatMoney(data.budget);
            document.getElementById("movieRevenue").innerText = formatMoney(data.revenue);
 
            showMovie();
 
            // Load additional data (these endpoints may not exist yet)
            loadGenres(id);
            loadDirector(id);
            loadCast(id);
        })
        .catch(() => showError("Could not connect to the server. Make sure the backend is running."));
}
 
// --- Load genres ---
function loadGenres(id) {
    fetch(`${BACKEND}/movie/${id}/genres`)
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById("movieGenres");
            if (!Array.isArray(data) || data.length === 0) return;
            container.innerHTML = data
                .map(g => `<span class="genre-tag">${g.name}</span>`)
                .join("");
        })
        .catch(() => {}); // silently fail until backend route exists
}
 
// --- Load director ---
function loadDirector(id) {
    fetch(`${BACKEND}/movie/${id}/director`)
        .then(res => res.json())
        .then(data => {
            const el = document.getElementById("movieDirector");
            if (!Array.isArray(data) || data.length === 0) return;
            el.innerText = data.map(d => d.name).join(", ");
        })
        .catch(() => {}); // silently fail until backend route exists
}
 
// --- Load cast ---
function loadCast(id) {
    fetch(`${BACKEND}/movie/${id}/cast`)
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById("movieCast");
            if (!Array.isArray(data) || data.length === 0) return;
            container.innerHTML = data
                .map(p => `<span class="cast-member">${p.name}</span>`)
                .join("");
        })
        .catch(() => {}); // silently fail until backend route exists
}
 
// --- Fallback search ---
function setupFallbackSearch() {
    showFallback();
    const input = document.getElementById("manualInput");
    const list = document.getElementById("manualResults");
 
    input.addEventListener("input", () => {
        const q = input.value.trim();
        if (q.length < 2) {
            list.innerHTML = "";
            return;
        }
        fetch(`${BACKEND}/search?q=${encodeURIComponent(q)}`)
            .then(res => res.json())
            .then(data => {
                list.innerHTML = "";
                if (!data.length) {
                    list.innerHTML = "<li class='no-results'>No results found.</li>";
                    return;
                }
                data.forEach(m => {
                    const li = document.createElement("li");
                    li.innerText = `${m.title} (${m.release_year})`;
                    li.onclick = () => {
                        // Update URL without reload so back button works
                        history.pushState({}, "", `?id=${m.id}`);
                        loadMovie(m.id);
                    };
                    list.appendChild(li);
                });
            })
            .catch(() => {
                list.innerHTML = "<li class='no-results'>Could not reach server.</li>";
            });
    });
}
 
// --- Init ---
if (movieId) {
    loadMovie(movieId);
} else {
    setupFallbackSearch();
}
