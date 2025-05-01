# tests/test_save_emails.py

import unittest
import json
import sqlite3
from db import storeEmailsBulk,TableQuery

class TestSaveEmailsBulk(unittest.TestCase):

    def setUp(self):
        """Set up in-memory SQLite DB and create emails table."""
        # Connect to an in-memory database (fast and clean)
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.cursor.execute(TableQuery.createEmails_Table())
        self.conn.commit()

    def tearDown(self):
        """Close DB connection after each test."""
        self.conn.close()

    def test_storeEmailsBulk(self):
        """Test saving multiple email records in bulk."""
        # Prepare fake emails matching EMAIL_FIELDS order
        with open('tests\list_emails.json', 'r', encoding='utf-8') as f:
            email_json_list = json.load(f)
            
        sample_emails = []
        for email in email_json_list:
            sample_emails.append((
                email['id'],
                email['thread_id'],
                email['sender'],
                email['subject'],
                email['snippet'],
                email['received_datetime'],
                email['label_ids']
            ))

        # Patch the get_db_connection() method in save_emails to use our in-memory DB
        original_get_db_connection = storeEmailsBulk.__globals__['getDbConnection']
        storeEmailsBulk.__globals__['getDbConnection'] = lambda: self.conn

        try:
            storeEmailsBulk(sample_emails)
            
            # Verify that records were inserted
            self.cursor.execute("SELECT COUNT(*) FROM emails;")
            count = self.cursor.fetchone()[0]
            self.assertEqual(count, len(sample_emails))

            # Optionally verify content
            self.cursor.execute(f"SELECT * FROM emails WHERE id = '{sample_emails[0][0]}';")
            record = self.cursor.fetchone()
            self.assertIsNotNone(record)
            self.assertEqual(record[2], "Reddit <noreply@redditmail.com>")  # sender
            self.assertEqual(record[3], "\"One thala getting traumatised of the other o...\"")  # subject

        finally:
            # Restore the original function
            storeEmailsBulk.__globals__['getDbConnection'] = original_get_db_connection

if __name__ == '__main__':
    unittest.main()
