# LogSense — Security Log Anomaly Explainer

A tool that reads security login logs, automatically detects suspicious patterns using rules, then uses AI to explain why each one is suspicious — built with a real database behind it.

**Developed by:** Tooba Asif
**Program:** ACT AI National Initiative (in collaboration with AI SkillBridge, HEC, and NAVTTC)
**Background:** Cyber Security student, Mehran University of Engineering & Technology (MUET), Jamshoro

## Live Demo
https://itstooba07.pythonanywhere.com

## What it does

- Detects brute-force login attempts, odd-hour logins, and impossible travel patterns
- Uses Groq's Llama 3.3 model to generate plain-language explanations for each flagged incident
- Stores logs and flagged incidents in a SQLite database
- Displays results on a clean dashboard with severity ratings (high/medium)

## Why this project

Reading raw security logs is hard for beginners in cybersecurity. LogSense bridges that gap by combining rule-based detection with AI-generated explanations, making log analysis approachable for students and SOC analysts alike.

## The AI feature

When a log entry is flagged by the rule-based detection (brute-force, odd-hour login, or impossible travel), LogSense sends the flagged entry to Groq's Llama 3.3 model (`llama-3.3-70b-versatile`) with the following prompt:

```
You are a SOC analyst assistant helping a cybersecurity student. In 2-3 simple sentences, explain why the following log entry is suspicious and what this type of activity typically indicates in a real environment.

Log: username={username}, ip={ip_address}, time={timestamp}, event={event_type}
Flag reason: {reason}
```

The model returns a plain-language explanation of why the pattern is suspicious, which is stored alongside the incident and displayed on the dashboard.

## Tech Stack

- Backend: Python, Flask
- Database: SQLite
- AI: Groq API (Llama 3.3)
- Frontend: HTML/CSS/JS
- Hosting: PythonAnywhere

## Screenshots

![Dashboard with upload form](screenshots/dashboard.png)
![Flagged incidents list with AI explanation expanded](screenshots/incident-list.png)
![Third screenshot — add one more before submitting](screenshots/screenshot-3.png)

## Setup — Run locally

1. Clone the repo:
   ```
   git clone https://github.com/tooba-07/logsense.git
   cd logsense
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Add your Groq API key to a `.env` file:
   ```
   GROQ_API_KEY=your-key-here
   ```

4. Run the app:
   ```
   python app.py
   ```

5. Open `http://127.0.0.1:5000` in your browser. The SQLite database (`logsense.db`) is created automatically on first run.
