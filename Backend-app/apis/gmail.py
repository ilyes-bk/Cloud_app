import os
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
service_account_file = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '')
from google.oauth2 import service_account
from googleapiclient.discovery import build
import base64
import mailparser
import socket
from ssl import SSLEOFError
from bs4 import BeautifulSoup
from google.oauth2.credentials import Credentials
import json
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
class Gmail:
    def __init__(self):
        self.credentials = self._load_credentials()
        self.client = build('gmail', 'v1', credentials=self.credentials)
        self.attempts = 3

    def _load_credentials(self):
        """Load credentials from token.json or prompt for OAuth2 flow if not available or expired"""
        creds = None
        
        if os.path.exists('token.json'):
            with open('token.json', 'r') as token:
                creds_data = json.load(token)
                creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())  # Refresh the token if expired
                except RefreshError:
                    print("Failed to refresh token. Please re-authenticate.")
                    creds = self._authorize()  # Re-authenticate if refresh fails
            else:
                creds = self._authorize()
            with open('token.json', 'w') as file:
                file.write(creds.to_json())
        return creds

    def _authorize(self):
        from google_auth_oauthlib.flow import InstalledAppFlow
        
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json', SCOPES, )
        creds = flow.run_local_server(port=8080)  # Runs a local server for authorization

        return creds


    def _parse_latest_message(self, service, user_id, message_id):
        msg = service.users().messages().get(userId=user_id, id=message_id, format='raw').execute()
        raw_email = base64.urlsafe_b64decode(msg['raw']).decode('utf-8')
        parsed_email = mailparser.parse_from_string(raw_email)
        if len(parsed_email.text_plain) == 0:
            html_content = '\n'.join(parsed_email.text_html)
            soup = BeautifulSoup(html_content, 'html.parser')
            text_plain = soup.get_text()
        else:
            text_plain = ''.join(parsed_email.text_plain)

        message_details = {
            'from': parsed_email.from_,
            'to': parsed_email.to,
            'subject': parsed_email.subject,
            'date': parsed_email.date,
            'body_text': f"Date: {parsed_email.date}\n {text_plain}",  # List of plain text parts
            'body_html': parsed_email.text_html,   # List of HTML parts
            'attachments': parsed_email.attachments  # List of attachments
        }
        return message_details


    def _query_messages(self, query):
        socket.setdefaulttimeout(2)
        for attempt in range(self.attempts):
            try:
                results = self.client.users().messages().list(userId='me', q=query).execute()
                messages = results.get('messages', [])
                thread_to_messages = {}
                for message in messages: 
                    if message['threadId'] not in thread_to_messages:
                        thread_to_messages[message['threadId']] = message['id']
                messages = []
                for tid, mid in thread_to_messages.items():
                    t = self._parse_latest_message(self.client, 'me', message_id=mid)
                    messages.append(t['body_text'])
                for i, msg in enumerate(messages, 1):
                    msg += f"{i}. Thread: {msg}\n\n{'-'*10}"
                return ''.join(messages)
            except TimeoutError as e:
                pass
            except SSLEOFError as e:
                pass
        socket.setdefaulttimeout(None)
        return "Gmail is not responding"

    def get_threads(self, email):
        q=f"from:{email} OR to:{email}"
        return self._query_messages(query=q)


    def get_threads_by_subject(self, subject):
        q=f"subject:{subject}"
        return self._query_messages(query=q) 
gmail = Gmail()