from flask import Blueprint, jsonify, request, Response
from assistant import build_graph
import uuid
from langchain_core.messages import HumanMessage, ToolMessage
from langgraph.checkpoint.postgres import PostgresSaver
from app.models.Conversation import Conversation 
import threading
from app.models.db_pool import pool
from app.models.Graph import Graph
from app.routes.stream_response import stream_response
api_routes = Blueprint('api', __name__)

@api_routes.route('/', methods=['GET'])
def get_conversations():
    """Return all data."""
    conversations = Conversation.get()
    convos = [{'id': c[0], 'title': c[1]} for c in conversations]

    return jsonify(convos), 200

@api_routes.route('/<string:thread_id>', methods=['DELETE'])
def delete_task(thread_id):
    """Return all data."""
    Conversation.delete(thread_id)

    return jsonify({}), 200


@api_routes.route('/<string:thread_id>', methods=['GET'])
def get_conversation(thread_id):
    serialized, confirmation = Graph.get_graph(thread_id)
    if serialized is None:
        return jsonify({'message': 'conversation not found'}), 404  
    payload = {'messages': serialized, 'id': thread_id}
    if confirmation:
        payload['confirmation'] = confirmation
    return jsonify(payload), 200

@api_routes.route('/', methods=['POST'])
def create_conversation():
    thread_id = str(uuid.uuid4())

    config = {"configurable": {"thread_id": thread_id}}
    data = request.json
    message = data.get('message')
    model = data.get('model')
    if not message:
        return jsonify({'message': 'Message field is required'}), 400
    
    db_thread = threading.Thread(target=Conversation.create_with_ai, args=(thread_id, message))
    db_thread.start()

    return Response(
            stream_response(message, model, config),
            content_type='application/json'
        )


@api_routes.route('/<string:thread_id>', methods=['POST'])
def update_conversation(thread_id):
    data = request.json
    message = data.get('message')
    model = data.get('model') 
    if not message:
        return jsonify({'message': 'Message field is required'}), 400

    with pool.connection() as conn:
        checkpointer = PostgresSaver(conn)
        graph = build_graph(checkpointer, model)
        
        config = {"configurable": {"thread_id": thread_id}}
        snapshot = graph.get_state(config)
        if 'sensitive_tools' in snapshot.next:
            if message == "yes":
                message = None
            else:
                message = [ToolMessage(tool_call_id=snapshot.values['messages'][-1].tool_calls[0]["id"],content="Tool call cancelled"),
                           HumanMessage(content=message)]

        else:
            message = HumanMessage(content=message)
    
    return Response(
            stream_response(message, model, config),
            content_type='application/json'
        )
