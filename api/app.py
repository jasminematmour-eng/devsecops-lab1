from flask import Flask, request, jsonify
import sqlite3
import hashlib
import os
import bcrypt

app = Flask(__name__)

# Utilisation d'une variable d'environnement au lieu d'une clé en clair
SECRET_KEY = os.environ.get("APP_SECRET_KEY", "default-safe-key")

def get_db_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Correction : Requête paramétrée contre l'injection SQL
    query = "SELECT password FROM users WHERE username=?"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode(), user['password']):
        return jsonify({"status": "success", "user": username})
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401

@app.route("/hash", methods=["POST"])
def hash_password():
    pwd = request.json.get("password", "")
    # Correction : Utilisation de bcrypt (plus sécurisé que MD5)
    hashed = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())
    return jsonify({"hash": hashed.decode()})

@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Welcome to the Secure DevSecOps API"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)