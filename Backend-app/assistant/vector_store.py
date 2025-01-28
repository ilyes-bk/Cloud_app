import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import tiktoken
import time
import shutil
STORE_DIR = 'stores'
TOKEN_LIMIT_PER_MINUTE = 900_000

def count_tokens(text, model = 'text-embedding-3-small'):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))
    
def batchify(docs, batch_size):
    for i in range(0, len(docs), batch_size):
        yield docs[i:i+batch_size]
        
def init_chroma_vector_store(docs, BATCH_SIZE=200, filename='test'):
    path = os.path.join(STORE_DIR, filename)
    
    if os.path.exists(path):
        print(f"Store exists. Deleting existing data at {path}...")
        shutil.rmtree(path)
    

    embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
    vector_store = None
    total_tokens = 0
    start_time = time.time()
    
    for batch in batchify(docs, BATCH_SIZE):
        batch_tokens = sum(count_tokens(doc.page_content) for doc in batch)
        total_tokens += batch_tokens

        if total_tokens >= TOKEN_LIMIT_PER_MINUTE:
            elapsed_time = time.time() - start_time
            if elapsed_time < 60:
                time_to_sleep = 60 - elapsed_time
                print(f"Token limit reached. Sleeping for {time_to_sleep:.2f} seconds...")
                time.sleep(time_to_sleep)
            
            total_tokens = 0
            start_time = time.time()

        bids = [b.id for b in batch]
        
        if vector_store is None:
            vector_store = Chroma.from_documents(batch, embeddings, persist_directory=path, ids=bids)
        else:
            vector_store.add_documents(batch, ids=bids)
     
    return vector_store
    
def list_vector_stores():
    stores = os.listdir(os.path.join(STORE_DIR))
    return stores

def load_vector_store(filename):
    path = os.path.join(STORE_DIR, filename)
    if not os.path.exists(path):
       print(f"Vector store not found in directory: {path}")
       return None
    else:
        embeddings = OpenAIEmbeddings(model = 'text-embedding-3-small')
        
        vector_store = Chroma(embedding_function=embeddings, persist_directory=path)
        
        print(f"Vector store loaded from directory: {path}")
        
        return vector_store
