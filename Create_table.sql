CREATE TABLE imdb_reviews (
    id SERIAL PRIMARY KEY,
    review_text TEXT NOT NULL,
    sentiment TEXT NOT NULL
);
