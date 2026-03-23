-- movies table (main data)
CREATE TABLE movies (
    id INTEGER PRIMARY KEY,
    title TEXT,
    overview TEXT,
    release_year INTEGER,
    runtime INTEGER,
    budget INTEGER,
    revenue INTEGER
);

-- genres table (list of genres)
CREATE TABLE genres (
    id INTEGER PRIMARY KEY,
    name TEXT
);

-- links movies to genres (many to many)
CREATE TABLE movie_genres (
    movie_id INTEGER,
    genre_id INTEGER
);

-- people table (actors & directors)
CREATE TABLE people (
    id INTEGER PRIMARY KEY,
    name TEXT
);

-- links movies to actors
CREATE TABLE movie_cast (
    movie_id INTEGER,
    person_id INTEGER
);

-- links movies to directors
CREATE TABLE movie_directors (
    movie_id INTEGER,
    person_id INTEGER
);