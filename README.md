**Objective # 1:
**
**ETL Flow
**main.py

This Python script is a data processing pipeline that fetches data from an API, validates and anonymizes it, and 
then stores it in an SQLite database. The script combines multiple modules and functionalities to achieve its objectives, such as data fetching, 
retrying failed requests, data quality checks, anonymization, and database interactions.

Modules and Classes: The script uses several custom modules and classes, including:

1. DataFetcher for retrieving data from an API refer DataFetcherModule.py
2. RetryPolicy for handling retries with exponential backoff in case of request failures refer to RetryModule.py.
3. DataQualityChecker to validate the quality of the fetched data QualityModule.py.
4. DataAnonymizer to anonymize sensitive information before storing it in a database DataAnonymizerModule.py.
5. KeyAuthenticator for authenticating access using keys stored in JSON files KeyAuthenticatorModule.py.
6. QueryDatabase for managing database operations like table creation, checking for existing tables, and inserting data query.py. 
Parameter Loading:
The script begins by loading parameters and authentication details from JSON files (params.json and auth_params.json).
These parameters include the API URL, filtering criteria (like gender and birthday range), and details for data fetching such as maximum records and chunk size.

Data Fetching:

The DataFetcher instance is used to make API requests with specified query parameters.
The RetryPolicy class ensures that API requests are retried up to a specified number of attempts (retries=3) with an increasing delay (backoff_factor=1) between each retry in case of failures.
Data is fetched either in chunks or as a whole based on the parameters, and the fetched records are accumulated until the desired amount (max_records) is reached.
Data Standardization: The standardize_data function flattens nested fields like addresses in the data, making it easier to process and store.

Data Quality and Anonymization:

A DataQualityChecker instance validates the data against required fields (e.g., checking for the presence of an 'email').
The DataAnonymizer class is used to anonymize sensitive fields to protect privacy before saving the data. The annonymiztaion rules are followed as mentioned in the document.

DataAnonymizer_Test.py also executes unit tests for email encryption and masking functions.


Database Operations:

The script initializes a QueryDatabase instance connected to an SQLite database located at the specified path.
It checks if the target table (users) exists. If not, it creates the table using predefined SQL queries.
Finally, the cleaned and anonymized data is inserted into the database.
Authentication:

Authentication is managed by the KeyAuthenticator class, which verifies that the correct keys (admin and database keys) are provided before allowing any database operations.


Key Challenges & Solutions:
1. The API did not support fetching more than 1000 records in one call, so that loop is implemented that checks the unique emails and keeps fetching till the max data size
   is reached which in this case was 10,000. 
2. After anonymizing the email it, the uniqueness of the data could not be verified. So an ecryption is generated to further check the uniquesness of the email, as the API
   does not support any unique parameter.
3. Adding authentication to the database as it was a first time exercise. 

Future Extensions:
1. There must be a monitor class that checks the health of the ETL during the whole flow and stores the metadata i.e ETL duration, records populated, schema evolution etc.
2. The Quality class shouold be extended and further checks should be added. We can extend it to add primary and secondary checks.
3. The Retry class can also have the retries for databasse connection and whole ETL failure retry.

Running the Code: 

To run the code, you will need the keys.json and auth_keys.json files, which contain the database password and encrypted values, respectively.

Please note that these files are not included in the repository to prevent unauthorized access to the database. If you require these files, please contact me via email, and I will provide them to you.

Objective # 2:

Data Summary and Presentation

Report.ipynb

The query in the notebook is gathering some key statistics about users from a database. 
It counts the total number of users, identifies how many are from Germany, and 
how many of those German users use Gmail. It also finds the top three countries where Gmail is most popular and counts the number of Gmail users who are 60 years or older.

Graphs Representation
Gmail Users in Germany (Top-Left Pie Chart): Shows the proportion of Gmail users versus other email users in Germany.

Gmail Users Over 60 (Top-Right Pie Chart): Displays how many Gmail users are aged 60 and above compared to other users.

Top Three Countries Using Gmail (Bottom-Left Bar Chart): Highlights the top three countries with the most Gmail users.

Summary Table (Bottom-Right): Provides a summary of the main statistics, like total users, Gmail users in Germany, and the top countries.

Overall, the graphs and table give a clear picture of how widely Gmail is used among different groups and regions.

Key Challenges:

1. Making graphs using python, something new to learn. 

