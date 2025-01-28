from app.routes.create_title import create_title
from app.models.db_pool import pool
class ConversationModel:
    def __init__(self):
        """Initialize the connection using the database URL."""
        pass
    def initialize_table(self):
        """Initialize the table if it doesn't already exist."""
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS conversations (
            id VARCHAR PRIMARY KEY,
            title VARCHAR,
            created_at TIMESTAMP DEFAULT NOW()
        );
        '''
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(create_table_query)
                conn.commit()
    
    def create(self, record_id, title):
        """Insert a new record into the table."""
        insert_query = '''
        INSERT INTO conversations (id, title) VALUES (%s, %s);
        '''
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(insert_query, (record_id, title))
                    conn.commit()
                    print(f"Record with id {record_id} created.")
        except Exception as e:
            print(f"Error: {e} (Record with id {record_id} might already exist)")

    def create_with_ai(self, record_id, usr_msg):
        """Insert a new record into the table."""
        insert_query = '''
        INSERT INTO conversations (id, title) VALUES (%s, %s);
        '''

        title = create_title(usr_msg)
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(insert_query, (record_id, title))
                    conn.commit()
                    print(f"Record with id {record_id} created.")
        except Exception as e:
            print(f"Error: {e} (Record with id {record_id} might already exist)")
        
    def delete(self, id):
        delete_query = '''
        DELETE FROM conversations WHERE id = %s;;
        '''
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(delete_query, (id,))
                    conn.commit()
        except Exception as e:
            print(f"Error: {e} (Record with id {id} )")


    def get(self):
        """Retrieve a maximum of 50 titles."""
        get_titles_query = '''
        SELECT id, title FROM conversations ORDER BY created_at DESC LIMIT 50;
        '''
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(get_titles_query)
                results = cur.fetchall()
                return results
            
Conversation = ConversationModel()
Conversation.initialize_table()
