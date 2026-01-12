from flask import Flask, request
import sqlite3
import bcrypt
import os
import ast
import subprocess

app = Flask(__name__)
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-12345")

DB_FILE = "users.db"
SAFE_DIR = "safe_files"  # créer ce dossier pour les fichiers à lire

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", "")
    password = request.json.get("password", "")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username=?"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    conn.close()

    if result and bcrypt.checkpw(password.encode(), result[1]):  # supposer password hashé
        return {"status": "success", "user": username}
    return {"status": "error", "message": "Invalid credentials"}

@app.route("/ping", methods=["POST"])
def ping():
    host = request.json.get("host", "")
    # sécurité : empêcher l'injection de commande
    output = subprocess.run(["ping", "-c", "1", host], capture_output=True, text=True)
    return {"output": output.stdout}

@app.route("/compute", methods=["POST"])
def compute():
    expr = request.json.get("expression", "1+1")
    try:
        result = ast.literal_eval(expr)
        return {"result": result}
    except:
        return {"error": "Invalid expression"}

@app.route("/hash", methods=["POST"])
def hash_password():
    pwd = request.json.get("password", "")
    hashed = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())
    return {"bcrypt": hashed.decode()}

@app.route("/readfile", methods=["POST"])
def readfile():
    filename = request.json.get("filename", "")
    safe_path = os.path.join(SAFE_DIR, os.path.basename(filename))
    try:
        with open(safe_path, "r") as f:
            content = f.read()
        return {"content": content}
    except Exception as e:
        return {"error": str(e)}

@app.route("/debug", methods=["GET"])
def debug():
    # Ne pas exposer secret key en prod
    return {"debug": True, "message": "Debug info hidden"}

@app.route("/hello", methods=["GET"])
def hello():
    return {"message": "Welcome to the DevSecOps API"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
