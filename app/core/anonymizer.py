import re

class ProfessionalAnonymizer:
    def __init__(self):
        # Professional-grade patterns for PII
        self.patterns = {
            "NAME": r"(?i)(my name is|i am|i'm|this is) ([A-Z][a-z]+)",
            "LOCATION": r"(?i)(lives in|from|at) ([A-Z][a-z]+)",
            "EMAIL": r"[\w\.-]+@[\w\.-]+\.\w+",
            "PHONE": r"\b\d{10}\b"
        }

    def scrub_data(self, text: str) -> str:
        """The professional method to mask PII."""
        masked_text = text
        for label, pattern in self.patterns.items():
            masked_text = re.sub(pattern, f"[{label}]", masked_text)
        return masked_text