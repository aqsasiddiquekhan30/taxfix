import sqlite3
from db.schema import create_index, create_table_query

class QueryDatabase:
    def __init__(self, db_name):
        self.db_name = db_name

    def create_table_from_query(self, create_table_query):
        """Creates a table using a provided SQL CREATE TABLE query."""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(create_table_query)
            conn.commit()
            print("Table created successfully using provided SQL query.")
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
        finally:
            conn.close()

    def insert_data(self, table_name, dataframe):
        """Inserts data from a DataFrame into the specified table."""
        if not self.table_exists(table_name):
            print(f"Table '{table_name}' does not exist. Data insertion aborted.")
            return

        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Get columns from DataFrame, excluding the auto-increment column 'id'
            columns = [col for col in dataframe.columns if col != 'id']
            placeholders = ', '.join(['?'] * len(columns))
            insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            
            # Convert DataFrame to list of tuples
            data_tuples = [
                tuple(row[col] for col in columns)
                for _, row in dataframe.iterrows()
                if not self.email_exists(table_name, row['email_encrypted'])
            ]

            if data_tuples:
                # Use executemany for bulk insert
                cursor.executemany(insert_query, data_tuples)
                conn.commit()
                print(f"Data inserted into table '{table_name}' successfully.")
            else:
                print("No new data to insert.")
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
        finally:
            conn.close()


    def email_exists(self, table_name, email_encrypted):
        """Checks if an encrypted email already exists in the table."""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            query = f"SELECT COUNT(*) FROM {table_name} WHERE email_encrypted = ?;"
            cursor.execute(query, (email_encrypted,))
            result = cursor.fetchone()
            return result[0] > 0
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            conn.close()
            return False

    def get_last_id(self, table_name):
        """Gets the last ID from the table if available."""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(f"SELECT MAX(id) FROM {table_name};")
            last_id = cursor.fetchone()[0]
            return last_id if last_id is not None else 0
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return None
        finally:
            conn.close()

    def table_exists(self, table_name):
        """Checks if a table exists in the database."""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
            exists = cursor.fetchone() is not None
            return exists
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False
        finally:
            conn.close()

    def create_database_table(self):
        """Create the users table and index in the database if they do not exist."""
        self.create_table_from_query(create_table_query)
        self.create_table_from_query(create_index)