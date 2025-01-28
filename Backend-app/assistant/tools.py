from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
from .vector_store import load_vector_store
from typing import Optional, Literal
from langgraph.graph import MessagesState
from apis.notionCRM import NotionCRM
from apis.shopify import Shopify
from apis.gmail import gmail
import logging
from apis.openphone import openphone
from app.models.Order import Order 
import os
import json
import logging
products_store = load_vector_store('products')
manuals_store = load_vector_store('manuals')
products_metadata_store = load_vector_store('products_metadata')

print(" ❎❎❎❎  Starting the tools module")

@tool 
def find_order_information(order_number: str):
    """
    Find order infomation with order number

    Args:
        order_number (str): Provided order number. Format is usually DXXXXXX or 23XXXX 

    Returns:
        order data, events
    """
    print(f" ❎❎❎❎  Calling find_order_information with order_number: {order_number}")
    try: 
        if 'D' in order_number:
            order = Order.get_order(comment_id=order_number)
            print(f" ❎❎❎❎  Order found: {order}")
        else:
            shopify = Shopify()
            order = shopify.order_via_name(order_number)
            order['link'] = f'https://admin.shopify.com/store/{os.environ["SHOPIFY_STORE"]}/orders/{order["id"].split("/")[0]}'
            print(f" ❎❎❎❎  Order found: {order}")

        # Fetch email threads
        email = order["customer"].get("email", None)
        try:
            events = order["events"][0]
        except:
            events = None
        if email:
            print(f" ❎❎❎❎  Calling get_email_threads with email: {email}")
            threads = gmail.get_threads(email)
            order['email_threads'] = threads
            print(f" ❎❎❎❎  Email threads found: {threads}")

        # Fetch phone conversations
        phone = order["customer"].get("phone", None)
        if phone:
            print(f" ❎❎❎❎  Calling get_phone_conversation with phone: {phone}")
            transcript = openphone.search_transcript(phone)
            order['phone_conversations'] = transcript
            print(f" ❎❎❎❎  Phone conversation transcript: {transcript}")

        return str(json.dumps(order)) + str(events)
    except Exception as e:
        logging.error(f"Error fetching order: {e}")
        return "Error fetching order"


@tool 
def find_email_threads_with_order(order_number: str):
    """
    Search email conversation(s) based on an order_number found in order event comments

    Args:
        order_number (str): Provided order number. Format is usually DXXXXXX

    Returns:
        str: the matching email conversations
    """
    print(f" 🆗🆗🆗🆗  Calling find_email_threads_with_order with order_number: {order_number}")
    try: 
        threads = gmail.get_threads_by_subject(order_number)
        print(f" 🆗🆗🆗🆗  Email threads found: {threads}")

        return threads
    except Exception as e:
        logging.error(f"Error fetching order: {e}")
        return "Error fetching order"


@tool
def add_customer_to_crm(customer_name: str, email: Optional[str] = None, phone: Optional[str]= None, next_follow_up: Optional[str] = None, comment: Optional[str] = None) -> str:
    """
    Add customer to CRM. 

    Args:
        customer_name (str): Customer name user provided
        email Optional[str]: Customer email if provided
        phone Optional[str]: Customer phone number if provided
        next_follow_up Optional[str]: Follow up date in format YYYY-MM-DD if provided
        comment Optional[str]: Optional comment that the user provided

    Returns:
        str: id of the crm entry
    """
    print(f" ❎❎❎❎  Calling add_customer_to_crm with customer_name: {customer_name}, email: {email}, phone: {phone}, next_follow_up: {next_follow_up}, comment: {comment}")
    crm = NotionCRM()
    page_id = crm.add(customer_name, email, phone, next_follow_up, comment)
    print(f" ❎❎❎❎  Customer added to CRM with page ID: {page_id}")
    return page_id

