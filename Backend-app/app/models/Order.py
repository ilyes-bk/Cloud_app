import threading
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from app.models.db_pool import pool
class OrderModel:
    def __init__(self):
        """Initialize the connection using the database URL."""
        pass
    def initialize_table(self):
        """Initialize the table if it doesn't already exist."""
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS Orders(
            id VARCHAR PRIMARY KEY,
            name TEXT,
            email TEXT,
            order_number TEXT,
            created_at TIMESTAMP DEFAULT NOW(),
            comments TEXT
        );
        '''
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(create_table_query)
                conn.commit()
                print("Table initialized.")
    
    def create(self, id, name, order_number, email, comments):
        """Insert a new record into the table."""
        insert_query = '''
        INSERT INTO Orders (id, name, order_number, email, comments) VALUES (%s, %s, %s, %s, %s);
        '''
        try:
            with pool.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(insert_query, (id, name, order_number, email, comments))
                    conn.commit()
        except Exception as e:
            print(f"Error: {e} (Order with id {id} might already exist)")
    

    def get_order(self, email=None, order_number=None, comment_id=None):
        """Get orders based on one provided condition (email, order_number, or comment_id)."""
        if sum([bool(email), bool(order_number), bool(comment_id)]) != 1:
            raise ValueError("You must provide exactly one of 'email', 'order_number', or 'comment_id'.")

        query = "SELECT * FROM Orders WHERE "
        params = []

        if email:
            query += "email = %s"
            params.append(email)
        elif order_number:
            query += "order_number = %s"
            params.append(order_number)
        elif comment_id:
            query += "comments LIKE %s"
            params.append(f'%{comment_id}%')
        with psycopg2.connect(os.environ['DATABASE_URL']) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, tuple(params))
                results = cur.fetchall()
                if len(results) > 0:
                    order = results[0]
                    order['created_at'] = order['created_at'].strftime("%Y-%m-%d %H:%M:%S")
                    return results[0]
        return results
    
    def delete(self, id):
        """Delete an order based on the provided id."""
        if not id:
            raise ValueError("You must provide the 'id' of the order to delete.")

        query = "DELETE FROM Orders WHERE id = %s"
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (id,))
                conn.commit()
            

Order = OrderModel()
Order.initialize_table()
