from flask import Flask, request, redirect, url_for, session, render_template_string
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

DATABASE = "users.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_db()


STYLE = """
<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: #f0f2f5;
    font-family: Arial, sans-serif;
}

.container {
    width: 100%;
    max-width: 400px;
    margin: 70px auto;
    padding: 20px;
}

.logo {
    text-align: center;
    margin-bottom: 25px;
}

.f-logo {
    width: 90px;
    height: 90px;
    margin: auto;
    border-radius: 50%;
    background: #1877f2;
    color: white;
    font-size: 75px;
    font-weight: bold;
    line-height: 105px;
}

.title {
    color: #1877f2;
    font-size: 30px;
    font-weight: bold;
    margin-top: 12px;
}

.box {
    background: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.15);
}

input {
    width: 100%;
    padding: 16px;
    margin-bottom: 12px;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 16px;
}

button {
    width: 100%;
    padding: 15px;
    border: none;
    border-radius: 8px;
    background: #1877f2;
    color: white;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
}

button:hover {
    background: #166fe5;
}

a {
    color: #1877f2;
    text-decoration: none;
}

.center {
    text-align: center;
    margin-top: 20px;
}

.error {
    background: #ffe5e5;
    color: #b00000;
    padding: 10px;
    border-radius: 7px;
    margin-bottom: 15px;
}

.success {
    background: #e5ffe