@tool
def get_product_metadata_information(keywords: str) -> str:
    """
    Search products based on metadata. 
    Only use when some of the following information is needed:
    Price, title, id, sku, or price. If you need other information, use other tools.

    Args:
        keywords (str): Keywords such as brand and model that user provided

    Returns:
        str: returns a list of product metadata
    """
    print(f" ❎❎❎❎  Calling get_product_metadata_information with keywords: {keywords}")
    results = products_metadata_store.similarity_search(keywords, 30)
    print(f" ❎❎❎❎  Product metadata search results: {results}")
    return results


@tool
def get_information_from_manual(query:str) -> str:
    """
    Search technical information from product manuals.
    You have access to following manuals:
    - HUUM HIVE
    - HUUM STEEL
    - HUUM CLIFF
    - HUUM DROP
    - SAUNUM AIR
    - HARVIA KIP
    - HARVIA VIRTA 

    Args:
        query (str): Descriptive query of the information that you are looking for. Include the product name in the query 

    Returns:
        str: documents (pages from manuals) that match the query 
    """
    print(f" ❎❎❎❎  Calling get_information_from_manual with query: {query}")
    models = ['cliff', 'steel', 'drop', 'hive', 'air', 'kip', 'virta']
    for model in models:
        if model in query.lower():
            selected_model = model
            break
    filter = {
        'source': f'{selected_model}.pdf'
    }
    docs = manuals_store.similarity_search(query, k=10, filter=filter)
    print(f" ❎❎❎❎  Manual search results: {docs}")
    return "\n\n".join([doc.page_content for doc in docs])


@tool
def get_product_information(keywords: str) -> str:
    """
    Search specific product infromation based on keywords.

    Args:
        keywords (str): Keywords such as brand and model that user provided

    Returns:
        str: documents (scraped webpages) that match the keywords 
    """
    print(f" ❎❎❎❎  Calling get_product_information with keywords: {keywords}")
    results = products_store.similarity_search(keywords, 4)
    print(f" ❎❎❎❎  Product information search results: {results}")
    return results


@tool
def get_email_threads(email: str) -> str:
    """
    Search email conversation(s) based on email

    Args:
        email (str): Email of recipient or sender  

    Returns:
        str: the matching email conversations
    """
    print(f" ❎❎❎❎  Calling get_email_threads with email: {email}")
    threads = gmail.get_threads(email)
    print(f" ❎❎❎❎  Email threads found: {threads}")
    return threads


@tool
def get_email_threads_by_subject(subject: str) -> str:
    """
    Search email conversation(s) based on subject 

    Args:
        email (str): Email of recipient or sender  

    Returns:
        str: the matching email conversations
    """
    print(f" ❎❎❎❎  Calling get_email_threads_by_subject with subject: {subject}")
    threads = gmail.get_threads_by_subject(subject)
    print(f" ❎❎❎❎  Email threads by subject found: {threads}")
    return threads

@tool
def get_phone_conversation(number: str) -> str:
    """
    Search phone conversation transcript

    Args:
        phone number:

    Returns
        str: transcript of the conversation
    """
    print(f" ❎❎❎❎  Calling get_phone_conversation with number: {number}")
    transcript = openphone.search_transcript(number)
    print(f" ❎❎❎❎  Phone conversation transcript: {transcript}")
    return transcript

@tool
def get_draft_information(order_number: str) -> str:
    """
    Search Draft Orders / Quotes. These are not completed orders but quoted orders.

    Args:
        order_number (str): Draft order id/number. Usually XXXX or DXXXX

    Returns:
        str: Draft order information
    """
    print(f" ❎❎❎❎  Calling get_draft_information with order_number: {order_number}")
    shopify = Shopify()
    draft = shopify.draft_order(order_number)
    print(f" ❎❎❎❎  Draft order information: {draft}")
    return draft 

