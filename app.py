from flask import Flask, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

DB = "users.db"


def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


init_db()


@app.route("/")
def home():
    username = session.get("username")

    if username:
        return f"""
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>موقعي الإلكتروني</title>
            <style>
                body {{
                    font-family: Arial;
                    background: #f2f2f2;
                    text-align: center;
                    padding: 60px 20px;
                }}
                .box {{
                    max-width: 500px;
                    margin: auto;
                    background: white;
                    padding: 30px;
                    border-radius: 15px;
                    box-shadow: 0 4px 15px #bbb;
                }}
                h1 {{ color: #1877f2; }}
                a {{
                    display: inline-block;
                    margin: 10px;
                    padding: 12px 25px;
                    background: #1877f2;
                    color: white;
                    text-decoration: none;
                    border-radius: 8px;
                }}
                .logout {{ background: #e74c3c; }}
            </style>
        </head>
        <body>
            <div class="box">
                <h1>مرحباً {username} 👋</h1>
                <p>أهلاً بك في موقعك الإلكتروني</p>
                <a href="/about">عن الموقع</a>
                <a class="logout" href="/logout">تسجيل الخروج</a>
            </div>
        </body>
        </html>
        """

    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>موقعي الإلكتروني</title>
        <style>
            body {
                font-family: Arial;
                background: #f2f2f2;
                text-align: center;
                padding: 60px 20px;
            }
            .box {
                max-width: 500px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 4px 15px #bbb;
            }
            h1 { color: #1877f2; }
            a {
                display: inline-block;
                margin: 10px;
                padding: 12px 25px;
                background: #1877f2;
                color: white;
                text-decoration: none;
                border-radius: 8px;
            }
        </style>
    </head>
    <body>
        <div class="box">
            <h1>مرحباً بك
