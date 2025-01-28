import requests
import os
import phonenumbers

def format_number(number):
    try:
        number = number.replace(" ", "").replace("(", "").replace(")", "").replace("-", "")
        if number.startswith('+'):
            parsed_number = phonenumbers.parse(number)
        else:
            parsed_number = phonenumbers.parse(f"+1{number}")

        if phonenumbers.is_valid_number(parsed_number):
            formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            return formatted_number
        else:
            return None
    
    except phonenumbers.phonenumberutil.NumberParseException:
        return None

class ShopifyQueries:

    @staticmethod 
    def orders(cursor=None):
        return f"""{{
                orders(first: 250, sortKey: CREATED_AT, reverse: true{', after: "' + cursor + '" ' if cursor else ''}) {{
                    edges {{
                        node {{
                            createdAt
                            name
                            id
                            customer {{
                                displayName
                                email
                                phone
                            }}
                            shippingAddress {{
                                name
                                company
                            }}
                            totalPrice
                            events(first: 30, query: "comments:true") {{
                                edges {{
                                    node {{
                                        id
                                        createdAt
                                        message
                                    }}
                                }}
                            }}
                        }}
                    }}
                    pageInfo {{
                        hasNextPage
                        endCursor
                    }}
                }}
            }}"""
    @staticmethod
    def order(order_id):
        if 'gid' not in str(order_id):
            order_id = 'gid://shopify/Order/' + str(order_id)
        return f"""{{
            order(id: "{order_id}") {{
                createdAt
                name
                id
                customer {{
                    displayName
                    email
                    phone
                }}
                shippingAddress {{
                    name
                    company
                }}
                totalPrice
                events(first: 30, query: "comments:true") {{
                    edges {{
                        node {{
                            id
                            createdAt
                            message
                        }}
                    }}
                }}
            }}
        }}"""
    
    @staticmethod
    def order_by_name(order_number):
        query = f"""
        {{
            orders(first: 5, query:"{order_number}") {{
                edges {{
                    node {{
                        id
                        name
                        createdAt
                        displayFulfillmentStatus
                        customer {{
                            displayName
                            email
                            phone
                        }}
                        events (first: 10, query:"action:comment"){{
                            edges {{
                                node {{
                                    createdAt
                                    message
                                    id
                                }}
                            }}
                        }}
                        fulfillments(first: 5) {{
                            status
                            trackingInfo(first: 5){{
                                url
                            }}
                        }}
                        lineItems(first: 5) {{
                            edges {{
                                node {{
                                    id
                                    title
                                    quantity
                                }} 
                            }} 
                        }}
                    }}
                }}
            }}
        }}
        """
        return query

    @staticmethod
    def draft_order(name):
        if 'D' not in name:
            name = 'D' + name
        return f"""
        {{
            draftOrders(first: 5, query:"{name}") {{
                edges {{
                    node {{
                        id
                        name
                        customer {{
                            displayName
                            email
                            phone
                        }}
                        lineItems(first: 5) {{
                            edges {{
                                node {{
                                    title
                                    quantity
                                }} 
                            }} 
                        }}
                    }} 
                }} 
            }} 
        }}
        """
    
    @staticmethod 
    def draft_orders(cursor=None):
        return f"""{{
                draftOrders(first: 250, sortKey: UPDATED_AT, reverse: true{', after: "' + cursor + '" ' if cursor else ''}) {{
                    edges {{
                        node {{
                            createdAt
                            name
                            id
                            customer {{
                                displayName
                                email
                                phone
                            }}
                            shippingAddress {{
                                name
                                company
                            }}
                            totalPrice
                        }}
                    }}
                    pageInfo {{
                        hasNextPage
                        endCursor
                    }}
                }}
            }}"""

    @staticmethod
    def products(cursor=None):
        return f"""
        {{
        products(first: 250 {f', after: "{cursor}"' if cursor else ''}) {{
            edges {{
            node {{
                id
                handle
                title
                productType
                variants(first: 250) {{
                edges {{
                    node {{
                    id
                    displayName
                    price
                    sku
                    }}
                }}
                }}
            }}
            }}
            pageInfo {{
            hasNextPage
            endCursor
            }}
        }}
        }}
        """

    @staticmethod
    def customer_query():
        return  """
            query($email: String!) {
                customers(first: 1, query: $email) {
                    edges {
                        node {
                            id
                            email
                            firstName
                            lastName
                            phone
                        }
                    }
                }
            }
        """
    
    @staticmethod
    def create_draft_order():
        return  """
        mutation($input: DraftOrderInput!) {
            draftOrderCreate(input: $input) {
                draftOrder {
                id
                name
                }
                userErrors {
                field
                message
                }
            }
        }
        """
    
    @staticmethod
    def create_customer():
        return """
        mutation($input: CustomerInput!) {
            customerCreate(input: $input) {
                customer {
                    id
                    email
                    firstName
                    lastName
                    phone
                }
                userErrors {
                    field
                    message
                }
            }
        }
        """
    @staticmethod
    def update_customer():
        return """
        mutation($input: CustomerInput!) {
            customerUpdate(input: $input) {
                customer {
                    id
                    email
                    firstName
                    lastName
                    phone
                }
                userErrors {
                    field
                    message
                }
            }
        }
        """ 

