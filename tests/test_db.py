# tests/test_db.py

import unittest
import os
import sqlite3
from db import getDbConnection, createEmailsTable, TableQuery

class TestDatabaseOperations(unittest.TestCase):

    def test_CreateEmailsTable(self):
        """Test if emails table can be created without errors."""        
        conn = getDbConnection()
        cursor = conn.cursor()
        # Drop table first if exists for clean test
        cursor.execute("DROP TABLE IF EXISTS emails;")
        conn.commit()

        # Run table creation
        createEmailsTable()

        # Now check if 'emails' table exists
        cursor.execute("""
            SELECT name FROM sqlite_master WHERE type='table' AND name='emails';
        """)
        table = cursor.fetchone()
        self.assertIsNotNone(table, "Emails table was not created successfully.")
        conn.close()

if __name__ == '__main__':
    unittest.main()
