import os
import json
from google.cloud import pubsub_v1
from google.api_core.exceptions import DeadlineExceeded
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "admin-gmail.json"
class ChatraSubscriber:
    def __init__(self):
        project_id = "pubsub-webhooks"
        subscription_id = "chatra-transcripts-topic-sub"
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscription_path = self.subscriber.subscription_path(project_id, subscription_id)

    def pull_transcripts(self):
        convos = []
        num_messages = 2 
        pulled_message_ids = set()
        try:
            response = self.subscriber.pull(
                request={
                    "subscription": self.subscription_path,
                    "max_messages": num_messages,
                },
            )
            for received_message in response.received_messages:
                message_id = received_message.message.message_id
                if message_id not in pulled_message_ids:
                    pulled_message_ids.add(message_id)
                    convos.append(json.loads(received_message.message.data.decode('utf-8')))
            
            ack_ids = [r.ack_id for r in response.received_messages]
            return ack_ids, convos
        except DeadlineExceeded as e:
            #print("Deadline exceeded during pull:", e)
            return [], []  

            
    def ack_transcripts(self, ack_ids): 
        self.subscriber.acknowledge(
            request={
                "subscription": self.subscription_path,
                "ack_ids": ack_ids,
            }
        )
    