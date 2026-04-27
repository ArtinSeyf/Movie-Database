import pandas as pd
import sqlite3
import ast

# load the kaggle files
movies = pd.read_csv("archive/movies_metadata.csv", low_memory=False)
credits = pd.read_csv("archive/credits.csv", low_memory=False)

# keep only the movie columns we need
movies = movies[
    ["id", "title", "overview", "release_date", "runtime", "budget", "revenue", "genres"]
]

# clean movie id
movies = movies[pd.to_numeric(movies["id"], errors="coerce").notnull()]
movies["id"] = movies["id"].astype(int)

# extract release year
movies["release_year"] = movies["release_date"].str[:4]
movies = movies[pd.to_numeric(movies["release_year"], errors="coerce").notnull()]
movies["release_year"] = movies["release_year"].astype(int)

# clean number fields
movies["budget"] = pd.to_numeric(movies["budget"], errors="coerce").fillna(0).astype(int)
movies["revenue"] = pd.to_numeric(movies["revenue"], errors="coerce").fillna(0).astype(int)
movies["runtime"] = pd.to_numeric(movies["runtime"], errors="coerce").fillna(0).astype(int)

# remove bad titles and duplicate movie ids
movies = movies.dropna(subset=["title"])
movies = movies.drop_duplicates(subset=["id"], keep="first")

# clean credits id
credits = credits[pd.to_numeric(credits["id"], errors="coerce").notnull()]
credits["id"] = credits["id"].astype(int)

# connect to database
conn = sqlite3.connect("movies.db")
cursor = conn.cursor()

# clear old data first
cursor.execute("DELETE FROM movie_directors")
cursor.execute("DELETE FROM movie_cast")
cursor.execute("DELETE FROM movie_genres")
cursor.execute("DELETE FROM people")
cursor.execute("DELETE FROM genres")
cursor.execute("DELETE FROM movies")

# insert main movie data
movies[
    ["id", "title", "overview", "release_year", "runtime", "budget", "revenue"]
].to_sql("movies", conn, if_exists="append", index=False)

# insert genres
for _, row in movies.iterrows():
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
                    (row["id"], genre_id)
                )
    except:
        pass

# insert cast and directors
for _, row in credits.iterrows():
    movie_id = row["id"]

    try:
        cast_list = ast.literal_eval(row["cast"])

        # only use top 10 cast members
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