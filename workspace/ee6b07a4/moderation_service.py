import datetime
import threading
from db_adapter import DatabaseAdapter

class ModerationService:
    def __init__(self, db_adapter: DatabaseAdapter):
        self.db_adapter = db_adapter
        self.lock = threading.Lock()

    def log_deletion(self, message_id, author_id, content, reason):
        # We can still keep local logging if needed, but here we prioritize DB
        with self.lock:
            self.db_adapter.log_to_db(message_id, author_id, content, reason)