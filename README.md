# 🛡️ MindVault: Secure AI Mental Health Companion
**A HIPAA-Aware AI Companion built for the 8th Sem Capstone Project at APS Engineering College.**

## 🚀 Overview
MindVault is a security-focused mental health chatbot that leverages **Gemini 2.5 Flash** for empathy and **AES-256 Encryption** for data privacy. 

## ✨ Key Features
* **PII Masking:** Uses Microsoft Presidio to scrub names and locations before AI analysis.
* **Vault Storage:** Conversations are encrypted at rest using Fernet (AES-256).
* **Audit Logging:** Full security audit trails for compliance.
* **Glassmorphism UI:** Premium dark-mode dashboard for enhanced user experience.

## 🛠️ Tech Stack
* [cite_start]**Backend:** Python (Flask) [cite: 29]
* **AI:** Google Gemini 2.5 SDK
* **Security:** Cryptography.py, Microsoft Presidio
* **Database:** SQLite

## 🚦 Quick Start
1. Clone the repo: `git clone https://github.com/MohammedFahad60/mindvault-ai.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your `.env` with `GEMINI_API_KEY`
4. Run: `python -m app.main`