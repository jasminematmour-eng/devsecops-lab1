from flask import Flask, request, jsonify
import sqlite3
import os
import bcrypt

app = Flask(__name__)

# Initialisation d'une base de données sécurisée
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    conn.commit()
    conn.close()

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Correction : Requête paramétrée (évite l'injection SQL)
    query = "SELECT password FROM users WHERE username=?"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode(), user['password'].encode()):
        return jsonify({"status": "success", "user": username})
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401

@app.route("/hash", methods=["POST"])
def hash_password():
    pwd = request.json.get("password", "")
    # Correction : Utilisation de bcrypt au lieu de MD5
    hashed = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())
    return jsonify({"hash": hashed.decode()})

@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({"message": "API Securisee et Pipeline Vert !"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)