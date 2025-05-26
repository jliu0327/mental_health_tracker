from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

# Configure application
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")