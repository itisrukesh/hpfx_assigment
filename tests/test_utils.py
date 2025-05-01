# tests/test_utils.py

import unittest
import json
from utils import BuildEmailRecord
from db import TableQuery

class TestBuildEmailRecord(unittest.TestCase):

    def setUp(self):
        """Load sample email data from JSON file."""
        with open('tests/single_email.json', 'r') as f:
            self.sample_email_data = json.load(f)

        # Convert JSON to a mock Gmail message format
        self.sample_msg_detail = {
            'id': self.sample_email_data['id'],
            'threadId': self.sample_email_data['thread_id'],
            'payload': {
                'headers': [
                    {'name': 'From', 'value': self.sample_email_data['sender']},
                    {'name': 'Subject', 'value': self.sample_email_data['subject']},
                    {'name': 'Date', 'value': self.sample_email_data['received_datetime']}
                ]
            },
            'snippet': self.sample_email_data['snippet'],
            'labelIds': self.sample_email_data['label_ids'].split(',')
        }

    def test_BuildEmailRecord(self):
        """Test if build_email_record correctly maps fields and order."""
        record = BuildEmailRecord(self.sample_msg_detail)

        self.assertIsInstance(record, tuple)
        self.assertEqual(len(record), len(TableQuery.EMAIL_FIELDS))

        record_dict = dict(zip(TableQuery.EMAIL_FIELDS.keys(), record))

        # Now validate from real sample
        self.assertEqual(record_dict['id'], self.sample_email_data['id'])
        self.assertEqual(record_dict['thread_id'], self.sample_email_data['thread_id'])
        self.assertEqual(record_dict['sender'], self.sample_email_data['sender'])
        self.assertEqual(record_dict['subject'], self.sample_email_data['subject'])
        self.assertEqual(record_dict['snippet'], self.sample_email_data['snippet'])
        self.assertEqual(record_dict['received_datetime'], self.sample_email_data['received_datetime'])
        self.assertEqual(record_dict['label_ids'], self.sample_email_data['label_ids'])

if __name__ == '__main__':
    unittest.main()
