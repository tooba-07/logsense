# LogSense — Security Log Anomaly Explainer


**Live Demo:** [https://itstooba07.pythonanywhere.com](https://itstooba07.pythonanywhere.com)  
**GitHub Repo:** [https://github.com/tooba-07/logsense](https://github.com/tooba-07/logsense)  

## 📖 What is LogSense?
LogSense is a complete, end-to-end web application designed for cybersecurity students and beginner SOC analysts. 

**The problem:** Raw security logs are filled with cryptic timestamps and IP addresses, making them difficult for beginners to interpret.  
**The solution:** LogSense combines rule-based detection with AI-generated explanations. Students can upload authentication logs, instantly see which events are suspicious, and receive plain-language explanations of *why* each event is a threat. 

## 🎯 Target Audience
This tool is built specifically for **cybersecurity students** and entry-level analysts who are learning to identify brute-force attacks, impossible travel patterns, and off-hours login anomalies in a real-world environment.

## ✨ What it does
- **Rule-Based Detection:** Automatically detects brute-force login attempts (7+ failed logins in 10 minutes), odd-hour logins (outside business hours), and impossible travel patterns.
- **AI-Powered Explanations:** Uses Groq's Llama 3.3 model to translate flagged events into simple, easy-to-understand sentences.
- **Data Persistence:** Stores logs and flagged incidents in a local SQLite database.
- **Interactive Dashboard:** Displays flagged incidents in a clean, dark-themed table with severity ratings (High/Medium) and expandable AI explanations.
- **Seamless Upload:** Users can upload their CSV log files directly via a simple web interface.

## 🤖 The AI Feature
When a log entry is flagged by the rule-based engine, LogSense sends the data to the **Groq API** using the `llama-3.3-70b-versatile` model.

**The system prompt used to generate explanations:**
> *"You are a SOC analyst assistant helping a cybersecurity student. In 2-3 simple sentences, explain why Log: username={username}, ip={ip_address}, time={timestamp}, event={event_type} Flag reason: {reason}"*

The model returns a natural-language explanation, which is stored in the database and displayed alongside the incident on the dashboard.

## 🛠️ Tech Stack
- **Backend:** Python, Flask
- **Database:** SQLite
- **AI Model:** Groq API (Llama 3.3)
- **Frontend:** HTML, CSS, JavaScript
- **Hosting:** PythonAnywhere


## Screenshots

![Dashboard with upload form](screenshots/dashboard.png)<img width="959" height="449" alt="dashboard" src="https://github.com/user-attachments/assets/cd87d3a7-5b6f-4929-95de-d7d06ed95a5a" />

![Flagged incidents list with AI explanation expanded](screenshots/incident-list.png)<img width="959" height="539" alt="incident-list" src="https://github.com/user-attachments/assets/b9b8d690-3fe5-4050-8297-4d21c55a27e8" />

![AI explanation view](screenshots/screenshot-3.png)<img width="944" height="445" alt="screenshot3" src="https://github.com/user-attachments/assets/2ea900e3-2e02-4c9c-a961-8b8eea082e13" />


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


## 📝 License & Status

**Status:** Fully functional, deployed, and ready for evaluation.

**License:** This project is developed as an individual final assignment for the ACT AI National Initiative program (MUET, Jamshoro). Open-source for academic review only. Not permitted for commercial redistribution without author consent.

**Submission:** Submitted to QuizyHub (MUET) for the Final Project — Ship Your AI App.

**Attribution:**
- **Developer:** Tooba Asif
- **Institution:** Mehran University of Engineering & Technology (MUET), Jamshoro
- **Program:** ACT AI National Initiative (AI SkillBridge, HEC, and NAVTTC)
