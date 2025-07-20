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


from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from helpers import *


app = Flask(__name__)


# Topics
groups = {
    "C++ Fundamentals": [
        "Data Types",
        "Loops",
        "Arrays",
        "Strings",
        "Functions",
    ],
    "Python Fundamentals": [
        "Data Types",
        "Loops",
        "Lists",
        "Dictionaries",
        "Functions",
    ],
    "Data Structures": [
        "Linked Lists",
        "Stacks",
        "Queues",
        "Trees",
        "Graphs",
    ],
    "Algorithms": [
        "Sorting",
        "Searching",
        "Dynamic Programming",
        "Greedy",
        "Backtracking",
    ],
    "Techniques": [
        "Problem Solving Techniques",
        "Time Complexity Analysis",
        "Space Complexity Analysis",
        "Contest Strategies",
        "Debugging Techniques",
    ],
    "Advanced Topics": [
        "Bit Manipulation",
        "Number Theory",
        "Combinatorics",
        "Game Theory",
        "Graph Theory",
    ],
    "Miscellaneous": [
        "Mathematical Foundations",
        "Coding Standards",
        "Code Optimization",
        "Memory Management",
        "Input/Output Techniques",
    ],
}


# Session is 31 days by default (remind user to create an account)
app.config["SESSION_PERMANENT"] = True
# Store session data in server files
app.config["SESSION_TYPE"] = "filesystem"


@app.route("/")
def index():
    """Root route, redirects to the home page."""
    return render_template("home.html", page="home")


@app.route("/home")
def home():
    """Home page, welcomes the user and explains the benefits of the website."""
    return render_template("home.html", page="home")


@app.route("/create")
def create():
    """Roadmap create page, where the user can enter input knowledge level."""
    return render_template("create.html", groups=groups, page="create")


@app.route("/progress")
def progress():
    """Progress page, where the user can track their progress."""
    return render_template("progress.html")


@app.route("/resources")
def resources():
    """Resources page, where the user can find the resources library."""
    return render_template("resources.html")


@app.route("/history")
def history():
    """History page, where the user can see their past roadmaps and their progress."""
    return render_template("history.html")


@app.route("/search")
def search():
    """Search page, where the user can search for resources."""
    return render_template("search.html")


@app.route("/profile")
def profile():
    """Profile page, where the user can view and edit their profile."""
    return render_template("profile.html")


@app.route("/logout")
def logout():
    """Logout page, where the user can log out of their account."""
    return render_template("logout.html")


@app.route("/login")
def login():
    """Login page, where the user can log in to their account."""
    return render_template("login.html")


@app.route("/register")
def register():
    """Register page, where the user can create a new account."""
    return render_template("register.html")
