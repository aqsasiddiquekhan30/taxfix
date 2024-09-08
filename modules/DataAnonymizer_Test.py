import unittest
import DataAnonymizerModule as DA


# Test for DataAnonymizer
class Test_Data_Anonymizer(unittest.TestCase):

    def setUp(self):
        # Initialize the DataAnonymizer instance
        self.da = DA.DataAnonymizer()
    
    def test_encrypt_decrypt_email(self):
        original_email = "test@gmail.com"
        encrypted_email = self.da.encrypt_email(original_email)
        
        # Ensure encryption produces a different result than the original email
        self.assertNotEqual(original_email, encrypted_email)
        
        decrypted_email = self.da.decrypt_email(encrypted_email)
        
        # Test that decrypting the encrypted email returns the original email
        self.assertEqual(original_email, decrypted_email)     
    
    def test_encrypt_email(self):
        original_email = "test@gmail.com"
        encrypted_email = self.da.encrypt_email(original_email)
        
        # Test that encryption returns a non-empty value
        self.assertIsNotNone(encrypted_email)
        self.assertNotEqual(original_email, encrypted_email)
        
        
    def test_masked_email(self):
        original_email = "test@gmail.com"
        masked_email = self.da.masked_email(original_email)  
        self.assertEqual("****@gmail.com", masked_email) 
        
# Run the tests when the script is executed
if __name__ == '__main__':
    unittest.main()
