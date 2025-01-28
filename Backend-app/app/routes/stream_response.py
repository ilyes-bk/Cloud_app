from app.models.db_pool import pool
from langgraph.checkpoint.postgres import PostgresSaver
from assistant import build_graph
import json
from langchain_core.messages import HumanMessage, ToolMessage, AIMessageChunk
from assistant.tools import get_confirmation
def stream_response(input_message, model, config):
    if input_message is not None:
        if isinstance(input_message, list):
            input_message = {"messages": input_message}
        else:
            input_message = {"messages": [input_message]}

    with pool.connection() as conn:
        checkpointer = PostgresSaver(conn)
        graph = build_graph(checkpointer=checkpointer ,model=model)
        for _, update in graph.stream(input_message, config, stream_mode=["messages", "values"]):
            if isinstance(update, dict) and 'messages' in update:
                serialized = [msg.dict() for msg in update.get('messages', [])]
                yield json.dumps({'messages': serialized, 'id': config['configurable']['thread_id']}) + "|||"
            elif isinstance(update, tuple) and isinstance(update[0], AIMessageChunk):
                yield json.dumps({'chunk': update[0].content}) + "|||"
        snapshot = graph.get_state(config)
        if "sensitive_tools" in snapshot.next:
            yield json.dumps({'confirmation': get_confirmation(snapshot)}) + "|||"