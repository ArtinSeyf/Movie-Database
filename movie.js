const backendPort = 5001;
const host = location.hostname || "localhost";
const BACKEND = `http://${host}:${backendPort}`;

const params = new URLSearchParams(window.location.search);
const movieId = params.get("id");

function showLoading() {
    document.getElementById("loadingState").style.display = "block";
    document.getElementById("errorState").style.display = "none";
    document.getElementById("movieDetail").style.display = "none";
    document.getElementById("fallbackSearch").style.display = "none";
}

function showError(msg) {
    document.getElementById("loadingState").style.display = "none";
    document.getElementById("errorState").style.display = "block";
    document.getElementById("movieDetail").style.display = "none";
    document.getElementById("fallbackSearch").style.display = "none";
    document.getElementById("errorMsg").innerText = msg || "We couldn't load this movie.";
}

function showMovie() {
    document.getElementById("loadingState").style.display = "none";
    document.getElementById("errorState").style.display = "none";
    document.getElementById("movieDetail").style.display = "block";
    document.getElementById("fallbackSearch").style.display = "none";
}

function showFallback() {
    document.getElementById("loadingState").style.display = "none";
    document.getElementById("errorState").style.display = "none";
    document.getElementById("movieDetail").style.display = "none";
    document.getElementById("fallbackSearch").style.display = "block";
}

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

function loadMovie(id) {
    showLoading();

    console.log("Loading movie ID:", id);
    console.log("Backend:", BACKEND);

    fetch(`${BACKEND}/movie/${id}`)
        .then(res => {
            if (!res.ok) {
                throw new Error("Movie route failed");
            }
            return res.json();
        })
        .then(data => {
            console.log("Movie data:", data);

            if (data.error) {
                showError("This movie does not exist in the database.");
                return;
            }

            document.title = `${data.title || "Movie"} - MovieHub`;

            document.getElementById("movieTitle").innerText = data.title || "N/A";
            document.getElementById("movieOverview").innerText = data.overview || "No overview available.";
            document.getElementById("movieYear").innerText = data.release_year || "N/A";
            document.getElementById("movieRuntime").innerText = formatRuntime(data.runtime);
            document.getElementById("movieBudget").innerText = formatMoney(data.budget);
            document.getElementById("movieRevenue").innerText = formatMoney(data.revenue);

            showMovie();

            loadGenres(id);
            loadDirector(id);
            loadCast(id);
        })
        .catch(error => {
            console.error("Movie loading error:", error);
            showError("Could not load movie data. Make sure Flask is running on port 5001.");
        });
}

function loadGenres(id) {
    const container = document.getElementById("movieGenres");

    fetch(`${BACKEND}/movie/${id}/genres`)
        .then(res => res.json())
        .then(data => {
            console.log("Genre data:", data);

            if (!Array.isArray(data) || data.length === 0) {
                container.innerHTML = "<span class='genre-tag'>No genre data</span>";
                return;
            }

            container.innerHTML = data
                .map(genre => `<span class="genre-tag">${genre.name}</span>`)
                .join("");
        })
        .catch(error => {
            console.error("Genre loading error:", error);
            container.innerHTML = "<span class='genre-tag'>No genre data</span>";
        });
}

function loadDirector(id) {
    const directorElement = document.getElementById("movieDirector");

    fetch(`${BACKEND}/movie/${id}/director`)
        .then(res => res.json())
        .then(data => {
            console.log("Director data:", data);

            if (!Array.isArray(data) || data.length === 0) {
                directorElement.innerText = "No director data";
                return;
            }

            directorElement.innerText = data
                .map(director => director.name)
                .join(", ");
        })
        .catch(error => {
            console.error("Director loading error:", error);
            directorElement.innerText = "No director data";
        });
}

function loadCast(id) {
    const container = document.getElementById("movieCast");

    fetch(`${BACKEND}/movie/${id}/cast`)
        .then(res => res.json())
        .then(data => {
            console.log("Cast data:", data);

            if (!Array.isArray(data) || data.length === 0) {
                container.innerHTML = "<span class='cast-member'>No cast data</span>";
                return;
            }

            container.innerHTML = data
                .map(actor => `<span class="cast-member">${actor.name}</span>`)
                .join("");
        })
        .catch(error => {
            console.error("Cast loading error:", error);
            container.innerHTML = "<span class='cast-member'>No cast data</span>";
        });
}

function setupFallbackSearch() {
    showFallback();

    const input = document.getElementById("manualInput");
    const list = document.getElementById("manualResults");

    input.addEventListener("input", function () {
        const q = input.value.trim();

        if (q.length < 2) {
            list.innerHTML = "";
            return;
        }

        fetch(`${BACKEND}/search?q=${encodeURIComponent(q)}`)
            .then(res => res.json())
            .then(data => {
                list.innerHTML = "";

                if (!Array.isArray(data) || data.length === 0) {
                    list.innerHTML = "<li class='no-results'>No results found.</li>";
                    return;
                }

                data.forEach(movie => {
                    const li = document.createElement("li");
                    li.innerText = `${movie.title} (${movie.release_year || "N/A"})`;

                    li.addEventListener("click", function () {
                        history.pushState({}, "", `?id=${movie.id}`);
                        loadMovie(movie.id);
                    });

                    list.appendChild(li);
                });
            })
            .catch(error => {
                console.error("Fallback search error:", error);
                list.innerHTML = "<li class='no-results'>Could not reach server.</li>";
            });
    });
}

if (movieId) {
    loadMovie(movieId);
} else {
    setupFallbackSearch();
}