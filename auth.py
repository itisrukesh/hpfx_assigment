import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from config import TOKENFILE, CREDSFILE, SCOPES, PORT

def authenticate_gmail():
    """Authenticate and return Gmail service."""
    creds = None 

    # Load existing credentials if available
    if os.path.exists(TOKENFILE):
        creds = Credentials.from_authorized_user_file(TOKENFILE, SCOPES)

    # If no valid credentials available, initiate login flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDSFILE, SCOPES)
            creds = flow.run_local_server(port=PORT)

        # Save the credentials for next run
        with open(TOKENFILE, 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service