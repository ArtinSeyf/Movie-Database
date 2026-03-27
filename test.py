from flask import Flask, jsonify, request
import sqlite3
from flask_cors import CORS

# create the app
app = Flask(__name__)
CORS(app)

# Database connection function
def get_db():
    conn = sqlite3.connect("movies.db")
    conn.row_factory = sqlite3.Row  # lets you convert rows to dicts
    return conn

# test route to see if server is working
@app.route("/")
def home():
    return "Backend is running"

# route to get all movies
@app.route("/movies")
def movies():
    db = get_db()
    rows = db.execute("SELECT * FROM movies").fetchall()
    return jsonify([dict(r) for r in rows])

# route for filtering movies with multiple criteria
@app.route("/filter")
def filter_movies():
    # get values from URL
    year_min = request.args.get("yearMin")
    year_max = request.args.get("yearMax")
    budget_min = request.args.get("budgetMin")
    budget_max = request.args.get("budgetMax")
    revenue_min = request.args.get("revenueMin")
    revenue_max = request.args.get("revenueMax")

    db = get_db()

    # Start building the query
    query = "SELECT * FROM movies WHERE 1=1"
    params = []

    # Add filters if they exist
    if year_min:
        query += " AND CAST(SUBSTR(release_year) AS INTEGER) >= ?"
        params.append(int(year_min))
    if year_max:
        query += " AND CAST(SUBSTR(release_year) AS INTEGER) <= ?"
        params.append(int(year_max))
    if budget_min:
        query += " AND budget >= ?"
        params.append(float(budget_min))
    if budget_max:
        query += " AND budget <= ?"
        params.append(float(budget_max))
    if revenue_min:
        query += " AND revenue >= ?"
        params.append(float(revenue_min))
    if revenue_max:
        query += " AND revenue <= ?"
        params.append(float(revenue_max))

    rows = db.execute(query, params).fetchall()
    return jsonify([dict(r) for r in rows])

# route to filter by specific year
@app.route("/filter/year/<int:year>")
def filter_year(year):
    db = get_db()
    rows = db.execute(
        "SELECT * FROM movies WHERE SUBSTR(release_date, 1, 4) = ?",
        (str(year),)
    ).fetchall()
    return jsonify([dict(r) for r in rows])

# route to search movies by title or people
@app.route("/search")
def search_movies():
    query = request.args.get("q", "").strip()

    if query == "":
        return jsonify([])

    db = get_db()
    query_param = f"%{query}%"

    rows = db.execute("""
        SELECT id, title, release_year
        FROM movies
        WHERE title LIKE ?
    """, (query_param,)).fetchall()

    return jsonify([dict(r) for r in rows])# runs app

if __name__ == "__main__":
    app.run(debug=True)