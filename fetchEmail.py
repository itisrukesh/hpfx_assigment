from auth import authenticateGmail
from db import createEmailsTable, storeEmailsBulk
from config import BATCHCOUNT
from utils import BuildEmailRecord


def fetchAndStoreEmails_from_Gmail(mail_service, max_res=10):
    """Fetch emails from Gmail and store them into DB."""
    count = 0    
    
    results = mail_service.users().messages().list(userId='me', maxResults=max_res).execute()
    msgs = results.get('messages',[])
    # print(msgs)
    
    batch = []
    
    for message in msgs:
        # email_data = {}
        msg_id = message["id"]
        msg_details = mail_service.users().messages().get(userId="me", id=msg_id, format='full').execute()
        # print(msg_details)
        
        email_record = BuildEmailRecord(msg_details)
        batch.append(email_record)

        # If batch full, save it
        if len(batch) >= BATCHCOUNT:
            storeEmailsBulk(batch)
            count+=1
            print(f"Batch {count} DONE!")
            batch = []
    # Save any remaining emails
    if batch:
        storeEmailsBulk(batch)
        print(f'Batch Remaining emails DONE!')

def fetchEmails_from_Db():
    '''Fetch emails from database.'''
    pass

if __name__ == "__main__":
    # Individual Running of fetch mail functionalities. If needed.
    service = authenticateGmail()
    createEmailsTable() # PUTME in main.go 
    fetchAndStoreEmails_from_Gmail(service, 200)
    # fetchEmails_from_Db()