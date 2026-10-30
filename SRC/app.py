from flask import Flask, request, render_template_string
import checkRepo
from codeInput import checkCodeApp

app = Flask(__name__)

PAGE = """
<h1>IssueAgent</h1>

<h2>Check Code</h2>

<form method="POST">
    <input type="hidden" name="action" value="code">

    <textarea
        name="code"
        rows="15"
        cols="80"
        placeholder="Paste code here..."
        required
    ></textarea>

    <br>
    <button type="submit">Analyse Code</button>
</form>

<hr>

<h2>Check Repository</h2>

<form method="POST">
    <input type="hidden" name="action" value="repo">

    <input
        type="text"
        name="repo"
        placeholder="GitHub repository URL"
        style="width: 450px;"
        required
    >

    <button type="submit">Analyse Repository</button>
</form>

{% if result %}
    <hr>
    <h2>Result</h2>
    <pre>{{ result }}</pre>
{% endif %}
"""


@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        action = request.form["action"]

        if action == "code":
            code = request.form["code"]
            result = checkCodeApp(code)

        elif action == "repo":
            repo = request.form["repo"]
            result = checkRepo.checkRepoByCode(repo)

    return render_template_string(PAGE, result=result)


if __name__ == "__main__":
    app.run(debug=True)