import pandas as pd
import sqlite3
import ast

# load the kaggle dataset
movies = pd.read_csv("archive/movies_metadata.csv", low_memory=False)

# load extra movie genre data separately so the original movie import stays simple
movie_genres_data = pd.read_csv(
    "archive/movies_metadata.csv",
    usecols=["id", "genres"],
    low_memory=False
)

# try loading credits.csv for cast and director data
try:
    credits = pd.read_csv("archive/credits.csv", low_memory=False)
except FileNotFoundError:
    credits = None
    print("credits.csv not found, cast and director data will not be imported")

# keep only the columns we actually need for the movies table
movies = movies[
    ["id", "title", "overview", "release_date", "runtime", "budget", "revenue"]
]

# remove rows where id is not a number
movies = movies[pd.to_numeric(movies["id"], errors="coerce").notnull()]
movies["id"] = movies["id"].astype(int)

# extract year from release_date
movies["release_year"] = movies["release_date"].str[:4]

# remove rows where year is invalid
movies = movies[pd.to_numeric(movies["release_year"], errors="coerce").notnull()]
movies["release_year"] = movies["release_year"].astype(int)

# convert numeric fields and replace bad values with 0
movies["budget"] = pd.to_numeric(movies["budget"], errors="coerce").fillna(0).astype(int)
movies["revenue"] = pd.to_numeric(movies["revenue"], errors="coerce").fillna(0).astype(int)
movies["runtime"] = pd.to_numeric(movies["runtime"], errors="coerce").fillna(0).astype(int)

# remove movies with no title
movies = movies.dropna(subset=["title"])

# remove duplicate movie IDs
movies = movies.drop_duplicates(subset=["id"], keep="first")

# connect to database
conn = sqlite3.connect("movies.db")
cursor = conn.cursor()

# make sure the extra tables exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS genres (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS movie_genres (
        movie_id INTEGER,
        genre_id INTEGER,
        PRIMARY KEY (movie_id, genre_id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS movie_cast (
        movie_id INTEGER,
        person_id INTEGER,
        PRIMARY KEY (movie_id, person_id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS movie_directors (
        movie_id INTEGER,
        person_id INTEGER,
        PRIMARY KEY (movie_id, person_id)
    )
""")

# clear movie table first so we do not duplicate movie data when re-running
conn.execute("DELETE FROM movies")

# insert cleaned movie data into database
movies[
    ["id", "title", "overview", "release_year", "runtime", "budget", "revenue"]
].to_sql("movies", conn, if_exists="append", index=False)

# clean genre data ids
movie_genres_data = movie_genres_data[
    pd.to_numeric(movie_genres_data["id"], errors="coerce").notnull()
]
movie_genres_data["id"] = movie_genres_data["id"].astype(int)

# insert genres from the Kaggle genres column
for _, row in movie_genres_data.iterrows():
    movie_id = row["id"]

    try:
        genre_list = ast.literal_eval(row["genres"])

        for genre in genre_list:
            genre_id = genre.get("id")
            genre_name = genre.get("name")

            if genre_id and genre_name:
                cursor.execute(
                    "INSERT OR IGNORE INTO genres (id, name) VALUES (?, ?)",
                    (genre_id, genre_name)
                )

                cursor.execute(
                    "INSERT OR IGNORE INTO movie_genres (movie_id, genre_id) VALUES (?, ?)",
                    (movie_id, genre_id)
                )

    except:
        pass

# insert cast and director data if credits.csv exists
if credits is not None:
    credits = credits[pd.to_numeric(credits["id"], errors="coerce").notnull()]
    credits["id"] = credits["id"].astype(int)

    for _, row in credits.iterrows():
        movie_id = row["id"]

        # cast column contains actors
        try:
            cast_list = ast.literal_eval(row["cast"])

            # only keep the first 10 actors to keep it simple
            for actor in cast_list[:10]:
                person_id = actor.get("id")
                name = actor.get("name")

                if person_id and name:
                    cursor.execute(
                        "INSERT OR IGNORE INTO people (id, name) VALUES (?, ?)",
                        (person_id, name)
                    )

                    cursor.execute(
                        "INSERT OR IGNORE INTO movie_cast (movie_id, person_id) VALUES (?, ?)",
                        (movie_id, person_id)
                    )

        except:
            pass

        # crew column contains directors
        try:
            crew_list = ast.literal_eval(row["crew"])

            for crew_member in crew_list:
                if crew_member.get("job") == "Director":
                    person_id = crew_member.get("id")
                    name = crew_member.get("name")

                    if person_id and name:
                        cursor.execute(
                            "INSERT OR IGNORE INTO people (id, name) VALUES (?, ?)",
                            (person_id, name)
                        )

                        cursor.execute(
                            "INSERT OR IGNORE INTO movie_directors (movie_id, person_id) VALUES (?, ?)",
                            (movie_id, person_id)
                        )

        except:
            pass

conn.commit()
conn.close()

print("dataset imported successfully")