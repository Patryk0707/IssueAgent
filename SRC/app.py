import os
from flask import Flask, request, render_template, jsonify
import checkRepo
import sendEmail
import sendNotification
from codeInput import checkCodeApp

app = Flask(__name__)
DB_FILE = "monitored_repos.txt"

# Helper functions to get/set registered repositories
def get_monitored_repos():
    if not os.path.exists(DB_FILE):
        return set()
    with open(DB_FILE, "r") as f:
        return set(line.strip().lower() for line in f if line.strip())

def add_repo_to_monitor(repo_url):
    repos = get_monitored_repos()
    clean_url = repo_url.strip().lower()
    if clean_url not in repos:
        with open(DB_FILE, "a") as f:
            f.write(clean_url + "\n")
        return True
    return False

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        action = request.form.get("action")

        if action == "code":
            code = request.form.get("code")
            if code:
                result = checkCodeApp(code)

        elif action == "repo":
            repo = request.form.get("repo")
            if repo:
                result = checkRepo.checkRepoByCode(repo)
                
        # --- NEW ACTION TRACKER FOR MONITORING ---
        elif action == "monitor":
            repo_to_monitor = request.form.get("repo_to_monitor")
            if repo_to_monitor:
                added = add_repo_to_monitor(repo_to_monitor)
                if added:
                    result = f"Successfully registered!\n\nNext Step: Go to GitHub Settings -> Webhooks for '{repo_to_monitor}' and set the Payload URL to your application's /webhook address."
                else:
                    result = "This repository is already registered in IssueAgent's monitoring list."

    return render_template("index.html", result=result, saved_email=sendEmail.loadSavedEmail())


# Send an analysis result by email and/or ntfy notification
@app.route("/send", methods=["POST"])
def send_result():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    email = (data.get("email") or "").strip()
    want_email = bool(data.get("send_email"))
    want_notification = bool(data.get("send_notification"))

    if not text:
        return jsonify({"ok": False, "message": "Nothing to send."}), 400
    if not want_email and not want_notification:
        return jsonify({"ok": False, "message": "Choose email and/or notification."}), 400

    # First line is the subject, everything after is the body (same as console version)
    subject, _, body = text.partition("\n")
    subject = subject.strip()
    body = body.strip()

    messages = []
    ok = True

    if want_notification:
        if sendNotification.send_ntfy(subject, body):
            messages.append("Notification sent.")
        else:
            ok = False
            messages.append("Notification failed (check NTFY_TOPIC).")

    if want_email:
        if not sendEmail.isValidEmail(email):
            ok = False
            messages.append("Invalid email address.")
        elif sendEmail.send_status_email(email, subject, body):
            sendEmail.saveEmail(email)
            messages.append("Email sent.")
        else:
            ok = False
            messages.append("Email failed (check SENDER_EMAIL/APP_PASSWORD).")

    return jsonify({"ok": ok, "message": " ".join(messages)})


# --- UPGRADED WEBHOOK ROUTE WITH AUTOMATED ANALYSIS ---
@app.route("/webhook", methods=["POST"])
def github_webhook():
    data = request.json
    
    if data and 'repository' in data:
        repo_url = data['repository'].get('html_url', '').lower()
        repo_name = data['repository'].get('name')
        
        monitored_list = get_monitored_repos()
        
        # Match incoming webhooks against user-registered list
        if repo_url in monitored_list:
            print(f"🎯 Monitored Change Detected: {repo_name}", flush=True)
            
            # Instantly pass incoming repo into your Nebius Agent framework
            analysis_result = checkRepo.checkRepoByCode(data['repository'].get('html_url'))
            
            print(f"📝 Analysis for {repo_name}:\n{analysis_result}", flush=True)
            
            return jsonify({"status": "success", "message": "Automated code review complete"}), 200
        else:
            print(f"🛑 Ignored webhook request from unmonitored repo: {repo_url}", flush=True)
            return jsonify({"status": "ignored", "message": "Repository not on monitoring list"}), 200
        
    return jsonify({"status": "error", "message": "Invalid payload format"}), 400
