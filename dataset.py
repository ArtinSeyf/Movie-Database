import pandas as pd
import sqlite3

# load the kaggle dataset
movies = pd.read_csv("archive/movies_metadata.csv", low_memory=False)

# keep only the columns we actually need
movies = movies[
    ["id", "title", "overview", "release_date", "runtime", "budget", "revenue"]
]

# ---- clean the data ----

# remove rows where id is not a number
movies = movies[pd.to_numeric(movies["id"], errors="coerce").notnull()]
movies["id"] = movies["id"].astype(int)

# extract year from release_date (first 4 characters)
movies["release_year"] = movies["release_date"].str[:4]

# remove rows where year is invalid
movies = movies[pd.to_numeric(movies["release_year"], errors="coerce").notnull()]
movies["release_year"] = movies["release_year"].astype(int)

# convert numeric fields (replace bad values with 0)
movies["budget"] = pd.to_numeric(movies["budget"], errors="coerce").fillna(0).astype(int)
movies["revenue"] = pd.to_numeric(movies["revenue"], errors="coerce").fillna(0).astype(int)
movies["runtime"] = pd.to_numeric(movies["runtime"], errors="coerce").fillna(0).astype(int)

# remove movies with no title
movies = movies.dropna(subset=["title"])


# ---- insert into database ----

conn = sqlite3.connect("movies.db")

# clear table first so we don't duplicate data when re-running
conn.execute("DELETE FROM movies")

# insert cleaned data into database
movies[
    ["id", "title", "overview", "release_year", "runtime", "budget", "revenue"]
].to_sql("movies", conn, if_exists="append", index=False)

conn.commit()
conn.close()

print("dataset imported successfully")