from flask import Blueprint, jsonify, request, Response
from assistant import build_transcript_graph, build_graph 
from app.models.Graph import Graph
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import HumanMessage, ToolMessage, AIMessageChunk
from app.models.Task import Task 
from app.models.db_pool import pool
from lib import write_follow_ups
import threading
from app.routes.stream_response import stream_response
task_routes = Blueprint('task', __name__)
follow_up_thread = None

@task_routes.route('/', methods=['POST'])
def action_route():
    action = request.args.get("action")
    if action == "DELETE_FOLLOW_UPS":
        Task.delete_by_type("FOLLOW-UP")
    elif action == "CREATE_FOLLOW_UPS":
        global follow_up_thread
        if follow_up_thread and follow_up_thread.is_alive():
            return jsonify({"message": "Already running"}), 200
        follow_up_thread = threading.Thread(target=write_follow_ups)
        follow_up_thread.start()
        return jsonify({"message": "Follow-up creation started"}), 200

    return jsonify({'message': "Success"}), 200

@task_routes.route('/', methods=['GET'])
def get_conversations():
    """Return all data."""
    conversations = Task.get()
    convos = [{'id': c[0], 'title': c[1]} for c in conversations]

    return jsonify(convos), 200



@task_routes.route('/<string:thread_id>', methods=['DELETE'])
def delete_task(thread_id):
    """Return all data."""
    Task.delete(thread_id)

    return jsonify({}), 200


@task_routes.route('/<string:thread_id>', methods=['GET'])
def get_conversation(thread_id):
    serialized, confirmation = Graph.get_graph(thread_id)
    if serialized is None:
        return jsonify({'message': 'conversation not found'}), 404  
    payload = {'messages': serialized, 'id': thread_id}
    if confirmation:
        payload['confirmation'] = confirmation
    return jsonify(payload), 200


@task_routes.route('/<string:thread_id>', methods=['POST'])
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
                message = ToolMessage(tool_call_id=snapshot.values['messages'][-1].tool_calls[0]["id"],
                                        content=f"Tool call canceled. Ask further instructions.")
        else:
            message = HumanMessage(content=message)
    
    return Response(
            stream_response(message, model, config),
            content_type='application/json'
        )


