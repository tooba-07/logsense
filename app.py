"""
LogSense - Log Anomaly Explainer
Flask app: handles log upload, runs detection rules,
calls Claude API for explanations, stores results in MySQL.
"""
from dotenv import load_dotenv
load_dotenv()

import os
import csv
import io
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template
import mysql.connector
from groq import Groq

app = Flask(__name__)

# ---------- CONFIG ----------
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "database": os.environ.get("DB_NAME", "logsense"),
}

# Set your Groq API key as an environment variable: Groq_API_KEY
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))  # reads Groq_API_KEY from environment automatically


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ---------- DETECTION RULES ----------
# Each function takes the full list of log rows and returns a list of
# (log_row, reason, severity) tuples for anything it flags.

def detect_brute_force(logs):
    """Flag if same IP has >5 failed_login events within a 10-minute window."""
    flagged = []
    failed_by_ip = {}
    for log in logs:
        if log["event_type"] != "failed_login":
            continue
        failed_by_ip.setdefault(log["ip_address"], []).append(log)

    for ip, attempts in failed_by_ip.items():
        attempts.sort(key=lambda x: x["timestamp"])
        for i in range(len(attempts)):
            window = [a for a in attempts if 0 <= (a["timestamp"] - attempts[i]["timestamp"]).total_seconds() <= 600]
            if len(window) > 5:
                for a in window:
                    flagged.append((a, f"Brute force pattern: {len(window)} failed logins from {ip} within 10 minutes", "high"))
                break  # avoid duplicate flags for the same cluster
    return flagged


def detect_odd_hour_login(logs):
    """Flag successful logins between 1 AM and 5 AM."""
    flagged = []
    for log in logs:
        if log["event_type"] == "successful_login" and 1 <= log["timestamp"].hour < 5:
            flagged.append((log, f"Login at unusual hour ({log['timestamp'].strftime('%H:%M')}) for user {log['username']}", "medium"))
    return flagged


def detect_new_ip(logs):
    """Flag a successful login from an IP not otherwise associated with that user."""
    flagged = []
    ip_by_user = {}
    for log in logs:
        ip_by_user.setdefault(log["username"], set()).add(log["ip_address"])

    for log in logs:
        if log["event_type"] != "successful_login":
            continue
        if len(ip_by_user[log["username"]]) > 1:
            continue  # not a one-off, user has multiple known IPs — skip simple flag
    return flagged  # kept simple; real version can cross-reference a "known IPs" table


def detect_impossible_travel(logs):
    """Flag same user with successful logins from 2 different IPs within 10 minutes."""
    flagged = []
    by_user = {}
    for log in logs:
        if log["event_type"] == "successful_login":
            by_user.setdefault(log["username"], []).append(log)

    for user, entries in by_user.items():
        entries.sort(key=lambda x: x["timestamp"])
        for i in range(len(entries) - 1):
            gap = (entries[i + 1]["timestamp"] - entries[i]["timestamp"]).total_seconds()
            if entries[i]["ip_address"] != entries[i + 1]["ip_address"] and 0 < gap <= 600:
                flagged.append((entries[i + 1], f"Impossible travel: {user} logged in from {entries[i]['ip_address']} then {entries[i+1]['ip_address']} within {int(gap/60)} minutes", "high"))
    return flagged


def run_all_rules(logs):
    all_flags = []
    all_flags += detect_brute_force(logs)
    all_flags += detect_odd_hour_login(logs)
    all_flags += detect_impossible_travel(logs)
    return all_flags


# ---------- AI EXPLANATION ----------

def get_ai_explanation(log, reason):
    prompt = (
        "You are a SOC analyst assistant helping a cybersecurity student. "
        "In 2-3 simple sentences, explain why the following log entry is suspicious "
        "and what this type of activity typically indicates in a real environment.\n\n"
        f"Log: username={log['username']}, ip={log['ip_address']}, "
        f"time={log['timestamp']}, event={log['event_type']}\n"
        f"Flag reason: {reason}"
    )
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


# ---------- ROUTES ----------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_logs():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    stream = io.StringIO(file.stream.read().decode("utf-8"))
    reader = csv.DictReader(stream)
    logs = []
    for row in reader:
        logs.append({
            "username": row["username"],
            "ip_address": row["ip_address"],
            "timestamp": datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S"),
            "event_type": row["event_type"],
            "attempt_count": int(row.get("attempt_count", 1)),
        })

    conn = get_db_connection()
    cursor = conn.cursor()

    log_ids = {}
    for log in logs:
        cursor.execute(
            "INSERT INTO logs (username, ip_address, timestamp, event_type, attempt_count) VALUES (%s,%s,%s,%s,%s)",
            (log["username"], log["ip_address"], log["timestamp"], log["event_type"], log["attempt_count"])
        )
        log_ids[id(log)] = cursor.lastrowid

    flags = run_all_rules(logs)

    results = []
    for log, reason, severity in flags:
        explanation = get_ai_explanation(log, reason)
        cursor.execute(
            "INSERT INTO flagged_incidents (log_id, reason, ai_explanation, severity) VALUES (%s,%s,%s,%s)",
            (log_ids[id(log)], reason, explanation, severity)
        )
        results.append({
            "username": log["username"],
            "ip_address": log["ip_address"],
            "timestamp": log["timestamp"].isoformat(),
            "reason": reason,
            "explanation": explanation,
            "severity": severity,
        })

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "total_logs": len(logs),
        "total_flagged": len(results),
        "flagged": results,
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)