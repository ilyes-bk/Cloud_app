import os
from typing import Optional
from notion_client import Client
from datetime import datetime, timedelta

class NotionComments():

    @staticmethod
    def order_comment(name, id):
        return {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": f"Order {name}\n"
                    }
                },
                {
                    "type": "text",
                    "text": {
                        "content": "Order Link",
                        "link": {
                            "url": f"https://admin.shopify.com/store/the-sauna-heater/orders/{id}"
                        }
                    }
                }
            ]
        }
    @staticmethod
    def draft_order_comment(name, id):
        return {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": f"Draft/Quote {name}\n"
                    }
                },
                {
                    "type": "text",
                    "text": {
                        "content": "Link",
                        "link": {
                            "url": f"https://admin.shopify.com/store/the-sauna-heater/draft_orders/{id}"
                        }
                    }
                }
            ]
        }
class NotionCRM:
    def __init__(self):
      self.client =  Client(auth=os.environ.get('NOTION_ACCESS_TOKEN'))
      self.database_id = "90cd0438-535c-452e-bb9c-2194fe09eb6f"

    def id_in_comments(self, customer_id, id):
        comments = self.get_comments(customer_id)
        for c in comments['results']:
            for text_part in c['rich_text']:
                if id in text_part['plain_text']:
                    return True
        return False

    def get_comments(self, page_id):
        return self.client.comments.list(block_id = page_id)
        
    def add_comment(self, page_id, comment = None, comment_data = None):
        if comment_data is None:
            comment_data = {
                    "parent": {"page_id": page_id},
                    "rich_text": [{"text": {"content": comment}}]
                }
        else: 
            comment_data["parent"] = {"page_id": page_id}
        self.client.comments.create(**comment_data)

    def add(self, customer_name: str, email: Optional[str] = None, phone: Optional[str]= None, next_follow_up: Optional[str] = None, comment: Optional[str] = None):
        today_date = datetime.today().strftime('%Y-%m-%d')
        if next_follow_up is None:
            next_follow_up = (datetime.today() + timedelta(weeks=1)).strftime('%Y-%m-%d')

        new_page_data = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Lead Name": {
                    "title": [{"text": {"content": customer_name}}]
                },
                "Tags": {
                    "multi_select": [{"name": "Buying Window"}]  
                },
                "Last Contact": {
                    "date": {
                        "start": today_date
                    }
                },
                "Next Follow Up": {
                    "date": {
                        "start": next_follow_up 
                    }
                }
            },
        }
        if email is not None:
            new_page_data["properties"]["Email"] = {"email": email}
        if phone is not None: 
            new_page_data["properties"]["Phone"] = {"phone_number": str(phone)}
        try:
            response = self.client.pages.create(**new_page_data)
            page_id = response['id']
            
            if comment is not None:
                self.add_comment(page_id, comment)
            return page_id
        except Exception as e:
            return None
      

    def get_all(self):
        all_pages = []
        has_more = True
        start_cursor = None
        
        while has_more:
            try:
                # Query the database with pagination support
                query_params = {
                "database_id": self.database_id,
                "filter": {
                    "property": "Tags",
                    "multi_select": {
                        "contains": "Buying Window"
                    }
                }
            }
                if start_cursor:
                    query_params["start_cursor"] = start_cursor
                query_result = self.client.databases.query(**query_params)
                
                all_pages.extend(query_result.get('results', []))
    
                has_more = query_result.get('has_more', False)
                start_cursor = query_result.get('next_cursor', None)
                
            except Exception as e:
                print("Error fetching the CRM database:", e)
                break
        customers = []
        # Process and print the retrieved data safely
        for page in all_pages:
            page_properties = page.get('properties', {})
            page_id = page.get('id', 'N/A')
            customer = self.build_customer(page_properties)
            customer['id'] = page_id
            customers.append(customer)
                    
        return customers
    
    def get_one(self, email):
        try:
            query_params = {
                "database_id": self.database_id,
                "filter": {
                    "property": "Email",
                    "email": {
                        "equals": email
                    }
                }
            }
            
            query_result = self.client.databases.query(**query_params)
            results = query_result.get('results', [])
            
            if not results:
                return None
            
            page = results[0]
            page_properties = page.get('properties', {})
            page_id = page.get('id', 'N/A')
            customer = self.build_customer(page_properties)
            customer['id'] = page_id
            return customer

        except Exception as e:
            print("Error fetching the CRM database:", e)
            return None
        
    def build_customer(self, page_properties):
        lead_name_prop = page_properties.get('Lead Name', {})
        lead_name_list = lead_name_prop.get('title', [])
        lead_name = lead_name_list[0].get('text', {}).get('content', 'N/A') if lead_name_list else 'N/A'

        last_contact_prop = page_properties.get('Last Contact', None)
        last_contact = last_contact_prop['date'].get('start', 'N/A') if last_contact_prop and last_contact_prop.get('date') else 'N/A'
        
        next_follow_up_prop = page_properties.get('Next Follow Up', None)
        next_follow_up = next_follow_up_prop['date'].get('start', 'N/A') if next_follow_up_prop and next_follow_up_prop.get('date') else 'N/A'
        
        tags_prop = page_properties.get('Tags', {}).get('multi_select', [])
        tags = [tag.get('name', 'N/A') for tag in tags_prop] if tags_prop else ['N/A']

        email = page_properties.get('Email', {}).get('email', 'N/A')
        phone = page_properties.get('Phone', {}).get('phone_number', 'N/A')
        
        # Construct the customer data
        customer = {
            'name': lead_name,
            'last_contact': last_contact,
            'next_follow_up': next_follow_up,
            'tags': tags,
            'email': email,
            'phone': phone
        }
        return customer
    