import unittest
from auth import authenticate_gmail

class TestGmailAuth(unittest.TestCase):
    def test_authenticate_gmail_service(self):
        """Test if Gmail service is authenticated and working."""
        service = authenticate_gmail()
        self.assertIsNotNone(service, "Failed to authenticate and build Gmail service.")
        
        # Check if we can get the user's email address
        profile = service.users().getProfile(userId='me').execute()
        self.assertIn('emailAddress', profile, "Email address not found in profile response.")
        
if __name__ == '__main__':
    unittest.main()