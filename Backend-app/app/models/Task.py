from app.models.db_pool import pool
class TaskModel:
    def __init__(self):
        """Initialize the connection using the database URL."""
        pass
    def initialize_table(self):
        """Initialize the table if it doesn't already exist."""
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS tasks (
            id VARCHAR PRIMARY KEY,
            title VARCHAR,
            created_at TIMESTAMP DEFAULT NOW(),
            handled BOOLEAN DEFAULT FALSE,
            type VARCHAR
        );
        '''
        with pool.connection() as conn: 
            with conn.cursor() as cur:
                cur.execute(create_table_query)
                conn.commit()

    def delete(self, id):
        """Delete row from table."""
        delete_query = '''
        DELETE FROM tasks WHERE id = %s;
        '''
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(delete_query, (id,))
                    conn.commit()
        except Exception as e:
            print(f"Error: {e} (Record with id {id} )")

    def delete_by_type(self, type):
        """Delete row from table."""
        delete_query = '''
        DELETE FROM tasks WHERE type = %s;
        '''
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(delete_query, (type,))
                    conn.commit()
            
        except Exception as e:
            print(f"Error: {e} (Record with id {id} )")

    def create(self, record_id, title, task_type):
        """Insert a new record into the table."""
        insert_query = '''
        INSERT INTO tasks (id, title, type) VALUES (%s, %s, %s);
        '''
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(insert_query, (record_id, title, task_type,))
                    conn.commit()
                    print(f"Record with id {record_id} created.")
            
        except Exception as e:
            print(e)

    def get(self):
        """Retrieve a maximum of 50 titles."""
        get_titles_query = '''
        SELECT id, title FROM tasks ORDER BY created_at DESC LIMIT 300;
        '''
        with pool.connection() as connection:
            with connection.cursor() as cur:
                cur.execute(get_titles_query)
                results = cur.fetchall()
                return results
            
Task = TaskModel()
Task.initialize_table()
