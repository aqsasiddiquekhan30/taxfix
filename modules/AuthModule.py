import os
import json
import bcrypt

class KeyAuthenticator:
    def __init__(self, config_file):
        self.config_file = config_file
        self.keys = self.load_keys()

    def load_keys(self):
        """Load keys from the configuration file."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as file:
                    return json.load(file)
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error reading from config file: {e}")
        return {}

    def generate_hash(self, key):
        """Generate a bcrypt hash for a given key."""
        salt = bcrypt.gensalt()
        hashed_key = bcrypt.hashpw(key.encode(), salt)
        return hashed_key.decode()

    def set_keys(self, admin_key, database_key):
        """Hash and store the admin and database keys."""
        self.keys['admin_key'] = self.generate_hash(admin_key)
        self.keys['database_key'] = self.generate_hash(database_key)
        self.save_keys()

    def save_keys(self):
        """Save the hashed keys to the configuration file."""
        try:
            with open(self.config_file, 'w') as file:
                json.dump(self.keys, file, indent=4)
        except IOError as e:
            print(f"Error writing to config file: {e}")

    def verify_key(self, provided_key, stored_hash):
        """Verify a provided key against the stored hash."""
        return bcrypt.checkpw(provided_key.encode(), stored_hash.encode())

    def authenticate_admin(self, provided_key):
        """Authenticate using the admin key provided."""
        stored_hash = self.keys.get('admin_key')
        if provided_key and stored_hash and self.verify_key(provided_key, stored_hash):
            print("Admin authentication successful.")
            return True
        else:
            print("Admin authentication failed.")
            return False

    def authenticate_database(self, provided_key):
        """Authenticate using the database key provided."""
        stored_hash = self.keys.get('database_key')
        if provided_key and stored_hash and self.verify_key(provided_key, stored_hash):
            print("Database authentication successful.")
            return True
        else:
            print("Database authentication failed.")
            return False
