import os
import logging
from datetime import datetime
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

# 1. NEW: Professional directory check for Cloud Deployment
# We must create the folder BEFORE calling basicConfig
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 2. Setup Audit Logger (ONLY ONE CONFIG CALL)
# This will now safely create the file because the directory exists
logging.basicConfig(
    filename=os.path.join(log_dir, 'security_audit.log'), 
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
        """Logs security events for compliance."""
        timestamp = datetime.now().isoformat()
        logging.info(f"AUDIT | {timestamp} | Action: {action} | User: {user_id} | Status: SUCCESS")