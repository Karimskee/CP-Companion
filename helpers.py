"""
Self made helpers functions for the CP Companion website application.
"""
from flask import flash, redirect, render_template, session


def logged_in():
    """Check if the user is logged in, so he can access certain pages if not."""
    if not session.get("user_id"):
        return redirect("/login")

    return True


def error(message):
    """Error feedback."""
    return render_template("error.html", message=message)


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("error.html", message=message), code
