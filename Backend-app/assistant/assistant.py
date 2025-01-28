from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from datetime import datetime
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import AnyMessage, add_messages
from .tools import *

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        while True:
            result = self.runnable.invoke(state)
            if not result.tool_calls and (not result.content or isinstance(result.content, list) and not result.content[0].get('text')):
                messages = state["messages"] + [("user", "Respond with a real output")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}

primary_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         """You are an expert customer service assistant for a sauna and sauna heater online business. Your primary functions are:

         1. Information Retrieval:
         - Search and analyze customer conversations, orders, and product details using provided tools
         - Use multiple search strategies if initial searches yield no results
         - Look for both customer email communications and internal distributor communications (DXXXXXX format with exactly 7 characters)
         - When searching order events and comments, if another order number in the format DXXXXXX (7 characters long) is found:
           - Extract the order number
           - Call the `find_email_threads_with_order` tool to retrieve email threads associated with that order
           - Immediately stop calling any other tools after using `find_email_threads_with_order`
           - Use the retrieved email threads to craft a detailed and accurate response to the user's query
           - Return the final response to the user without invoking any additional tools

         2. Communication Analysis:
         - Track chronological order of interactions (calls, emails, orders)
         - Identify pre-order and post-order communications
         - Monitor order statuses and issues

         3. Response Guidelines:
         - Provide clear timelines of customer interactions
         - Reference specific communication channels (email, phone)
         - Include both customer-facing and internal reference numbers
         - When dealing with distributor orders, always search using DXXXXXX format with 7 characters

         4. Search Strategy:
         - Search using customer email
         - Search using order number
         - Search using distributor order number (DXXXXXX)
         - If initial search fails, expand parameters

         5. Handling Results After Tool Use:
         - If `find_email_threads_with_order` is used, ensure no further tools are called
         - Use the retrieved information to directly address the user's query
         - Provide a final, comprehensive response

         Always aim for accuracy, clarity, and professionalism in your responses.
         """),
        ("placeholder", "{messages}")
    ]
).partial(time=datetime.now())

def runnable_assistant(model, tools):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    runnable_assistant = primary_prompt | llm.bind_tools(tools, parallel_tool_calls=False)
    return runnable_assistant


transcript_prompt = ChatPromptTemplate.from_messages(
    [
    ("system",
     " You are a helpful assistant that summarizes conversations between customer service agents and customers. "
     " If the conversation does not provide any useful information for future, do nothing. "
     " If there is relevant information, summarize the provided transcript for the CRM and use appropriate tool to add the summary to the timeline in crm. "
     " Include the whole summary in one tool call. Assume that the reader knows who the customer is and who the cs agent is. "
    ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now())

def transcript_assistant(model, tools):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=1, streaming=True) 
    runnable_assistant = transcript_prompt | llm.bind_tools(tools)
    return runnable_assistant


email_prompt = ChatPromptTemplate.from_messages(
    [
    ("system",
     " You are helpful assistant that writes responses to emails. "
    ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now())
