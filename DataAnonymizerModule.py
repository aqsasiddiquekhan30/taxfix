from cryptography.fernet import Fernet
from datetime import datetime

class DataAnonymizer:
    def __init__(self, encryption_key=None):
        # Generate a key if none is provided
        self.key = encryption_key or Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def anonymize(self, data):
        """Anonymize a list of records according to specified rules."""
        for record in data:
            # Mask identifiable fields except city
            self.mask_identifiable_info(record)
            # Generalize birthdate to age group
            self.generalize_birthdate(record)
            # Simplify email to domain only with partial masking
            self.simplify_email(record)
            # Encrypt email
            if 'email' in record:
                record['email_encrypted'] = self.encrypt_email(record['email'])
                record['email'] = self.masked_email(record['email'])  # Mask the email but keep the domain
        return data

    def encrypt_email(self, email):
        """Encrypt the email address."""
        return self.cipher.encrypt(email.encode()).decode()

    def decrypt_email(self, encrypted_email):
        """Decrypt the email address."""
        return self.cipher.decrypt(encrypted_email.encode()).decode()

    def masked_email(self, email):
        """Mask the local part of the email, keep the domain visible."""
        email_parts = email.split('@')
        if len(email_parts) == 2:
            local_part, domain = email_parts
            return f"****@{domain}"
        return "****"

    def mask_identifiable_info(self, record):
        """Partially mask user-identifiable fields except city."""
        if 'firstname' in record:
            record['firstname'] = self.partial_mask(record['firstname'])
        if 'lastname' in record:
            record['lastname'] = self.partial_mask(record['lastname'])
        if 'phone' in record:
            record['phone'] = self.partial_mask_phone(record['phone'])
        if 'street' in record:
            record['street'] = self.partial_mask(record.get('street', ''))
        if 'zipcode' in record:
            record['zipcode'] = self.partial_mask_zipcode(record.get('zipcode', ''))
        if 'latitude' in record:
            record['latitude'] = "****"
        if 'longitude' in record:
            record['longitude'] = "****"
        if 'buildingNumber' in record:
            record['buildingNumber'] = "****"
        if 'streetName' in record:
            record['streetName'] = self.partial_mask(record['streetName'])

    def partial_mask(self, value):
        """Partially mask a string, showing only the first character."""
        if not isinstance(value, str) or not value:
            return "****"
        return value[0] + "***"

    def partial_mask_phone(self, phone):
        """Partially mask a phone number, showing only the last 3 digits."""
        if not isinstance(phone, str) or len(phone) < 3:
            return "****"
        return '*' * (len(phone) - 3) + phone[-3:]

    def partial_mask_zipcode(self, zipcode):
        """Partially mask a zipcode, showing only the first digit."""
        if not isinstance(zipcode, str) or len(zipcode) < 1:
            return "****"
        return zipcode[0] + "****"

    def generalize_birthdate(self, record):
        """Generalize birthdate to a ten-year age group."""
        if 'birthday' in record and record['birthday']:
            try:
                birth_year = datetime.strptime(record['birthday'], "%Y-%m-%d").year
                current_year = datetime.now().year
                age = current_year - birth_year
                age_group = f"[{(age // 10) * 10}-{((age // 10) * 10) + 10}]"
                record['birthday'] = age_group
            except ValueError:
                record['birthday'] = "Unknown"

    def simplify_email(self, record):
        """Simplify email to domain only with partial masking."""
        if 'email' in record and record['email']:
            email_parts = record['email'].split('@')
            if len(email_parts) == 2:
                domain = email_parts[1]
                record['email'] = f"****@{domain}"
            else:
                record['email'] = "****"
