from app.models.db_pool import pool
from langgraph.checkpoint.postgres import PostgresSaver
from assistant import build_graph, get_confirmation

class Graph:
    @staticmethod
    def get_graph(thread_id):
        with pool.connection() as conn:
            checkpointer = PostgresSaver(conn)
            graph = build_graph(checkpointer)
            config = {"configurable": {"thread_id": thread_id}}
            snapshot = graph.get_state(config)
            if snapshot.created_at is None:
                return None
            serialized = [msg.dict() for msg in snapshot.values['messages']]
            if "sensitive_tools" in snapshot.next:
                return serialized, get_confirmation(snapshot)
            return serialized, None