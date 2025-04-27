import sqlite3
from config import DBFILE

def getDbConnection():
    '''Establish and return a database connection.'''
    conn = sqlite3.connect(DBFILE)
    return conn

def create_emails_table():
    """Create the emails table if it doesn't exist."""
    conn = getDbConnection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id TEXT PRIMARY KEY,
            thread_id TEXT,
            sender TEXT,
            subject TEXT,
            snippet TEXT,
            received_datetime TEXT,
            label_ids TEXT
        )
    ''')
    conn.commit()
    conn.close()