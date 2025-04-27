from auth import authenticateGmail
from db import create_emails_table, getDbConnection
import email

def fetchEmails(max_res=10):
    """Fetch emails from Gmail and store them into SQLite DB."""
    
    mail_service = authenticateGmail()
    create_emails_table()
    
    results = mail_service.users().messages().list(userId='me', maxResults=max_res).execute()
    msgs = results.get('messages',[])
    # print(msgs)
    
    conn = getDbConnection()
    cursor = conn.cursor()
    
    for message in msgs:
        msg_id = message["id"]
        msg_details = mail_service.users().messages().get(userId="me", id=msg_id, format='full').execute()
        # print(msg_details)
        payload = msg_details['payload']
        headers = msg_details["payload"]['headers']

        sender = subject = received_datetime = ""        
        for header in headers:
            if header['name'] == 'From':
                sender = header['value']
            if header['name'] == 'Subject':
                subject = header['value']
            if header['name'] == 'Date':
                received_datetime = header['value']
        
        # print(sender, subject, received_datetime)
        snippet = msg_details.get('snippet', '')
        label_ids = ','.join(msg_details.get('labelIds', []))
        # print(snippet, label_ids)
        
          # Insert into database
        cursor.execute('''
            INSERT OR IGNORE INTO emails (id, thread_id, sender, subject, snippet, received_datetime, label_ids)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            msg_details['id'],
            msg_details['threadId'],
            sender,
            subject,
            snippet,
            received_datetime,
            label_ids
        ))
    
    conn.commit()
    conn.close()        
            
        

if __name__ == "__main__":
    fetchEmails(20)