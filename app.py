import os

from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

# Configure application
app = Flask(__name__)

@app.route("/")
def index():
    conn = db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close
    return render_template("index.html", users=users)

# connect to same db 
def db_connection():
    conn = sqlite3.connect('mental_health.db')
    return conn

