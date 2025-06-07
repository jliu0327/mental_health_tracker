import os

from flask import Flask, flash, redirect, render_template, request, session
from datetime import date, datetime
from werkzeug.security import check_password_hash, generate_password_hash
from helper import db_connection, login_required, GENDERS, MOODS, CATEGORIES, PRIORITIES

# Configure application
app = Flask(__name__)
app.secret_key = 'wNZZI1OYWT'


@app.route("/")
@login_required
def index():
    conn = db_connection()
    cur = conn.cursor()
    users = cur.execute('SELECT * FROM users').fetchall()
    conn.close
    return render_template("index.html", users=users)


# Log in users
@app.route("/login", methods=["GET", "POST"])
def login():
    # Clear only user_id
    session.pop("user_id", None)

    # User reached route via POST
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # database checking
        if not all([username, password]):
            flash('One or more fields are missing')
            return redirect("/login")
        
        
        # Connect to database
        conn = db_connection()
        cur = conn.cursor()
        # Query database for username
        cur.execute(
            "SELECT * FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        if row is None:
            flash('Username does not exist')
            return redirect("/login")
        elif not check_password_hash(row["hash"], password):
            flash("Invalid password. Please try again.")
            return redirect("/login")
        
        # Remember user id
        session["user_id"] = row["id"]
        # Redirect user to homepage
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    # Forget user_id
    session.clear()
    # Redirect back to login page
    return redirect("/")


# Register user
@app.route("/register", methods=["GET", "POST"])
def register():
    # User reached route via POST (through submitting form)
    if request.method == "POST":
        first_name = request.form.get("first")
        last_name = request.form.get("last")
        gender = request.form.get("gender")
        date_of_birth = request.form.get("dob")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check if nothing is entered
        if not all([first_name, last_name, gender, date_of_birth, username, password]):
            flash('Please fill out all the fields')
            return redirect("/register")

        # Check if password and confirmation match
        if password != confirmation:
            flash('Passwords do not match')
            return redirect("/register")
        
        # Connect to database
        conn = db_connection()
        cur = conn.cursor()
        # Check if username is taken
        rows = cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = rows.fetchone()
        if existing_user:
            flash('Username already taken')
            return redirect("/register")
        
        # Hash the password
        hash_password = generate_password_hash(password)
        # Insert information into database
        cur.execute("INSERT INTO users (first_name, last_name, gender, dob, username, hash) VALUES (?, ?, ?, ?, ?, ?)",
                    (first_name, last_name, gender, date_of_birth, username, hash_password))
        
        # Commit changes and close connection
        conn.commit()
        conn.close()

        # Retrieve id of newly inserted user
        user_id = cur.lastrowid
        session["user_id"] = user_id
        # Redirect user to homepage
        return redirect("/")
    else:
        min_date = "1965-01-01"
        birthdate = date.today().replace(year=date.today().year - 10)
        return render_template("register.html", genders=GENDERS, birthdate=birthdate, min_date=min_date)


@app.route("/entry", methods=["GET", "POST"])
@login_required
def journal_log():
    # Connect to database
    conn = db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        # Retrieve information from journal page
        entry_date = request.form.get("date")
        content = request.form.get("content")
        if not entry_date or not content.strip():
            flash('One or more fields are missing')
            return redirect("/entry")

        # Insert data into table
        cur.execute("INSERT INTO entries (user_id, date, content) VALUES (?, ?, ?)",
                    (session["user_id"], entry_date, content))
        # Commit changes
        conn.commit()

    # Executes query and prepares the query, but does not return data
    cur.execute("SELECT date, content FROM entries WHERE user_id = ? ORDER BY date DESC", (session["user_id"],))
    # Retrieve all the rows from result set as a list of tuples
    entries = cur.fetchall()
    # Close connection
    conn.close()

    today = date.today()
    return render_template("journal.html", today=today, entries=entries)


@app.route("/tracker", methods=["GET", "POST"])
@login_required
def mood_tracker():
    # Connect to database
    conn = db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        # Retrieve information from tracker page
        today_date = request.form.get("date")
        mood_today = request.form.get("mood_feeling")
        sleep = request.form.get("mood_sleep")
        diet = request.form.get("mood_diet")
        energy = request.form.get("mood_energy")
        stress = request.form.get("mood_stress")

        # Data validation if user missed a field
        if not all([today_date, mood_today, sleep, diet, energy, stress]):
            flash("One or more fields is missing")
            return redirect("/tracker")

        # Insert data into table
        cur.execute("INSERT INTO tracker (user_id, date, mood, sleep, diet, energy, stress) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (session["user_id"], today_date, mood_today, sleep, diet, energy, stress))
        # Commit changes
        conn.commit()
        # Close connection
        conn.close()
    else:
        today = date.today()
        birthdate = date.today().replace(year=date.today().year - 10)
        return render_template("tracker.html", moods=MOODS, birthdate=birthdate, today=today)


@app.route("/goals", methods=["GET", "POST"])
@login_required
def goal_tracker():
    # Connect to database
    conn = db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        goals = request.form.get("set_goals")
        category = request.form.get("category")
        description = request.form.get("description")
        due_date = request.form.get("date")
        priority = request.form.get("priority")

        if not goals:
            flash("Please fill out the goal field if you want to submit")
            return redirect("/goals")
        elif not category:
            flash("Please fill out the category before submitting")
            return redirect("/goals")
        
        # Insert data into table
        cur.execute("INSERT INTO goals (user_id, goal_title, category, description, due_date, priority) VALUES (?, ?, ?, ?, ?, ?)",
                    session["user_id"], goals, category, description, due_date, priority)
        # Commit changes
        conn.commit()

        # Show user's goals
        cur.execute("SELECT * FROM goals WHERE user_id = ?", (session["user_id"],))
        cur.fetchall()
        # Close connection
        conn.close()

    today = date.today()

    return render_template("goal.html", today=today)


if __name__ == "__main__":
    app.run(debug=True)