# LogSense — Security Log Anomaly Explainer

A tool that reads security login logs, automatically detects suspicious patterns using rules, then uses AI to explain why each one is suspicious — built with a real database behind it.

**Developed by:** Tooba Asif
**Program:** ACT AI National Initiative (in collaboration with AI SkillBridge, HEC, and NAVTTC)
**Background:** Cyber Security student, Mehran University of Engineering and Technology (MUET), Jamshoro

## What it does
- Detects brute-force login attempts, odd-hour logins, and impossible travel patterns
- Uses Groq's Llama model to generate plain-language explanations for each flagged incident
- Stores logs and flagged incidents in MySQL
- Displays results on a clean dashboard

## Why this project
Reading raw security logs is hard for beginners in cybersecurity. LogSense bridges that gap by combining rule-based detection with AI-generated explanations, making log analysis approachable for students and SOC analysts alike.

## Tech Stack
- Backend: Python, Flask
- Database: MySQL
- AI: Groq API (Llama 3.3)
- Frontend: HTML/CSS/JS

## Setup
1. Install dependencies: `pip install flask mysql-connector-python groq python-dotenv`
2. Run `schema.sql` in MySQL to create tables
3. Add your Groq API key to a `.env` file as `GROQ_API_KEY=your-key`
4. Run `python app.py`
5. Open `http://127.0.0.1:5000`
