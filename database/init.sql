CREATE TABLE fbi_wanted (
    uid SERIAL PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    url VARCHAR(255),
    reward_text VARCHAR(255),
    poster_url VARCHAR(255),
    subjects VARCHAR(255),
    publication VARCHAR(255),
    nationality VARCHAR(255),
    hair VARCHAR(255),
    eyes VARCHAR(255),
    height VARCHAR(255),
    weight VARCHAR(255),
    sex VARCHAR(255),
    scars_and_marks TEXT,
    remarks TEXT
);
