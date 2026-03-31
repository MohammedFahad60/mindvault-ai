from flask import Flask, render_template, request, jsonify
import os
from core.security import DataShield
from core.anonymizer import ProfessionalAnonymizer # Use ONLY the class
from core.ai_engine import MentalHealthBot
from database.models import ChatDatabase

# 1. Initialize the Flask App
app = Flask(__name__)

# 2. Initialize our Professional Logic Classes
shield = DataShield()
anonymizer = ProfessionalAnonymizer() 
bot = MentalHealthBot()
db = ChatDatabase()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("message")
    user_id = "student_001" 

    # A. PRIVACY: Professional PII Masking
    # This removes names/locations before Gemini sees it
    masked_text = anonymizer.scrub_data(user_input) 
    
    # B. AI: Get Response from Gemini 2.5 Flash
    ai_reply = bot.get_response(masked_text)
    
    # C. SECURITY: Encrypt the RAW message for the DB
    # We save the original (encrypted) so the user can see their history later
    encrypted_msg = shield.encrypt_message(user_input)
    
    # D. AUDIT: Log the transaction (HIPAA Requirement)
    shield.audit_access("MESSAGE_STORED", user_id) 
    
    # E. PERSISTENCE: Save to SQLite
    db.save_message(user_id, encrypted_msg)
    
    return jsonify({
        "reply": ai_reply,
        "status": "encrypted_and_saved"
    })
    
@app.route('/history', methods=['GET'])
def get_history():
    user_id = "student_001"
    raw_history = db.get_user_history(user_id)
    
    decrypted_history = []
    for encrypted_content, timestamp in raw_history:
        try:
            # Securely decrypt for the user's view
            text = shield.decrypt_message(encrypted_content)
            decrypted_history.append({"text": text, "time": timestamp})
        except Exception:
            continue
            
    return jsonify(decrypted_history)

if __name__ == '__main__':
    print("Starting Mental Health Vault Pro on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)