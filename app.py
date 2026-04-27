from flask import Flask, jsonify, request
from flask import send_from_directory

try:
    from flask_cors import CORS
except Exception:
    CORS = None

import sqlite3

# serve static frontend files directly from the project root
app = Flask(__name__, static_folder=".", static_url_path="")

# enable flask-cors if available
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


# serve filters page
@app.route("/Filters.html")
def filters_page():
    return send_from_directory(".", "Filters.html")


# get movies used for homepage
@app.route("/movies")
def movies():
    db = get_db()

    rows = db.execute(
        "SELECT id, title, release_year FROM movies LIMIT 50"
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


# search movies by title
@app.route("/search")
def search():
    query = request.args.get("q")

    if not query:
        return jsonify([])

    db = get_db()

    rows = db.execute(
        "SELECT id, title, release_year FROM movies WHERE title LIKE ? LIMIT 20",
        (f"%{query}%",)
    ).fetchall()

    return jsonify([dict(row) for row in rows])


# filter movies by year, budget and revenue
@app.route("/filter")
def filter_movies():
    year_min = request.args.get("yearMin")
    year_max = request.args.get("yearMax")

    budget_min = request.args.get("budgetMin")
    budget_max = request.args.get("budgetMax")

    revenue_min = request.args.get("revenueMin")
    revenue_max = request.args.get("revenueMax")

    genres = request.args.getlist("genres")

    db = get_db()

    query = "SELECT id, title, release_year, budget, revenue, overview FROM movies WHERE 1=1"
    params = []

    if year_min:
        query += " AND release_year >= ?"
        params.append(int(year_min))

    if year_max:
        query += " AND release_year <= ?"
        params.append(int(year_max))

    if budget_min:
        query += " AND budget >= ?"
        params.append(int(budget_min))

    if budget_max:
        query += " AND budget <= ?"
        params.append(int(budget_max))

    if revenue_min:
        query += " AND revenue >= ?"
        params.append(int(revenue_min))

    if revenue_max:
        query += " AND revenue <= ?"
        params.append(int(revenue_max))

    # simple genre workaround used before proper genre tables were connected
    if genres:
        genre_clauses = []

        for _ in genres:
            genre_clauses.append("(LOWER(title) LIKE ? OR LOWER(overview) LIKE ?)")

        query += " AND (" + " OR ".join(genre_clauses) + ")"

        for g in genres:
            g_param = f"%{g.lower()}%"
            params.append(g_param)
            params.append(g_param)

    try:
        print("FILTER ARGS:", dict(request.args))
        print("SQL:", query)
        print("PARAMS:", params)
    except Exception:
        pass

    rows = db.execute(query, params).fetchall()

    return jsonify([dict(row) for row in rows])


if __name__ == "__main__":
    app.run(debug=False, port=5001)