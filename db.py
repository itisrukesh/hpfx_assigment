import sqlite3
from config import DBFILE

class TableQuery:
    EMAIL_FIELDS = {
        'id': 'TEXT',
        'thread_id': 'TEXT',
        'sender': 'TEXT',
        'subject': 'TEXT',
        'snippet': 'TEXT',
        'received_datetime': 'DATETIME',
        'label_ids': 'TEXT',
        # 'is_read': 'BOOLEAN',           # Example extra field.  
        # 'attachment_count': 'INTEGER'   # Example extra field. 
    }

    @classmethod
    def createEmails_Table(cls):
        columns = ',\n'.join([
            f"{field} {datatype}" for field, datatype in cls.EMAIL_FIELDS.items()
        ])
        query = f'''
            CREATE TABLE IF NOT EXISTS emails (
                {columns},
                PRIMARY KEY (id)
            );
        '''
        return query

    @classmethod
    def insertEmail(cls):
        placeholders = ', '.join(['?' for _ in cls.EMAIL_FIELDS])
        columns = ', '.join(cls.EMAIL_FIELDS.keys())
        query = f'''
            INSERT OR IGNORE INTO emails ({columns})
            VALUES ({placeholders});
        '''
        return query

    SELECT_ALL_EMAILS = '''
        SELECT * FROM emails;
    '''

def getDbConnection():
    '''Establish and return a database connection.'''
    return sqlite3.connect(DBFILE)

# Table Creation
def createEmailsTable():
    """Create the emails table if it doesn't exist."""
    with getDbConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(TableQuery.createEmails_Table())
        conn.commit()

def storeEmailsBulk(email_records):
    """Bulk save a list of email records into the database."""
    if not email_records:
        return

    with getDbConnection() as conn:
        cursor = conn.cursor()
        cursor.executemany(TableQuery.insertEmail(), email_records)
        conn.commit()