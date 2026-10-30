from flask import Flask, request, render_template
import checkRepo
from codeInput import checkCodeApp

app = Flask(__name__)

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

    # Flask will automatically take'index.html' from directory 'templates'
    return render_template("index.html", result=result)
