import os

from flask import Flask, flash, redirect, render_template, request, session
import sqlite3
from datetime import datetime
import re
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)
app.secret_key = 'wNZZI1OYWT'

# Gender list for registration
GENDERS = [
    "Male",
    "Female",
    "Nonbinary"
]


# connect to same db 
def db_connection():
    conn = sqlite3.connect('mental_health.db')
    return conn


@app.route("/")
def index():
    conn = db_connection()
    cur = conn.cursor()
    users = cur.execute('SELECT * FROM users').fetchall()
    conn.close
    return render_template("index.html", users=users)


# Log in users
@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


# Register user
@app.route("/register", methods=["GET", "POST"])
def register():
    # User reached route via POST (through submitting form)
    if request.method == "POST":
        first_name = request.form.get("first")
        last_name = request.form.get("last")
        gender = request.form.get("gender")
        date_of_birth = request.form.get("dob")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check if nothing is entered
        if not all([first_name, last_name, gender, date_of_birth, email, username, password]):
            flash('Please fill out all the fields')
            return redirect("/register")
        
        # Validate user input and email formatting
        if not re.search("^[a-zA-z0-9.+]+@[a-zA-Z0-9.-]+\.com$", email):
            flash('Inaccurate email format')
            return redirect("/register")

        # Check if password and confirmation match
        if password != confirmation:
            flash('Passwords do not match')
            return redirect("/register")

    return render_template("register.html", genders=GENDERS)



if __name__ == "__main__":
    app.run(debug=True)