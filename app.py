"""
A web application to aid competitive programmers with their learning journey.

Input (atleast one):
- Topics covered by the user.
- Top rating in a competitive programming platform.

Algorithm:
- Retrieves relevant resources from the database.

Output:
- A roadmap for the user to follow, with downloadable resouces.
"""

# Since I'm a lazy coder, here is the command to launch the website:
# flask run --debug

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    """Home page, welcomes the user and explains the benefits of the website."""
    return render_template("layout.html")


@app.route("/input", methods=["GET", "POST"])
def input():
    """Input page, where the user can enter their topics and ratings."""
    ...


@app.route("/output")
def output():
    """Output page, where the user can see their personalized roadmap."""
    return "Hello World"
    ...


def history():
    """History page, where the user can see their past roadmaps."""
    ...
