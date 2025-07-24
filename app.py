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


from cs50 import SQL

from flask import Flask, flash, redirect, render_template, request, session
# from flask_modals import Modal, render_template_modal
from flask_session import Session

from helpers import *
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
# modal = Modal(app)
app.secret_key = "very top secret key mr sirrrr"

# Session is 31 days by default (remind user to create an account)
app.config["SESSION_PERMANENT"] = True
# Store session data in server files
app.config["SESSION_TYPE"] = "filesystem"
# Initialize the session
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///users.db")


# All available topics
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


@app.route("/")
def index():
    """Root route, redirects to the home page."""
    return render_template("home.html", page="home")


@app.route("/home")
def home():
    """Home page, welcomes the user and explains the benefits of the website."""
    return render_template("home.html", page="home")


@app.route("/create", methods=["GET", "POST"])
def create():
    """Roadmap create page, where the user can enter input knowledge level."""
    # Requested via navigation
    if request.method == "GET":
        print("GET")
        return render_template("create.html", groups=groups, page="create")

    # Requested via the create button
    codeforces = request.form.get("codeforces")
    atcoder = request.form.get("atcoder")
    leetcode = request.form.get("leetcode")
    rating = 0

    # Validate input
    if codeforces or atcoder or leetcode:
        try:
            codeforces = int(codeforces)
            atcoder = int(atcoder)
            leetcode = int(leetcode)
        except ValueError:
            return render_template("error.html", message="Nope")

        rating = max(codeforces, atcoder, leetcode)

    # Cache user data into the session (topics, rating)
    topics = request.form.getlist("topics")

    session["rating"] = rating
    session["topics"] = topics

    return redirect("/progress")


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
    # Logout user, without deleting the session stored data (e.g. topics, rating)
    session.pop("user_id")
    return redirect("/")


# TODO: Make the login and register modals rather than pages
@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page, where the user can log in to their account."""
    # If accessed via navigation
    if request.method == "GET":
        return render_template("login.html")

    # Accessed via the login button
    email = request.form.get("email")
    password = request.form.get("password")

    print(email, password)

    # Validate input
    # TODO: When midifying the required attribute via devtools, it sends a GET request 404, leading
    # to a blank login page FIX IT
    if not email or not password:
        print("missing")
        return error("Missing required input.")

    # Ensure user is registered
    user_data = db.execute("SELECT * FROM users WHERE email = ?", email)

    print(user_data)

    if len(user_data) != 1:
        # TODO: if more than 1 email found, our problem
        print("user not found")
        return error("email is not registered.")

    # Ensure password is correct
    if not check_password_hash(user_data[0]["password"], password):
        print("incorrect password")
        return error("Incorrect password.")

    print("all good")

    # Remember which user has logged in
    session["user_id"] = user_data[0]["id"]

    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register page, where the user can create a new account."""
    # If accessed via navigation
    if request.method == "GET":
        return render_template("register.html")

    # Accessed via the register button
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    repassword = request.form.get("repassword")

    # Validate input
    # name is not required
    if not name:
        name = "user"

    # Required fields
    if not email or not password or not repassword:
        return error("Missing required input.")

    # Password confirmation validation
    if password != repassword:
        return error("Passwords do not match.")

    # check if email is available
    user_data = db.execute("SELECT * FROM users WHERE email = ?", email)

    if len(user_data) != 0:
        return error("this email is already registered, try to login instead.")

    # Insert user data into the database
    db.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
               name, email, generate_password_hash(password))

    # Log the user in
    session["user_id"] = db.execute(
        "SELECT id FROM users WHERE email = ?", email)[0]["id"]

    return redirect("/")
