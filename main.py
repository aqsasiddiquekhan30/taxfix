import json
import pandas as pd
from DataFetcherModule import DataFetcher
from RetryModule import RetryPolicy
from QualityModule import DataQualityChecker
from DataAnonymizerModule import DataAnonymizer
from AuthModule import KeyAuthenticator
from QueryModule import QueryDatabase

def load_params(file_path):
    """Load parameters from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading parameters: {e}")
        return {}

def standardize_data(data):
    """Standardize and flatten nested address fields in the data."""
    standardized_data = []
    for record in data:
        if 'address' in record and isinstance(record['address'], dict):
            address = record.pop('address')
            record.update({
                'street': address.get('street', ''),
                'streetName': address.get('streetName', ''),
                'buildingNumber': address.get('buildingNumber', ''),
                'city': address.get('city', ''),
                'zipcode': address.get('zipcode', ''),
                'country': address.get('country', ''),
                'latitude': address.get('latitude', ''),
                'longitude': address.get('longitude', '')
            })
        standardized_data.append(record)
    return standardized_data

def main():
    # Load parameters and authentication details
    params = load_params('params.json')
    auth_params = load_params('auth_params.json')

    # Extract parameters
    api_url = params.get('url')
    gender = params.get('gender')
    birthday_start = params.get('birthday_start')
    max_records = params.get('max_records')
    chunk_size = params.get('chunk_size')

    # SQL queries for table creation
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
    create_index = '''
    CREATE INDEX IF NOT EXISTS idx_email_encrypt ON users (email_encrypted);
    '''

    if not api_url:
        raise ValueError("API URL is missing in params.json")

    # Initialize RetryPolicy and DataFetcher
    retry_policy = RetryPolicy(retries=3, backoff_factor=1)
    fetch_params = {
        '_gender': gender,
        '_birthday_start': birthday_start
    }
    data_fetcher = DataFetcher(api_url, fetch_params)

    # Initialize SQLite table creator
    db_path = r'C:\Users\Aqsa khan\taxfixUsers.db'
    table_creator = QueryDatabase(db_path)

    # Fetch data with retries
    data = []
    params.update({'max_records': max_records, 'chunk_size': chunk_size})

    try:
        if max_records and chunk_size:
            while len(data) < max_records:
                records_to_fetch = min(chunk_size, max_records - len(data))
                fetch_params.update({'_quantity': records_to_fetch})
                response = retry_policy.get(api_url, fetch_params)
                if response:
                    chunk_data = response.json().get('data', [])
                    if not chunk_data:
                        print("No more data available.")
                        break
                    data.extend(chunk_data)
                    print(f"Fetched {len(chunk_data)} records, total so far: {len(data)}")
                else:
                    break
        else:
            response = retry_policy.get(api_url, fetch_params)
            if response:
                data = response.json().get('data', [])
                print(f"Fetched {len(data)} records in a single request.")
    
    except Exception as e:
        print(f"Error fetching data: {e}")

    # Validate data quality
    quality_checker = DataQualityChecker()
    required_fields = ['email']
    if data and quality_checker.validate_data(data, required_fields):
        print(f"Total records fetched and validated: {len(data)}")
        # Proceed with anonymization and database insertion
        pd.set_option('display.max_columns', None)
        data = standardize_data(data)
        
        anonymizer = DataAnonymizer()
        anonymized_data = anonymizer.anonymize(data)
        dataframe = pd.DataFrame(anonymized_data)
        clean_data = dataframe.drop(columns=['id', 'website', 'image'], errors='ignore', inplace=False)

        # Initialize the authenticator
        authenticator = KeyAuthenticator('keys.json')
        if authenticator.authenticate_admin(auth_params.get('admin_key')):
            if authenticator.authenticate_database(auth_params.get('database_key')):
                # Check if the table exists, if not, create it
                if not table_creator.table_exists('users'):
                    table_creator.create_table_from_query(create_table_query)
                    table_creator.create_table_from_query(create_index)
                table_creator.insert_data('users', clean_data)
                print(clean_data)
        else:
            print("Authentication failed.")
    else:
        print("Data validation failed or no data available.")

if __name__ == "__main__":
    main()
