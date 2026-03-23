import pandas as pd

movies = pd.read_csv("archive/movies_metadata.csv")

print(movies.columns)
print(movies.head())