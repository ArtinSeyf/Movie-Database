import pandas as pd
import sqlite3

# load dataset
movies = pd.read_csv("archive/movies_metadata.csv", low_memory=False)

# keep needed columns
movies = movies[[
    "id",
    "title",
    "overview",
    "release_date",
    "runtime",
    "budget",
    "revenue"
]]

# clean id
movies = movies[pd.to_numeric(movies["id"], errors="coerce").notnull()]
movies["id"] = movies["id"].astype(int)

# extract year
movies["release_year"] = movies["release_date"].str[:4]
movies = movies[pd.to_numeric(movies["release_year"], errors="coerce").notnull()]
movies["release_year"] = movies["release_year"].astype(int)

# clean numbers
movies["budget"] = pd.to_numeric(movies["budget"], errors="coerce").fillna(0).astype(int)
movies["revenue"] = pd.to_numeric(movies["revenue"], errors="coerce").fillna(0).astype(int)
movies["runtime"] = pd.to_numeric(movies["runtime"], errors="coerce").fillna(0).astype(int)

# remove empty titles
movies = movies.dropna(subset=["title"])

# connect database
conn = sqlite3.connect("movies.db")

# clear old data (prevents duplicates)
conn.execute("DELETE FROM movies")

# insert data
movies[[
    "id",
    "title",
    "overview",
    "release_year",
    "runtime",
    "budget",
    "revenue"
]].to_sql("movies", conn, if_exists="append", index=False)

conn.commit()
conn.close()

print("dataset imported")