class Shopify:
    def __init__(self):
        self.TOKEN = os.environ['SHOPIFY_ACCESS_TOKEN']
        self.STORE = os.environ['SHOPIFY_STORE']
        self.url = f"https://{self.STORE}.myshopify.com/admin/api/2023-07/graphql.json"

    def _flat_edges(self, data, key):
        print(data)
        data[key] = [edge['node'] for edge in data[key]['edges'] if 'node' in edge]

    def _flat_events(self, order):
        filtered_events = [
                {
                    'id': event['node']['id'],
                    'createdAt': event['node']['createdAt'],
                    'message': event['node']['message']
                }
                for event in order['events']['edges']
                if 'CommentEvent' in event['node']['id']  # Only keep comment events
            ]
        order['events'] = filtered_events

    def auth_req(self, query, variables = None):
        data = {'query': query}
        if variables:
            data['variables'] = variables
        response = requests.post(self.url,
        json=data,
        headers={
            'Content-Type': 'application/json',
            'X-Shopify-Access-Token': self.TOKEN
        })
        return response

    def orders(self, max=None):
        all_orders = []
        has_next_page = True
        cursor = None

        while has_next_page:
            query = ShopifyQueries.orders(cursor)
            
            response = self.auth_req(query)
            
            if response.status_code == 200:
                data = response.json()
                orders = [o['node'] for o in data['data']['orders']['edges']]
                all_orders.extend(orders)
                if max is not None and len(all_orders) >= max:
                    break  
                page_info = data['data']['orders']['pageInfo']
                has_next_page = page_info['hasNextPage']
                cursor = page_info['endCursor']
            else:
                has_next_page = False
        for order in all_orders:
            self._flat_events(order)
        return all_orders

    def draft_order(self, draft_name):
        query = ShopifyQueries.draft_order(draft_name)
        response = self.auth_req(query)
        
        if response.status_code == 200:
            data = response.json()
            drafts = data['data']['draftOrders']['edges']
            
            if len(drafts):
                draft = drafts[0]['node']
                
                # Flatten the lineItems list by extracting the 'node' for each item
                draft['lineItems'] = [item['node'] for item in draft['lineItems']['edges']]
                
                return draft
        
    def order(self, id):
        query = ShopifyQueries.order(id)
        response = self.auth_req(query)
        if response.status_code == 200:
            data = response.json()
            order = data['data']['order']
            self._flat_events(order)
            return order

    def order_via_name(self, name):
        query = ShopifyQueries.order_by_name(name)
        response = self.auth_req(query)
        print(response.text)
        if response.status_code == 200:
            data = response.json()
            
            if len(data['data']['orders']['edges']) > 0:
                order = data['data']['orders']['edges'][0]['node']
                self._flat_events(order)
                self._flat_edges(order, 'lineItems')
                return order 

    def draft_orders(self, max=None):
        all_draft_orders = []
        has_next_page = True
        cursor = None

        while has_next_page:
            query = ShopifyQueries.draft_orders(cursor)
            
            response = self.auth_req(query)
            
            if response.status_code == 200:
                data = response.json()
                draft_orders = [d['node'] for d in data['data']['draftOrders']['edges']]
                all_draft_orders.extend(draft_orders)
                if max is not None and len(all_draft_orders) >= max:
                    break 
                page_info = data['data']['draftOrders']['pageInfo']
                has_next_page = page_info['hasNextPage']
                cursor = page_info['endCursor']
            else:
                has_next_page = False
        
        return all_draft_orders

    def products(self):
        all_products = []
        has_next_page = True
        cursor = None

        while has_next_page:
            query = ShopifyQueries.products(cursor)
            response = self.auth_req(query)
            if response.status_code == 200:
                data = response.json()
                draft_orders = [d['node'] for d in data['data']['products']['edges']]
                all_products.extend(draft_orders)
                page_info = data['data']['products']['pageInfo']
                has_next_page = page_info['hasNextPage']
                cursor = page_info['endCursor']
            else:
                has_next_page = False
        
        return all_products
    
    def _gidify(self, id, resource):
        if 'gid' not in str(id):
            return "gid://shopify/" + resource + "/" + str(id)
        return id

    def customer_create(self, email=None, first_name=None, last_name=None, phone=None, province_code = None):
        input_dict = {}
        if email:
            input_dict["email"] = email
        if first_name:
            input_dict["firstName"] = first_name
        if last_name:
            input_dict["lastName"] = last_name
        if phone:
            input_dict["phone"] = phone
        if province_code:
            input_dict['addresses'] = []
            input_dict['addresses'].append({"countryCode": "US", "provinceCode": province_code}) 

        query = ShopifyQueries.create_customer()
        response = self.auth_req(query, {'input': input_dict})
        data = response.json()
        try:
            customer = data['data']['customerCreate']['customer']
            return customer
        except Exception as e:
            return "something went wrong with"

    def get_customer(self, email):
        query = ShopifyQueries.customer_query()
        variables = {"email": email}
        response = self.auth_req(query, variables)
        data = response.json()
        if len(data['data']['customers']['edges']) != 0:
            customer = data['data']['customers']['edges'][0]['node']
            return customer
        return None

    def draft_order_create(self, ids, email, phone = None, first_name = None, last_name = None, province_code = None):
        try:
            if phone:
                phone = format_number(phone)
            customer = self.get_customer(email)
            if customer is None:
                customer = self.customer_create(email, first_name, last_name, phone)
            input = {
                "lineItems": [{'variantId': self._gidify(id, "ProductVariant"), 'quantity': 1} for id in ids],
                "email": email,
            }
            if "shippingAddress" not in input:
                input["shippingAddress"] = {}

            if phone:
                input['phone'] = phone
        
            if province_code:
                input["shippingAddress"]["countryCode"] = "US"
                input["shippingAddress"]["provinceCode"] = province_code
            
            query = ShopifyQueries.create_draft_order()
            response = self.auth_req(query, {'input': input})
            data = response.json()
            draft = data['data']['draftOrderCreate']['draftOrder']
            draft_id = draft['id'].split('/')[-1]
            draft['link'] = f'https://admin.shopify.com/store/{self.STORE}/draft_orders/' + draft_id
            return draft
        except Exception as e: 
            return "Something went wrong with creating the draft"
        
