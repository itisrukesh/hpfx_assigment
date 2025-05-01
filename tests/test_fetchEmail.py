import unittest
from unittest.mock import patch, MagicMock
from fetchEmail import fetchAndStoreEmails_from_Gmail

class TestFetchAndStoreEmails(unittest.TestCase):

    @patch('fetchEmail.storeEmailsBulk')
    def test_fetchAndStoreEmails_from_Gmail_with_mocked_service(self, mock_store_bulk):
        # Create a mock Gmail service
        fake_service = MagicMock()

        # Simulate messages().list().execute() returning 2 email message IDs
        fake_service.users.return_value.messages.return_value.list.return_value.execute.return_value = {
            'messages': [{'id': 'msg1'}, {'id': 'msg2'}]
        }

        # Simulate messages().get().execute() returning email details
        def fake_get_message(userId, id, format):
            return {
                'id': id,
                'threadId': f'thread_{id}',
                'payload': {
                    'headers': [
                        {'name': 'From', 'value': f'sender_{id}@example.com'},
                        {'name': 'Subject', 'value': f'Subject {id}'},
                        {'name': 'Date', 'value': 'Sat, 26 Apr 2025 10:30:00 +0000'}
                    ]
                },
                'snippet': f'Snippet for {id}',
                'labelIds': ['INBOX', 'IMPORTANT']
            }

        # Patch get().execute() calls to use fake_get_message
        fake_service.users.return_value.messages.return_value.get.side_effect = lambda userId, id, format: MagicMock(
            execute=lambda: fake_get_message(userId, id, format)
        )

        # Run the fetch + store function with mocked service
        fetchAndStoreEmails_from_Gmail(fake_service, max_res=2)

        # Assert that storeEmailsBulk() was called
        self.assertTrue(mock_store_bulk.called)

        # Grab the arguments passed to storeEmailsBulk
        all_calls = mock_store_bulk.call_args_list
        all_emails = []
        for call in all_calls:
            args, _ = call
            all_emails.extend(args[0])  # append each batch's emails

        # Expect 2 emails in total
        self.assertEqual(len(all_emails), 2)

        # Check structure of first email
        first_email = all_emails[0]
        self.assertEqual(first_email[2], 'sender_msg1@example.com')     # sender
        self.assertEqual(first_email[3], 'Subject msg1')                # subject
        self.assertIn('Sat, 26 Apr 2025 10:30:00 +0000', first_email[5])  # received_datetime

if __name__ == '__main__':
    unittest.main()
