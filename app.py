from flask import Flask, request, redirect, url_for, session, render_template_string
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

DATABASE = "users.db"


def init_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
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
    direction: rtl;
}

.logo {
    width: 120px;
    height: 120px;
    margin: 30px auto 10px;
    border-radius: 50%;
    background: #1877f2;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: Arial, sans-serif;
    font-size: 90px;
    font-weight: bold;
}

.card {
    width: 90%;
    max-width: 490px;
    margin: 25px auto;
    padding: 30px;
    background: white;
    border-radius: 15px;
    box-shadow: 0 3px 15px #ccc;
}

h2 {
    text-align: center;
    font-size: 32px;
}

input {
    width: 100%;
    padding: 17px;
    margin: 8px 0;
    border: 1px solid #ddd;
    border-radius: 10px;
    font-size: 17px;
}

button {
    width: 100%;
    padding: 16px;
    margin-top: 10px;
    border: 0;
    border-radius: 9px;
    background: #1877f2;
    color: white;
    font-size: 19px;
}

a {
    color: #1877f2;
    text-decoration: none;
}

.message {
    text-align: center;
    color: #d00;
    margin: 10px;
}
</style>
"""


@app.route("/")
def home():
    return render_template_string(STYLE + """
        <div class="logo">f</div>

        <div class="card">
            <h2>تسجيل الدخول</h2>

            <form method="POST" action="/login">
                <input type="email"
                       name="email"
                       placeholder="البريد الإلكتروني"
                       required>

                <input type="password"
                       name="password"
                       placeholder="كلمة السر"
                       required>

                <button type="submit">
                    تسجيل الدخول
                </button>
            </form>

            <hr>

            <p style="text-align:center;">
                <a href="/register">إنشاء حساب جديد</a>
            </p>
        </div>
    """)


@app.route("/register", methods=["GET", "POST"])
def register():

    message = ""

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if len(password) < 6:
            message = "كلمة السر يجب أن تكون 6 أحرف على الأقل."

        else:
            password_hash = generate_password_hash(password)

            try:
                conn = sqlite3.connect(DATABASE)

                conn.execute("""
                    INSERT INTO users
                    (username, email, password_hash)
                    VALUES (?, ?, ?)
                """, (username, email, password_hash))

                conn.commit()
                conn.close()

                return redirect(url_for("home"))

            except sqlite3.IntegrityError:
                message = "البريد الإلكتروني مسجل من قبل."

    return render_template_string(STYLE + """
        <div class="logo">f</div>

        <div class="card">
            <h2>إنشاء حساب</h2>

            {% if message %}
                <div class="message">{{ message }}</div>
            {% endif %}

            <form method="POST">

                <input type="text"
                       name="username"
                       placeholder="اسم المستخدم"
                       required>

                <input type="email"
                       name="email"
                       placeholder="البريد الإلكتروني"
                       required>

                <input type="password"
                       name="password"
                       placeholder="كلمة السر"
                       required>

                <button type="submit">
                    إنشاء الحساب
                </button>

            </form>

            <p style="text-align:center;">
                <a href="/">العودة لتسجيل الدخول</a>
            </p>
        </div>
    """, message=message)


@app.route("/login", methods=["POST"])
def login():

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    conn = sqlite3.connect(DATABASE)
    user = conn.execute(
        "SELECT id, username, password_hash FROM users WHERE email = ?",
        (email,)
    ).fetchone()
    conn.close()

    if user and check_password_hash(user[2], password):
        session["user_id"] = user[0]
        session["username"] = user[1]

        return f"""
        <h1 style="text-align:center;">
            مرحباً {user[1]} 👋
        </h1>
        <p style="text-align:center;">
            تم تسجيل الدخول بنجاح.
        </p>
        """

    return render_template_string(STYLE + """
        <div class="logo">f</div>

        <div class="card">
            <h2>تسجيل الدخول</h2>

            <div class="message">
                البريد الإلكتروني أو كلمة السر غير صحيحة.
            </div>

            <a href="/">
                <button>العودة</button>
            </a>
        </div>
    """)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
)
