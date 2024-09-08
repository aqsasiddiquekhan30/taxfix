class DataQualityChecker:
    @staticmethod
    def validate_data(data, required_fields):
        """Check that required fields are present in all records."""
        if not all(all(field in record for field in required_fields) for record in data):
            print("Data quality issue: Missing required fields in some records.")
            return False
        return True