@tool
def create_draft_order(ids: list, email: str, phone: Optional[str] = None, 
                       first_name: Optional[str] = None, last_name: Optional[str] = None, 
                       province_code: Optional[str] = None) -> str:
    """
    Creates a draft order in Shopify by passing relevant customer information and product IDs.
    Make sure to have the ids before using this tool. You can get them using metadata tool

    Args:
        ids (list): List of product variant IDs to be added to the draft order.
        email (str): The email address of the customer.
        phone (Optional[str], optional): The phone number of the customer. Defaults to None.
        first_name (Optional[str], optional): The first name of the customer. Defaults to None.
        last_name (Optional[str], optional): The last name of the customer. Defaults to None.
        province_code (Optional[str], optional): The province code for the shipping address. Defaults to None.

    Returns:
        str: Information about the draft order, including success or failure message.
    """
    print(f" ❎❎❎❎  Calling create_draft_order with ids: {ids}, email: {email}, phone: {phone}, first_name: {first_name}, last_name: {last_name}, province_code: {province_code}")
    # Instantiate Shopify class and call draft_order_create
    shopify = Shopify()
    draft_order = shopify.draft_order_create(ids, email, phone, first_name, last_name, province_code)
    print(f" ❎❎❎❎  Draft order created: {draft_order}")
    return draft_order

@tool
def use_style(style: Literal['Cristian']) -> str:
    """
    Get examples of style
    Args:
        style (str): Person's name who's style we are usoing 

    Returns:
        str: examples of persons style
    """
    print(f" ❎❎❎❎  Calling use_style with style: {style}")
    file_path = f'./data/{style.lower()}.json'

    try:
        # Try to open and read the JSON file
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            print(f" ❎❎❎❎  Style examples found: {data}")
            return '\n'.join(data)
    except Exception as e:
        logging.error(f"Error reading style file: {e}")
        return ""

