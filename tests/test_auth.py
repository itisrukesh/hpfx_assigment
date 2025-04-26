import unittest
from auth import authenticateGmail

class TestGmailAuth(unittest.TestCase):
    def testAuthenticateGmailService(self):
        """Test if Gmail service is authenticated and working."""
        service = authenticateGmail()
        self.assertIsNotNone(service, "Failed to authenticate and build Gmail service.")
        
        # Check if we can get the user's email address
        profile = service.users().getProfile(userId='me').execute()
        self.assertIn('emailAddress', profile, "Email address not found in profile response.")
        
if __name__ == '__main__':
    unittest.main()