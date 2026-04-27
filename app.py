from flask import Flask, jsonify, request
from flask import send_from_directory
import sqlite3

try:
    from flask_cors import CORS
except Exception:
    CORS = None


# serve frontend files directly from the project root
app = Flask(__name__, static_folder=".", static_url_path="")

# enable CORS if flask_cors is installed
if CORS:
    CORS(app)


# connect to database
def get_db():
    conn = sqlite3.connect("movies.db")
    conn.row_factory = sqlite3.Row
    return conn


# fallback CORS headers for local development
@app.after_request
def add_cors_headers(response):
    response.headers.setdefault("Access-Control-Allow-Origin", "*")
    response.headers.setdefault("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.setdefault("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    return response


# simple test route
@app.route("/")
def home():
    return "backend running"


# serve main frontend pages
@app.route("/Home.html")
def home_page():
    return send_from_directory(".", "Home.html")


@app.route("/Filters.html")
def filters_page():
    return send_from_directory(".", "Filters.html")


@app.route("/search.html")
def search_page():
    return send_from_directory(".", "search.html")


@app.route("/movie.html")
def movie_page():
    return send_from_directory(".", "movie.html")


@app.route("/TopRated.html")
def top_rated_page():
    return send_from_directory(".", "TopRated.html")


# get movies used for browsing/homepage
@app.route("/movies")
def movies():
    db = get_db()

    rows = db.execute(
        "SELECT id, title, release_year FROM movies LIMIT 100"
    ).fetchall()

    return jsonify([dict(row) for row in rows])


# get one movie by id
@app.route("/movie/<int:id>")
def movie(id):
    db = get_db()

    row = db.execute(
        "SELECT * FROM movies WHERE id = ?",
        (id,)
    ).fetchone()

    if row:
        return jsonify(dict(row))

    return jsonify({"error": "not found"})


# get genres for one movie
@app.route("/movie/<int:id>/genres")
def movie_genres(id):
    db = get_db()

    rows = db.execute("""
        SELECT genres.name
        FROM genres
        JOIN movie_genres ON genres.id = movie_genres.genre_id
        WHERE movie_genres.movie_id = ?
    """, (id,)).fetchall()

    return jsonify([dict(row) for row in rows])


# get cast for one movie
@app.route("/movie/<int:id>/cast")
def movie_cast(id):
    db = get_db()

    rows = db.execute("""
        SELECT people.name
        FROM people
        JOIN movie_cast ON people.id = movie_cast.person_id
        WHERE movie_cast.movie_id = ?
        LIMIT 10
    """, (id,)).fetchall()

    return jsonify([dict(row) for row in rows])


# get director for one movie
@app.route("/movie/<int:id>/director")
def movie_director(id):
    db = get_db()

    rows = db.execute("""
        SELECT people.name
        FROM people
        JOIN movie_directors ON people.id = movie_directors.person_id
        WHERE movie_directors.movie_id = ?
    """, (id,)).fetchall()

    return jsonify([dict(row) for row in rows])


# search movies by title, actor or director
@app.route("/search")
def search():
    query = request.args.get("q", "")
    search_type = request.args.get("type", "title")

    if not query:
        return jsonify([])

    db = get_db()
    search_value = f"%{query}%"

    if search_type == "actor":
        rows = db.execute("""
            SELECT DISTINCT movies.id, movies.title, movies.release_year
            FROM movies
            JOIN movie_cast ON movies.id = movie_cast.movie_id
            JOIN people ON movie_cast.person_id = people.id
            WHERE people.name LIKE ?
            LIMIT 50
        """, (search_value,)).fetchall()

    elif search_type == "director":
        rows = db.execute("""
            SELECT DISTINCT movies.id, movies.title, movies.release_year
            FROM movies
            JOIN movie_directors ON movies.id = movie_directors.movie_id
            JOIN people ON movie_directors.person_id = people.id
            WHERE people.name LIKE ?
            LIMIT 50
        """, (search_value,)).fetchall()

    else:
        rows = db.execute("""
            SELECT id, title, release_year
            FROM movies
            WHERE title LIKE ?
            LIMIT 50
        """, (search_value,)).fetchall()

    return jsonify([dict(row) for row in rows])


# filter movies by year, budget, revenue, genre, actor and director
@app.route("/filter")
def filter_movies():
    year_min = request.args.get("yearMin")
    year_max = request.args.get("yearMax")

    budget_min = request.args.get("budgetMin")
    budget_max = request.args.get("budgetMax")

    revenue_min = request.args.get("revenueMin")
    revenue_max = request.args.get("revenueMax")

    genres = request.args.getlist("genres")
    actor = request.args.get("actor")
    director = request.args.get("director")

    db = get_db()

    query = """
        SELECT DISTINCT movies.id, movies.title, movies.release_year,
                        movies.budget, movies.revenue, movies.overview
        FROM movies
        WHERE 1=1
    """

    params = []

    if year_min:
        query += " AND movies.release_year >= ?"
        params.append(int(year_min))

    if year_max:
        query += " AND movies.release_year <= ?"
        params.append(int(year_max))

    if budget_min:
        query += " AND movies.budget >= ?"
        params.append(int(budget_min))

    if budget_max:
        query += " AND movies.budget <= ?"
        params.append(int(budget_max))

    if revenue_min:
        query += " AND movies.revenue >= ?"
        params.append(int(revenue_min))

    if revenue_max:
        query += " AND movies.revenue <= ?"
        params.append(int(revenue_max))

    if genres:
        placeholders = ",".join(["?"] * len(genres))

        query += f"""
            AND movies.id IN (
                SELECT movie_genres.movie_id
                FROM movie_genres
                JOIN genres ON movie_genres.genre_id = genres.id
                WHERE genres.name IN ({placeholders})
            )
        """

        params.extend(genres)

    if actor:
        query += """
            AND movies.id IN (
                SELECT movie_cast.movie_id
                FROM movie_cast
                JOIN people ON movie_cast.person_id = people.id
                WHERE people.name LIKE ?
            )
        """
        params.append(f"%{actor}%")

    if director:
        query += """
            AND movies.id IN (
                SELECT movie_directors.movie_id
                FROM movie_directors
                JOIN people ON movie_directors.person_id = people.id
                WHERE people.name LIKE ?
            )
        """
        params.append(f"%{director}%")

    query += " LIMIT 100"

    rows = db.execute(query, params).fetchall()

    return jsonify([dict(row) for row in rows])


if __name__ == "__main__":
    app.run(debug=False, port=5001)