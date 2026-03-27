# import pandas as pd
#
# movies = pd.read_csv("archive/movies_metadata.csv")
#
# print(movies.columns)
# print(movies.head())
import pandas as pd
import sqlite3

# load dataset
movies = pd.read_csv("movies_metadata.csv", low_memory=False)

# keep only the columns we need
movies = movies[["id", "title", "overview", "release_date", "runtime", "budget", "revenue"]]

# convert release_date to year
movies["release_year"] = movies["release_date"].str[:4]

# remove rows with bad ids
movies = movies[pd.to_numeric(movies["id"], errors="coerce").notnull()]
movies["id"] = movies["id"].astype(int)

# connect to database
conn = sqlite3.connect("movies.db")

# write to database
movies[["id","title","overview","release_year","runtime","budget","revenue"]].to_sql(
    "movies",
    conn,
    if_exists="append",
    index=False
)

print("Dataset imported successfully")