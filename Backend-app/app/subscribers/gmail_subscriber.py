import json
from google.cloud import pubsub_v1
from google.api_core.exceptions import DeadlineExceeded

class GmailSubscriber:
    def __init__(self):
        project_id = "pubsub-webhooks"
        subscription_id = "gmail-sub"
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscription_path = self.subscriber.subscription_path(project_id, subscription_id)
        self.history_id = None
    def pull(self):
        num_messages = 2
        pulled_message_ids = set()
        hist_id = self.history_id
        try:
            response = self.subscriber.pull(
                request={
                    "subscription": self.subscription_path,
                    "max_messages": num_messages,
                },
            )
            if not response.received_messages:
                return [], None
            hist_ids = []
            for received_message in response.received_messages:
                message_id = received_message.message.message_id
                if message_id not in pulled_message_ids:
                    pulled_message_ids.add(message_id)
                    try:
                        data = json.loads(received_message.message.data.decode('utf-8'))
                        hist_ids.append(int(data['historyId'])) 
                    except Exception as e:
                        print("Error parsing message:", e)
            self.history_id = min(hist_ids) 
            ack_ids = [r.ack_id for r in response.received_messages]
            return ack_ids, hist_id 

        except DeadlineExceeded as e:
            print("Deadline exceeded during pull:", e)
            return [], None 

    def ack_transcripts(self, ack_ids): 
        try:
            self.subscriber.acknowledge(
                request={
                    "subscription": self.subscription_path,
                    "ack_ids": ack_ids,
                }
            )
        except Exception as e:
            print("Error during acknowledge:", e)
