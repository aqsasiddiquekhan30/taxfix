
# SQL query to create the users table
create_table_query = '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        firstname TEXT NOT NULL,
        lastname TEXT NOT NULL,
        email TEXT NOT NULL,
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
    '''
    
# SQL query to create an index on the email_encrypted column
create_index = '''
    CREATE INDEX IF NOT EXISTS idx_email_encrypt ON users (email_encrypted);
    '''