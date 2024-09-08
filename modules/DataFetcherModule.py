import requests

class DataFetcher:
    def __init__(self, url, params):
        self.url = url
        self.params = params

    def fetch_data(self):
        """Fetch data from the API."""
        try:
            response = requests.get(self.url, params=self.params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json().get('data', [])  # Get 'data' from the JSON response
            print(f"Fetched {len(data)} records in a single request.")
            return data
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return []

