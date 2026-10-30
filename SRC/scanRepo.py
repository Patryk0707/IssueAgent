import hmac, hashlib, json, os, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

import sendNotification
from Agent import agent

SECRET = os.environ["GITHUB_WEBHOOK_SECRET"].encode()
GH_TOKEN = os.environ.get("GITHUB_TOKEN")
ai = agent()


def review(repo, sha):
    headers = {"Accept": "application/vnd.github.diff"}
    if GH_TOKEN:
        headers["Authorization"] = f"Bearer {GH_TOKEN}"
    diff = requests.get(f"https://api.github.com/repos/{repo}/commits/{sha}",
                        headers=headers).text
    result = ai.nebiusAgent("Check changes for mistakes:\n" + diff[:20000])
    print(result)
    subject, _, body = result.strip().partition("\n")
    sendNotification.send_ntfy(subject.strip(), body.strip())


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        sig = self.headers.get("X-Hub-Signature-256", "")
        expected = "sha256=" + hmac.new(SECRET, body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected):
            self.send_response(403); self.end_headers(); return
        self.send_response(200); self.end_headers()  # answering fast
        if self.headers.get("X-GitHub-Event") == "push":
            data = json.loads(body)
            threading.Thread(target=review,
                             args=(data["repository"]["full_name"], data["after"]),
                             daemon=True).start()

    def log_message(self, *a):
        pass

#sdajfhq"-qAD
def listenForRepoUpdate(port=5000):
    print(f"Waiting for a webhook {port}. To stop: Ctrl+C")
    try:
        HTTPServer(("", port), Handler).serve_forever()
    except KeyboardInterrupt:
        print("Stopped")