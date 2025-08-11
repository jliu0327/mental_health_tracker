import os

from flask import Flask, flash, redirect, render_template, request, session
from datetime import date, datetime
from werkzeug.security import check_password_hash, generate_password_hash
from helper import db_connection, login_required, GENDERS, MOODS, CATEGORIES, PRIORITIES, MOOD_MAPS

# Configure application
app = Flask(__name__, static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY')

@app.route("/")
@login_required
def index():
    conn = db_connection()
    cur = conn.cursor()

    # get user id
    user_id = session["user_id"]

    # get latest 5 journal entries
    cur.execute("SELECT date, mood, stress, emotion, self_reflection, content FROM entries WHERE user_id = ? ORDER BY date DESC LIMIT 4", (user_id,))
    journal_entries = cur.fetchall()

    # get latest 5 mood tracker entries
    cur.execute("SELECT date, mood_val, sleep_val, diet_val, energy_val, stress_val FROM tracker WHERE user_id = ? ORDER BY date DESC LIMIT 10", 
    (user_id,))
    mood_rows = cur.fetchall()[::-1]

    dates = []
    mood_val = []
    sleep_val = []
    diet_val = []
    energy_val = []
    stress_val = []
    for row in mood_rows:
        dates.append(row[0])
        mood_val.append(row[1])
        sleep_val.append(row[2])
        diet_val.append(row[3])
        energy_val.append(row[4])
        stress_val.append(row[5])

    # get latest 5 goal entries
    cur.execute("SELECT goal_title, category, description, due_date, priority FROM goals WHERE user_id = ? AND completed = 0 ORDER BY due_date LIMIT 5", (user_id,))
    goal_entries = cur.fetchall()

    conn.close()
    
    return render_template("index.html",
                           journal_entries = journal_entries,
                           goal_entries = goal_entries,
                           dates=dates,
                           mood_val=mood_val,
                           sleep_val=sleep_val,
                           diet_val=diet_val,
                           energy_val=energy_val,
                           stress_val=stress_val)


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
        first_name = request.form.get("first-name")
        last_name = request.form.get("last-name")
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
        mood_response = request.form.get("mood-response")
        stress_response = request.form.get("stress-response")
        emotion_response = request.form.get("emotion-response")
        reflection_response = request.form.get("reflection-response")
        additional_thoughts = request.form.get("additional-thoughts")

        if not all([entry_date, mood_response, stress_response, emotion_response, reflection_response]):
            flash('One or more fields are missing')
            return redirect("/entry")

        # Insert data into table
        cur.execute("INSERT INTO entries (user_id, date, mood, stress, emotion, self_reflection, additional_thoughts) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (session["user_id"], entry_date, mood_response, stress_response, emotion_response, reflection_response, additional_thoughts))
        # Commit changes
        conn.commit()
        conn.close()
        return redirect("/entry")

    # Executes query and prepares the query, but does not return data
    cur.execute("SELECT date, mood, stress, emotion, self_reflection, content FROM entries WHERE user_id = ? ORDER BY date DESC", (session["user_id"],))
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

        # Convert mood value to numeric value
        mood_today_val = MOOD_MAPS.get(mood_today, 0)
        sleep_val = MOOD_MAPS.get(sleep, 0)
        diet_val = MOOD_MAPS.get(diet, 0)
        energy_val = MOOD_MAPS.get(energy, 0)
        stress_val = MOOD_MAPS.get(stress, 0)

        # Insert data into table
        cur.execute("""INSERT INTO tracker (user_id, date, mood, mood_val, sleep, sleep_val, 
                    diet, diet_val, energy, energy_val, stress, stress_val) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (session["user_id"], today_date, mood_today, mood_today_val, sleep, sleep_val, 
                     diet, diet_val, energy, energy_val, stress, stress_val))
        # Commit changes
        conn.commit()
        # Close connection
        conn.close()
        return redirect("/tracker")
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
        due_date = request.form.get("target_date")
        priority = request.form.get("priority")

        if not goals:
            flash("Please fill out the goal field if you want to submit")
            return redirect("/goals")
        elif not category:
            flash("Please fill out the category before submitting")
            return redirect("/goals")
        
        # Insert data into table
        cur.execute("INSERT INTO goals (user_id, goal_title, category, description, due_date, priority) VALUES (?, ?, ?, ?, ?, ?)",
                    (session["user_id"], goals, category, description, due_date, priority))
        # Commit changes
        conn.commit()
        conn.close()
        return redirect("/goals")

    # Show user's goals
    cur.execute("SELECT * FROM goals WHERE user_id = ? AND completed = 0", (session["user_id"],))
    goals_data = cur.fetchall()
    # Show user's completed goals
    cur.execute("SELECT goal_title, category, description FROM goals WHERE user_id = ? AND completed = 1", (session["user_id"],))
    completed_goals = cur.fetchall()
    # Close connection
    conn.close()

    today = date.today()
    return render_template("goal.html", goals=goals_data, completed_goals=completed_goals, today=today, categories=CATEGORIES, priorities=PRIORITIES)


@app.route("/complete_goal", methods=["POST"])
@login_required
def complete_goal():
    conn = db_connection()
    cur = conn.cursor()

    goal_id = request.form.get("goal_id")
    # Always set to complete when checked
    if request.form.get("completed"):
        is_complete = 1
    else:
        is_complete = 0

    cur.execute("UPDATE goals SET completed = ? WHERE id = ? AND user_id = ?", (is_complete, goal_id, session["user_id"]))
    conn.commit()
    conn.close()

    return redirect("/goals")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        action = request.form.get("action")
        # cancel changes if "Cancel" button is selected
        if action == "cancel":
            return redirect("profile")
        
        # proceed with save logic
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("SELECT hash FROM users WHERE id = ?", (session["user_id"],))
        row = cur.fetchone()
        stored_hash = row[0]

        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        username = request.form.get("username")
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")
        
        if not check_password_hash(stored_hash, current_password):
            flash("Current password is incorrect. Please try again.")
            return redirect("/profile")
        
        if new_password != confirm_password:
            flash("New passwords do not match.")
            return render_template("profile.html",
                                   first_name = first_name,
                                   last_name = last_name,
                                   username = username)
        else:
            hash_password = generate_password_hash(new_password)
        
        ## update table if they click "save"
        cur.execute("UPDATE users SET first_name = ?, last_name = ?, username = ?, hash = ? WHERE id = ?",
                    (first_name, last_name, username, hash_password, session["user_id"]))
        conn.commit()
        conn.close()
        return redirect("profile")
    else:
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("SELECT first_name, last_name, username FROM users WHERE id = ?", (session["user_id"],))
        user = cur.fetchone()
        conn.close()

        return render_template("profile.html",
                               first_name = user[0],
                               last_name = user[1],
                               username = user[2])


if __name__ == "__main__":
    app.run(debug=True)