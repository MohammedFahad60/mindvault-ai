import sqlite3
from datetime import datetime

class ChatDatabase:
    def __init__(self, db_name="mental_health_vault.db"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        """Creates the messages table if it doesn't exist."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                encrypted_content TEXT,
                timestamp TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def save_message(self, user_id, encrypted_text):
        """Saves a single encrypted message to the DB."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO messages (user_id, encrypted_content, timestamp) VALUES (?, ?, ?)",
            (user_id, encrypted_text, now)
        )
        conn.commit()
        conn.close()

    def get_user_history(self, user_id):
        """Retrieves all encrypted messages for a specific user."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT encrypted_content, timestamp FROM messages WHERE user_id = ?", (user_id,))
        history = cursor.fetchall()
        conn.close()
        return history