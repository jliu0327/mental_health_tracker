import os

from flask import Flask, redirect, render_template, request, session
import sqlite3
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

@app.route("/")
def index():
    conn = db_connection()
    cur = conn.cursor()
    users = cur.execute('SELECT * FROM users').fetchall()
    conn.close
    return render_template("layout.html", users=users)

# connect to same db 
def db_connection():
    conn = sqlite3.connect('mental_health.db')
    return conn


if __name__ == "__main__":
    app.run(debug=True)