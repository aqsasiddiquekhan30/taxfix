import json

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
