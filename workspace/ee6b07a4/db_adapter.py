import psycopg2
from psycopg2 import sql

class DatabaseAdapter:
    def __init__(self, db_config):
        self.config = db_config

    def log_to_db(self, message_id, author_id, content, reason):
        conn = psycopg2.connect(**self.config)
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO moderation_logs (message_id, author_id, content, reason) VALUES (%s, %s, %s, %s)",
                    (message_id, author_id, content, reason)
                )
                conn.commit()
        finally:
            conn.close()