def handle_get_product_info(tools_by_name, tool_calls):
    output_messages = []
    doc_ids = set()
    for tool_call in tool_calls:
        docs = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
        filtered_docs = [doc for doc in docs if doc.metadata['id'] not in doc_ids]
        [doc_ids.add(doc.metadata['id']) for doc in docs]

        if tool_call['name'] == 'get_product_metadata_information':
            content = []
            for doc in filtered_docs:
                metadata = doc.metadata
                title = metadata.get("title", "No Title")
                id = metadata.get("id", "No ID")
                price = metadata.get("price", "No Price")
                sku = metadata.get("sku", "No SKU")
                url = metadata.get("url", "No URL")

                formatted_doc = (
                    f"### Product: {title}\n"
                    f"- **ID:** {id}\n"
                    f"- **Price:** {price}\n"
                    f"- **SKU:** {sku}\n"
                    f"- **Link:** [View Product]({url})\n"
                )
                content.append(formatted_doc)

            formatted_content = "\n\n".join(content)
            print(f" ❎❎❎❎  Product metadata information: {formatted_content}")

            output_messages.append(
                ToolMessage(
                    content=formatted_content,
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        else:
            print(f" ❎❎❎❎  Product information: {filtered_docs}")
            output_messages.append(
                ToolMessage(
                    content="\n\n".join([doc.page_content for doc in filtered_docs]),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
    return {"messages": output_messages}

@tool
def add_timeline_event(email: str, timeline_comment: str) -> str:
    """
    Add timeline comment such as conversation summary or other thing about interactions with the customer. 

    Args:
        email (str): customers email
        timeline_comment (str): comment/summary/event to add to crm timeline

    Returns:
        str: email of the customer if succesfull
    """
    print(f" ❎❎❎❎  Calling add_timeline_event with email: {email}, timeline_comment: {timeline_comment}")
    crm = NotionCRM()
    customer = crm.get_one(email)
    crm.add_comment(customer['id'], timeline_comment)
    print(f" ❎❎❎❎  Timeline event added for customer: {email}")
    return email

safe_tools = [
    find_order_information,
    find_email_threads_with_order,
    get_product_metadata_information,
    get_product_information,
    get_email_threads,
    get_email_threads_by_subject,
    get_information_from_manual,
    get_draft_information,
    use_style,
    get_phone_conversation 
]

sensitive_tools = [
    create_draft_order,
    add_customer_to_crm,
]

sensitive_tool_names = {t.name for t in sensitive_tools}

def call_tool(state: MessagesState):
    tools = safe_tools + sensitive_tools
    tools_by_name = {tool.name: tool for tool in tools}
    messages = state["messages"]
    last_message = messages[-1]
    output_messages = []

    tool_calls = [tool_call['name'] for tool_call in last_message.tool_calls]
    if all(call == 'get_product_information' for call in tool_calls) or  all(call == 'get_product_metadata_information' for call in tool_calls):
        return handle_get_product_info(tools_by_name, last_message.tool_calls)

    for tool_call in last_message.tool_calls:
        try:
            tool_result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
            print(f" ❎❎❎❎  Tool {tool_call['name']} result: {tool_result}")
            output_messages.append(
                ToolMessage(
                    content=tool_result,
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )

        except Exception as e:
            logging.error(f"Error in tool {tool_call['name']}: {e}")
            output_messages.append(
                ToolMessage(
                    content="",
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                    additional_kwargs={"error": e},
                )
            )
    return {"messages": output_messages}

def get_confirmation(snapshot):
    prompt_line = "\nAnswer **yes** to confirm. Otherwise explain changes"
    if 'sensitive_tools' in  snapshot.next:
        try:
            tool_call = snapshot.values['messages'][-1].tool_calls[0]
            if tool_call['name'] == 'create_draft_order':
                lines = []
                ids = [str(id) for id in tool_call['args']['ids']]
                pr_docs = products_metadata_store.get(ids=ids) 

                if 'email' in tool_call['args']:
                    lines.append(f"**Email:** {tool_call['args']['email']}\n")
                if 'first_name' in tool_call['args'] or 'last_name' in tool_call['args']:
                    if 'first_name' in tool_call['args'] and 'last_name' in tool_call['args']:
                        name = f"{tool_call['args']['first_name']} {tool_call['args']['last_name']}"
                    elif 'first_name' in tool_call['args']:
                        name = tool_call['args']['first_name']
                    elif 'last_name' in tool_call['args']:
                        name = tool_call['args']['last_name']
                    lines.append(f"**Name:** {name}\n")
                if 'phone' in tool_call['args']:
                    lines.append(f"**Phone:**{tool_call['args']['phone']}\n")
                if 'province_code' in tool_call['args']:
                    lines.append(f"**Province:** {tool_call['args']['province_code']}\n")


                if 'metadatas' in pr_docs:
                    lines.append("**Products:**\n")  # Correct forma
                    for metadata in pr_docs['metadatas']:
                        lines.append(f"- {metadata['title']}\n")
                lines.append(prompt_line)
                confirmation = "".join(lines)
                print(f" ❎❎❎❎  Confirmation for create_draft_order: {confirmation}")
                return confirmation

            elif tool_call['name'] == 'add_customer_to_crm':
                lines = []
                if 'customer_name' in tool_call['args']:
                    lines.append(f"Name: {tool_call['args']['customer_name']}")
                if 'email' in tool_call['args']:
                    lines.append(f"Email: {tool_call['args']['email']}")
                if 'phone' in tool_call['args']:
                    lines.append(f"Phone: {tool_call['args']['phone']}")
                if 'next_follow_up' in tool_call['args']:
                    lines.append(f"Follow Up: {tool_call['args']['next_follow_up']}")
                if 'comment' in tool_call['args']:
                    lines.append(f"Comment: {tool_call['args']['comment']}")
                confirmation = "\n".join(lines)
                print(f" ❎❎❎❎  Confirmation for add_customer_to_crm: {confirmation}")
                return confirmation
        except Exception as e:
            logging.error(f"Error during confirmation: {e}")
            return "Unexpected error occurred during confirmation"
    return "Unexpected tool call"


