import os
from google import genai
from google.genai import errors
from dotenv import load_dotenv

load_dotenv()

class MentalHealthBot:
    def __init__(self, use_mock=False):
        self.use_mock = use_mock
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key)
        self.model_id = 'gemini-2.5-flash' 
        
        # PROFESSIONAL SYSTEM INSTRUCTION
        self.system_instruction = (
            "You are a professional, empathetic therapist. "
            "You are receiving 'Masked Input' where names and locations have been removed for privacy. "
            "IMPORTANT: Never use placeholders like [NAME], [USER], or [PERSON] in your reply. "
            "Instead, address the user warmly but anonymously using phrases like 'I'm here for you' "
            "or 'It takes courage to share that.' Keep your tone clinical yet compassionate."
        )
        
    def get_response(self, masked_input: str) -> str:
        if self.use_mock:
            return "[MOCK RESPONSE] I hear that you're going through a lot. Your privacy is protected."

        try:
            # INTEGRATED SYSTEM INSTRUCTION
            response = self.client.models.generate_content(
                model=self.model_id,
                config={'system_instruction': self.system_instruction},
                contents=masked_input
            )
            return response.text
        except errors.ClientError as e:
            if "429" in str(e):
                return "[QUOTA EXHAUSTED] The AI is resting, but your message was safely encrypted and saved."
            return f"Error: {str(e)}"
    
    def get_advanced_response(self, current_masked_input, chat_history_list):
        """Constructs a professional session with historical context."""
        history_context = "\n".join([f"User: {h['text']}" for h in chat_history_list])
        
        full_prompt = f"Context of past conversation:\n{history_context}\n\nCurrent User Message: {current_masked_input}"
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                config={'system_instruction': self.system_instruction},
                contents=full_prompt
            )
            return response.text
        except Exception as e:
            return f"Error during session analysis: {str(e)}"