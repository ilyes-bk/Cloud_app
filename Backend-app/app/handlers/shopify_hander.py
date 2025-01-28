from app.subscribers.shopify_subscriber import ShopifySubscriber
from apis.notionCRM import NotionCRM, NotionComments
from apis.shopify import Shopify
from time import sleep
from app.models.Order import Order 
import json

def shopify_handler():
    shopify_sub = ShopifySubscriber()
    crm = NotionCRM()
    shopify = Shopify()
    to_be_acked = []
    while True:
        ack_ids, events = shopify_sub.pull_transcripts()
        for i, event in enumerate(events):
            print(event['admin_graphql_api_id'])
            if 'DraftOrder' in event['admin_graphql_api_id']:

                email = event.get('email')
                first = event.get('customer', {}).get('first_name')
                last = event.get('customer', {}).get('last_name')
                phone = event.get('customer', {}).get('phone')
                full_name = f"{first or ''} {last or ''}".strip() or None

                if email is not None:
                    customer = crm.get_one(email)
                    if customer is None:
                        id = crm.add(full_name, email=email, phone=phone)
                    else:
                        id = customer['id'] if customer else None
                    if id is not None and not crm.id_in_comments(id, event['name']):
                        comment_data = NotionComments.draft_order_comment(event['name'], event['id'])
                        crm.add_comment(id, comment_data=comment_data)
            elif 'Order' in event['admin_graphql_api_id']:
                # Update CRM
                comment_data = NotionComments.order_comment(event['name'], event['id'])
                email = event.get('email')
                customer = crm.get_one(email)
                if customer is not None and not crm.id_in_comments(customer['id'], event['name']):
                    crm.add_comment(customer['id'], comment_data=comment_data)
                
                # Update DB
                order = shopify.order(event['id'])
                Order.delete(order['id'].split('/')[-1])
                Order.create(order['id'].split('/')[-1], order['customer']['displayName'], order['name'], order['customer']['email'].lower(), json.dumps(order['events']))

            to_be_acked.append(ack_ids[i])

        if len(to_be_acked) != 0:
            shopify_sub.ack_transcripts(to_be_acked) 
        sleep(30)
