import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_user():
    creds = None

    # Check if the token file exists and read it
    if os.path.exists('token.json'):
        with open('token.json', 'r') as token:
            creds_dict = json.load(token)
            creds = Credentials.from_authorized_user_info(creds_dict, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=8080)

        # Save the credentials as plain text in a JSON file
        creds_dict = {
            'token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_uri': creds.token_uri,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            'scopes': creds.scopes
        }
        
        with open('token.json', 'w') as token:
            json.dump(creds_dict, token)

    return creds

if __name__ == '__main__':
    authenticate_user()

