import os
import psycopg2
from flask import Flask, request, render_template, redirect, url_for, session, abort
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load local environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

def get_db_connection():
    """Connect to PostgreSQL using env variables"""
    return psycopg2.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME")
    )

def check_rate_limit(ip):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        one_minute_ago = datetime.now() - timedelta(minutes=1)
        cur.execute("SELECT COUNT(*) FROM security_logs WHERE ip_address = %s AND timestamp > %s", (ip, one_minute_ago))
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return count
    except: return 0

def log_event(ip, event_type, severity, desc):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        browser = request.headers.get('User-Agent')
        ref = request.headers.get('Referer')
        cur.execute(
            "INSERT INTO security_logs (ip_address, event_type, severity, description, browser_info, referrer) VALUES (%s, %s, %s, %s, %s, %s)",
            (ip, event_type, severity, desc, browser, ref)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e: print(f"DB Log Error: {e}")

def is_banned(ip):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM security_logs WHERE ip_address = %s AND severity = 10", (ip,))
        banned = cur.fetchone()[0] > 0
        cur.close()
        conn.close()
        return banned
    except: return False

@app.route('/')
def public_home():
    ip = request.remote_addr
    if is_banned(ip):
        abort(403)
    log_event(ip, "VISIT", 1, "Redirect to AI Interface")
    # Redirect to the Streamlit Public Interface
    return redirect("http://89.168.117.245:8502")

@app.route('/wp-admin')
@app.route('/.env')
def honeypot():
    ip = request.remote_addr
    log_event(ip, "HACK_ATTEMPT", 10, f"Honeypot hit: {request.path}")
    return abort(403)

if __name__ == '__main__':
    # Running on port 8500 as established on the server
    app.run(host='0.0.0.0', port=8500, debug=False)
