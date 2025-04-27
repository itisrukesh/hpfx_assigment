import unittest
from unittest.mock import patch, MagicMock
from fetchEmail import fetchEmails

class TestFetchEmails(unittest.TestCase):

    @patch('fetchEmail.authenticateGmail')
    @patch('fetchEmail.createEmailsTable')
    @patch('fetchEmail.storeEmailsBulk')
    def test_fetchEmails_WithMock(self, mock_store_bulk, mock_create_table, mock_authenticate_gmail):
        """Test fetchEmails() with mocked Gmail API and store functionality."""

        # Create a fake Gmail service
        fake_service = MagicMock()

        # Mock service.users().messages().list().execute()
        fake_service.users.return_value.messages.return_value.list.return_value.execute.return_value = {
            'messages': [{'id': 'msg1'}, {'id': 'msg2'}]
        }

        # Mock service.users().messages().get().execute()
        def fake_get_message(userId, id, format):
            return {
                'id': id,
                'threadId': f"thread_{id}",
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

        # Mock message.get().execute() per message
        fake_service.users.return_value.messages.return_value.get.side_effect = lambda userId, id, format: MagicMock(
            execute=lambda: fake_get_message(userId, id, format)
        )

        # Make authenticateGmail() return our fake service
        mock_authenticate_gmail.return_value = fake_service

        # Run your fetchEmails function
        fetchEmails(max_res=2)

        # Assert createEmailsTable() was called once
        mock_create_table.assert_called_once()

        # Assert storeEmailsBulk() was called (at least once)
        self.assertTrue(mock_store_bulk.called)

        # Check what was passed to storeEmailsBulk()
        args, kwargs = mock_store_bulk.call_args
        batch = args[0]  # first positional argument is batch

        # We expect 2 emails
        self.assertEqual(len(batch), 2)

        # Check basic fields inside one email tuple
        first_email = batch[0]
        self.assertEqual(first_email[2], 'sender_msg1@example.com')  # sender
        self.assertEqual(first_email[3], 'Subject msg1')  # subject
        self.assertIn('Sat, 26 Apr 2025 10:30:00 +0000', first_email[5])  # received_datetime contains date

if __name__ == '__main__':
    unittest.main()
