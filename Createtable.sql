CREATE TABLE user_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    birthday DATE,
    gender TEXT CHECK(gender IN ('male', 'female')),
    street TEXT,
    streetName TEXT,
    buildingNumber TEXT,
    city TEXT,
    zipcode TEXT,
    country TEXT,
    latitude REAL,
    longitude REAL,
    email_encrypted TEXT
);

CREATE INDEX idx_email_encrypted ON user_info (email_encrypted);
