(() => {
    function init() {
        const scroll = document.querySelector('.ScrollMovies'); // may be null on some pages
        const leftArrow = document.querySelector('.LeftArrow');
        const rightArrow = document.querySelector('.RightArrow');

        const scrollAmount = 400; // how far it will scroll

        // Only wire arrow handlers when both arrow and scroll container exist
        if (rightArrow && scroll) {
            rightArrow.addEventListener('click', () => {
                scroll.scrollBy({ left: scrollAmount, behavior: 'smooth' });
            });
        }
        if (leftArrow && scroll) {
            leftArrow.addEventListener('click', () => {
                scroll.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
            });
        }

        // Make poster images clickable and fetch movie id via backend search
        const posters = document.querySelectorAll('.home-poster');
        posters.forEach(p => {
            p.style.cursor = 'pointer';
            p.addEventListener('click', () => {
                const title = p.dataset.title;
                if (!title) return;
                // backend on localhost:5001 (use hostname fallback)
                const backend = `http://${location.hostname || 'localhost'}:5001`;
                fetch(`${backend}/search?q=${encodeURIComponent(title)}`)
                    .then(r => r.json())
                    .then(results => {
                        if (!Array.isArray(results) || results.length === 0) {
                            alert('Movie not found in database.');
                            return;
                        }
                        const movie = results[0];
                        window.location.href = `movie.html?id=${movie.id}`;
                    })
                    .catch(() => alert('Could not reach backend.'));
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();