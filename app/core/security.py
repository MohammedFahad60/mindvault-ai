import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import logging
from datetime import datetime

# Setup Audit Logger
logging.basicConfig(filename='logs/security_audit.log', level=logging.INFO)

load_dotenv()

LOG_DIR = 'logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'security_audit.log'), 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DataShield:
    def __init__(self):
        key = os.getenv("ENCRYPTION_KEY")
        if not key:
            raise ValueError("No ENCRYPTION_KEY found in .env file!")
        self.cipher = Fernet(key.encode())

    def encrypt_message(self, plain_text: str) -> str:
        """Encrypts sensitive data for the database."""
        return self.cipher.encrypt(plain_text.encode()).decode()

    def decrypt_message(self, encrypted_text: str) -> str:
        """Decrypts data for application use."""
        return self.cipher.decrypt(encrypted_text.encode()).decode()
    
    def audit_access(self, action, user_id):
        timestamp = datetime.now().isoformat()
        logging.info(f"AUDIT | {timestamp} | Action: {action} | User: {user_id} | Status: SUCCESS")