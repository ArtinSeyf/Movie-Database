-- create main movies table
CREATE TABLE movies (
    id INTEGER PRIMARY KEY,
    title TEXT,
    overview TEXT,
    release_year INTEGER,
    runtime INTEGER,
    budget INTEGER,
    revenue INTEGER
);

-- create genres table
CREATE TABLE genres (
    id INTEGER PRIMARY KEY,
    name TEXT
);

-- link movies to genres (many-to-many)
CREATE TABLE movie_genres (
    movie_id INTEGER,
    genre_id INTEGER,
    PRIMARY KEY (movie_id, genre_id)
);

-- create people table (actors + directors)
CREATE TABLE people (
    id INTEGER PRIMARY KEY,
    name TEXT
);

-- link movies to actors
CREATE TABLE movie_cast (
    movie_id INTEGER,
    person_id INTEGER,
    PRIMARY KEY (movie_id, person_id)
);

-- link movies to directors
CREATE TABLE movie_directors (
    movie_id INTEGER,
    person_id INTEGER,
    PRIMARY KEY (movie_id, person_id)
);