from app.subscribers.gmail_subscriber import GmailSubscriber
from google.oauth2 import service_account
from googleapiclient.discovery import build
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
from langchain_core.messages import HumanMessage
from assistant import build_transcript_graph 
from time import sleep
connection_kwargs = {
    "autocommit": True,
    "prepare_threshold": 0,
}
def gmail_client(service_account_file, user_email):
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=SCOPES)
    delegated_credentials = credentials.with_subject(user_email)
    gmail_client = build('gmail', 'v1', credentials=delegated_credentials)
    return gmail_client

def get_history(service, start_history_id):
    """Fetches recent history since the provided historyId."""
    changes = []
    while True:
        try:
            request = service.users().history().list(userId='me', startHistoryId=start_history_id)
            while request:
                response = request.execute()
                changes.extend(response.get('history', []))
                request = service.users().history().list_next(request, response)  # Check for pagination
            
            return changes
        except TimeoutError as e:
            sleep(5)

def gmail_handler():
    gmail_sub = GmailSubscriber()
    handled_ids = set()
    service = gmail_client("admin-gmail.json", "support@thesaunaheater.com")
    while True:
        ack_ids, hist_id = gmail_sub.pull()
        print(f"Hist ID: {hist_id}")
        if hist_id is not None:
            thread_ids = set()
            changes = get_history(service, hist_id)
            for change in changes:
                
                if 'messagesAdded' in change:
                    for message_entry in change['messagesAdded']:
                        message = message_entry['message']
                        
                        if ('SENT' in message['labelIds'] or 'INBOX' in message['labelIds']) and message['id'] not in handled_ids:
                            thread_ids.add(message['threadId'])
                            handled_ids.add(message['id'])

            for thread_id in thread_ids:
                try:
                    thread = service.users().threads().get(userId='me', id=thread_id).execute()
                    msgs = [msg for msg in thread.get('messages', []) if 'DRAFT' not in msg['labelIds']]
                    
                    if msgs:
                        headers = msgs[-1]['payload'].get('headers', [])
                        header_dict = {header['name']: header['value'] for header in headers}
                        
                        print("From:", header_dict.get("From"))
                        print("To:", header_dict.get("To"))
                        print("Subject:", header_dict.get("Subject"))
                        print('*' * 20)
                except Exception as e:
                    print(f"Error fetching thread {thread_id}: {e}")

        if ack_ids:
            gmail_sub.ack_transcripts(ack_ids)

        sleep(5)
