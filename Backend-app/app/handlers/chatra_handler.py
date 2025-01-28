from app.subscribers.chatra_subscriber import ChatraSubscriber
from apis.notionCRM import NotionCRM
import uuid
from langgraph.checkpoint.postgres import PostgresSaver
from app.models.Task import Task 
from psycopg import Connection
from langchain_core.messages import HumanMessage
from assistant import build_transcript_graph 
DATABASE_URL="postgresql://miikatuomela@localhost:5432/gpt"
from time import sleep
connection_kwargs = {
    "autocommit": True,
    "prepare_threshold": 0,
}
def chatra_handler():
    chatra_sub = ChatraSubscriber()
    crm = NotionCRM()
    while True:
        ack_ids, convos = chatra_sub.pull_transcripts()
        for c in convos:
            name = c['client']['basicInfo'].get('name', None)
            email = c['client']['basicInfo'].get('email', None)
            transcript_lines = []
    
            if email is not None:
                for m in c['messages']:
                    if m['type'] == 'agent':
                        # Append agent messages with the agent's name
                        transcript_lines.append(f"{m['agentName']}: {m['message']}")
                    else:
                        # Append customer messages, using 'name' if available
                        if name is not None:
                            transcript_lines.append(f"{name}: {m['message']}")
                        else:
                            transcript_lines.append(f"Customer: {m['message']}")
                transcript = "\n".join(transcript_lines)

                message = f"Email: {email}\nTranscript: {transcript}"

                customer = crm.get_one(email) 
                print("Customer", customer)
                if customer is None:
                    pass
                    #customer = crm.add(name, email)
                thread_id = str(uuid.uuid4())
                config = {"configurable": {"thread_id": thread_id}}
                Task.create(thread_id, "Chatra summary for: " + email)
                with Connection.connect(DATABASE_URL, **connection_kwargs) as conn:
                    checkpointer = PostgresSaver(conn)
                    input_message = HumanMessage(content=message)
                    graph = build_transcript_graph(checkpointer)
                    graph.invoke({"messages": [input_message]}, config, stream_mode="values")
        if len(ack_ids) != 0:
            pass
            #chatra_sub.ack_transcripts(ack_ids) 
        sleep(30)
