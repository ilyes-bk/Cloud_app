from langgraph.graph import END, StateGraph, START, MessagesState
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import AnyMessage, add_messages
from typing_extensions import TypedDict
from typing import Annotated
from .tools import sensitive_tool_names, sensitive_tools, call_tool
from .tools import *
from .assistant import Assistant, runnable_assistant, transcript_assistant

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    
def route_tools(state: State):
    next_node = tools_condition(state)
    if next_node == END:
        return END
    ai_message = state["messages"][-1]
    first_tool_call = ai_message.tool_calls[0]
    if first_tool_call["name"] in sensitive_tool_names:
        return "sensitive_tools"
    return "safe_tools"


def build_graph(checkpointer=None, model="gpt-4o-mini"):
    
    sensitive_tools = [
    add_customer_to_crm,
    create_draft_order
]
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
    builder = StateGraph(State)

    builder.add_node("assistant", Assistant(runnable_assistant(model, sensitive_tools + safe_tools)))
    builder.add_node("safe_tools", call_tool)
    builder.add_node("sensitive_tools", ToolNode(sensitive_tools))
    builder.add_edge(START, "assistant")
        
    builder.add_conditional_edges(
        "assistant", route_tools, ["safe_tools", "sensitive_tools", END]
    )

    builder.add_edge("safe_tools", "assistant")
    builder.add_edge("sensitive_tools", "assistant")

    graph = builder.compile(
        checkpointer=checkpointer,
        interrupt_before=["sensitive_tools"])
    return graph

def build_transcript_graph(checkpointer, model="gpt-4o-mini"):

    sensitive_tools = [
    ]

    builder = StateGraph(State)
    builder.add_node("assistant", Assistant(transcript_assistant(model, sensitive_tools)))
    builder.add_node("safe_tools", call_tool)
    builder.add_node("sensitive_tools", ToolNode(sensitive_tools))
    builder.add_edge(START, "assistant")

    builder.add_conditional_edges(
        "assistant", route_tools, ["safe_tools", "sensitive_tools", END]
    )
    builder.add_edge("safe_tools", "assistant")
    builder.add_edge("sensitive_tools", "assistant")

    graph = builder.compile(
        checkpointer=checkpointer,
        interrupt_before=["sensitive_tools"])
    return graph
