import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class RetryPolicy:
    def __init__(self, retries=3, backoff_factor=1):
        self.session = requests.Session()
        self.retries = retries
        self.backoff_factor = backoff_factor
        self.setup_retry()

    def setup_retry(self):
        """Configure retry strategy for the session."""
        retry_strategy = Retry(
            total=self.retries,
            backoff_factor=self.backoff_factor,
            allowed_methods=["GET"]  # Retry only GET requests
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def get(self, url, params=None):
        """Make a GET request with retry logic."""
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response
        except requests.RequestException as error:
            print(f"Error fetching data: {error}")
            return None
