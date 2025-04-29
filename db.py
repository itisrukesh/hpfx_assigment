import sqlite3
from config import DBFILE, EMAILSTABLE, HISTORYTABLE

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
    
    RULE_HISTORY_FIELDS = {
        'email_id':"TEXT",
        'rule_id':'TEXT',
        'actions_taken':'TEXT',
        'status':'TEXT',
        'processed_at':'DATETIME'
    }
    
    SELECT_ALL_EMAILS = f'''
        SELECT * FROM {EMAILSTABLE};
    '''

    @classmethod
    def createEmails_Table(cls):
        columns = ',\n'.join([
            f"{field} {datatype}" for field, datatype in cls.EMAIL_FIELDS.items()
        ])
        query = f'''
            CREATE TABLE IF NOT EXISTS {EMAILSTABLE} (
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
            INSERT OR IGNORE INTO {EMAILSTABLE} ({columns})
            VALUES ({placeholders});
        '''
        return query
    
    @classmethod
    def createProcessedHistory_Table(cls):
        columns = ',\n'.join([
            f"{field} {datatype}" for field, datatype in cls.RULE_HISTORY_FIELDS.items()
        ])
        query = f'''
            CREATE TABLE IF NOT EXISTS {HISTORYTABLE} (
                {columns},
                FOREIGN KEY (email_id) REFERENCES {EMAILSTABLE}(id)
            );
        '''
        return query
    
    @classmethod
    def insertHistories(cls):
        placeholders = ', '.join(['?' for _ in cls.RULE_HISTORY_FIELDS])
        columns = ', '.join(cls.RULE_HISTORY_FIELDS.keys())
        query = f'''
            INSERT OR IGNORE INTO {HISTORYTABLE} ({columns})
            VALUES ({placeholders});
        '''
        return query


def getDbConnection():
    '''Establish and return a database connection.'''
    return sqlite3.connect(DBFILE)

def get_mails_from_db() -> list:
    """Get the emails from table."""
    with getDbConnection() as conn:
        cursor = conn.cursor()    
        cursor.execute(TableQuery.SELECT_ALL_EMAILS)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        emails = [dict(zip(columns, row)) for row in rows]
        
    return emails

# Table Creation Emails:
def createEmailsTable():
    """Create the emails table if it doesn't exist."""
    with getDbConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(TableQuery.createEmails_Table())
        conn.commit()

# Table Creation History:
def createHistoriesTable():
    '''Create the processed history table if it doesn't exist'''
    with getDbConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(TableQuery.createProcessedHistory_Table())
        conn.commit()

def storeEmailsBulk(email_records):
    """Bulk save a list of email records into the database."""
    if not email_records:
        return

    with getDbConnection() as conn:
        cursor = conn.cursor()
        cursor.executemany(TableQuery.insertEmail(), email_records)
        conn.commit()
        
def storeProcessedHistory(processed_records):
    """Bulk save a list of processed history records into the database."""
    if not processed_records:
        return
    
    with getDbConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(TableQuery.insertHistories(), processed_records)
        conn.commit()