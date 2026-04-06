from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("movies.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return "backend running"


# get movies (used for homepage)
@app.route("/movies")
def movies():
    db = get_db()
    rows = db.execute("SELECT id, title FROM movies LIMIT 50").fetchall()
    return jsonify([dict(row) for row in rows])


# get one movie
@app.route("/movie/<id>")
def movie(id):
    db = get_db()
    row = db.execute("SELECT * FROM movies WHERE id = ?", (id,)).fetchone()

    if row:
        return jsonify(dict(row))
    return jsonify({"error": "not found"})


# search by title
@app.route("/search")
def search():
    query = request.args.get("query")

    db = get_db()
    rows = db.execute(
        "SELECT id, title FROM movies WHERE title LIKE ? LIMIT 20",
        ("%" + query + "%",)
    ).fetchall()

    return jsonify([dict(row) for row in rows])


# filter (year, budget, revenue)
@app.route("/filter")
def filter_movies():

    year_min = request.args.get("yearMin")
    year_max = request.args.get("yearMax")

    budget_min = request.args.get("budgetMin")
    budget_max = request.args.get("budgetMax")

    revenue_min = request.args.get("revenueMin")
    revenue_max = request.args.get("revenueMax")

    db = get_db()

    query = "SELECT id, title FROM movies WHERE 1=1"
    params = []

    if year_min:
        query += " AND release_year >= ?"
        params.append(year_min)

    if year_max:
        query += " AND release_year <= ?"
        params.append(year_max)

    if budget_min:
        query += " AND budget >= ?"
        params.append(budget_min)

    if budget_max:
        query += " AND budget <= ?"
        params.append(budget_max)

    if revenue_min:
        query += " AND revenue >= ?"
        params.append(revenue_min)

    if revenue_max:
        query += " AND revenue <= ?"
        params.append(revenue_max)

    rows = db.execute(query, params).fetchall()

    return jsonify([dict(row) for row in rows])


if __name__ == "__main__":
    app.run(debug=True)