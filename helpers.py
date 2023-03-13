from flask import redirect, render_template, request, session
from functools import wraps
import random

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.
        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    
    number = random.randint(0, 3)

    return render_template("apology.html", top=code, bottom=escape(message), number=number), code



def login_required(f):
    """
    Decorate routes to require login.
    If user not logged in, redirect to index page.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function
