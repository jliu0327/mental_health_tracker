import sqlite3
from functools import wraps
from flask import session, redirect

# connect to same database
def db_connection():
    conn = sqlite3.connect('mental_health.db')
    # Enable dict-like access when querying database
    conn.row_factory = sqlite3.Row
    return conn


def login_required(f):
    # python decorator
    ## keeps the original function's name and info when wrapping it with new function
    @wraps(f)
    # *args is any number of unnamed inputs (like a list)
    # **kawrgs is any number of named inputs (like a dictionary)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        # if user is logged in, runs the original function(f) with any necessary inputs
        return f(*args, **kwargs)
    return decorated_function
