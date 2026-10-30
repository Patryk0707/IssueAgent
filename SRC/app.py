import os
from flask import Flask, request, render_template, jsonify
import checkRepo
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

    return render_template("index.html", result=result)


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
