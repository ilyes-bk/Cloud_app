import phonenumbers
import requests
import os
import json

class OpenPhone:
    def __init__(self):
        self.key = os.environ['OPENPHONE_API_KEY']
        self.id_to_user = {}
        numbers = self.phone_numbers()['data']
        for number in numbers:
            for user in number['users']:
                self.id_to_user[user['id']] = user['firstName']
                
    def auth_req(self, endpoint, params={}):
        url = "https://api.openphone.com/v1" + endpoint        
        response = requests.get(url, headers = {"Authorization": self.key}, params=params)
        data = response.json()
        return data

    def calls(self, number):
        number = phonenumbers.parse(number, "US")
        number = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)
        params = {
            "phoneNumberId": "PN2UNaof5N",
            "participants": [number],
            "maxResults": 10
        }
        return self.auth_req("/calls", params)

    def recording(self, id):
        endpoint = f"/call-recordings/{id}"
        return self.auth_req(endpoint)
        
    def transcript(self, id):
        endpoint = f"/call-transcripts/{id}"
        return self.auth_req(endpoint)
        
    def phone_numbers(self):
        endpoint = "/phone-numbers"
        return self.auth_req(endpoint)

    def _format_transcript(self, dialogue):
        formatted_dialogue = ""
        for line in dialogue:
            if line['userId'] is not None:
                formatted_dialogue += f"{self.id_to_user[line['userId']]}: {line['content']} \n"
            else:
                formatted_dialogue += f"Customer: {line['content']} \n"
        return formatted_dialogue
            
    
    def search_transcript(self, number):
        calls = self.calls(number)
        for call in calls['data']:
            if call['duration'] > 10:
                call_id = call['id']
                transcript = openphone.transcript(call_id)
                if 'data' in transcript:
                    
                    dialogue = self._format_transcript(transcript['data']['dialogue'])
                    transcript = transcript['data']['createdAt'] + "\n" + dialogue

                    return transcript
        return "Cound't find transcript"
                
    def numbers(self):
        return self.auth_req('/phone-numbers')

#openphone = OpenPhone()


class MockCalls:
    def __init__(self):
        try:
            with open('./data/mock-calls.json', 'r') as mock_calls:
                self.calls = json.load(mock_calls)
        except FileNotFoundError:
            self.calls = {}
        print(self.calls)
    def search_transcript(self, number): 
        number = phonenumbers.parse(number, "US")
        number = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)
        calls = self.calls.get(number, 'Calls not found')
        if isinstance(calls, list):
            calls = '\n'.join(calls)

        return calls


openphone = MockCalls()