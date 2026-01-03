from flask import Flask, request
import sqlite3
import subprocess
import hashlib
import os

app = Flask(__name__)

# Clé secrète codée en dur (mauvaise pratique volontaire)
SECRET_KEY = "dev-secret-key-12345"


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = (
        f"SELECT * FROM users "
        f"WHERE username='{username}' AND password='{password}'"
    )
    cursor.execute(query)

    result = cursor.fetchone()
    conn.close()

    if result:
        return {"status": "success", "user": username}

    return {"status": "error", "message": "Invalid credentials"}


@app.route("/ping", methods=["POST"])
def ping():
    host = request.json.get("host", "")
    cmd = f"ping -c 1 {host}"
    #output = subprocess.check_output(cmd, shell=True)
    output = subprocess.check_output(
        ["ping","-C","1",host],
        stderr=subprocess.STDOUT,
        text=True
    )

    return {"output": output.decode()}


@app.route("/compute", methods=["POST"])
def compute():
    expression = request.json.get("expression", "1+1")
    result = eval(expression)  # CRITIQUE
