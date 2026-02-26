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
        
    def get_response(self, masked_input: str) -> str:
        if self.use_mock:
            return "[MOCK RESPONSE] I hear that you're going through a lot. Your privacy is protected, and I'm here to listen."

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=f"Supportive AI: {masked_input}"
            )
            return response.text
        except errors.ClientError as e:
            if "429" in str(e):
                return "[QUOTA EXHAUSTED] The AI is resting, but your message was safely encrypted and saved to the database."
            return f"Error: {str(e)}"
    
    def get_advanced_response(self, current_masked_input, chat_history_list):
        # Construct a memory block
        history_context = "\n".join([f"User: {h['text']}" for h in chat_history_list])
        
        full_prompt = f"""
        You are a professional therapist. 
        Context of past conversation:
        {history_context}
        
        Current User Message: {current_masked_input}
        """
        # Send to Gemini...