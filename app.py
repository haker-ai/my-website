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
    background: #e5ffe9;
    color: #08752b;
    padding: 10px;
    border-radius: 7px;
    margin-bottom: 15px;
}
</style>
"""


@app.route("/")
def home():

    if "user_id" in session:
        return redirect(url_for("profile"))

    return render_template_string(
        STYLE + """
        <div class="container">

            <div class="logo">
                <div class="f-logo">f</div>
                <div class="title">موقعي</div>
            </div>

            <div class="box">

                <h2>تسجيل الدخول</h2>

                <form method="POST" action="/login">

                    <input
                        type="email"
                        name="email"
                        placeholder="البريد الإلكتروني"
                        required
                    >

                    <input
                        type="password"
                        name="password"
                        placeholder="كلمة السر"
                        required
                    >

                    <button type="submit">
                        تسجيل الدخول
                    </button>

                </form>

                <div class="center">
                    <a href="/register">إنشاء حساب جديد</a>
                </div>

            </div>

        </div>
        """
    )


@app.route("/register", methods=["GET", "POST"])
def register():

    error = ""

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if len(username) < 3:
            error = "اسم المستخدم يجب أن يكون 3 أحرف على الأقل."

        elif len(password) < 8:
            error = "كلمة السر يجب أن تكون 8 أحرف على الأقل."

        else:

            password_hash = generate_password_hash(password)

            try:

                conn = get_db()

                conn.execute(
                    """
                    INSERT INTO users
                    (username, email, password_hash)
                    VALUES (?, ?, ?)
                    """,
                    (username, email, password_hash)
                )

                conn.commit()
                conn.close()

                return redirect(url_for("home"))

            except sqlite3.IntegrityError:

                error = "البريد الإلكتروني أو اسم المستخدم مستخدم بالفعل."

    return render_template_string(
        STYLE + """
        <div class="container">

            <div class="logo">
                <div class="f-logo">f</div>
                <div class="title">موقعي</div>
            </div>

            <div class="box">

                <h2>إنشاء حساب جديد</h2>

                {% if error %}
                    <div class="error">{{ error }}</div>
                {% endif %}

                <form method="POST">

                    <input
                        type="text"
                        name="username"
                        placeholder="اسم المستخدم"
                        required
                    >

                    <input
                        type="email"
                        name="email"
                        placeholder="البريد الإلكتروني"
                        required
                    >

                    <input
                        type="password"
                        name="password"
                        placeholder="كلمة السر"
                        required
                    >

                    <button type="submit">
                        إنشاء الحساب
                    </button>

                </form>

                <div class="center">
                    <a href="/">العودة لتسجيل الدخول</a>
                </div>

            </div>

        </div>
        """,
        error=error
    )


@app.route("/login", methods=["POST"])
def login():

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    conn = get_db()

    user = conn.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    conn.close()

    if user and check_password_hash(
        user["password_hash"],
        password
    ):

        session["user_id"] = user["id"]
        session["username"] = user["username"]

        return redirect(url_for("profile"))

    return render_template_string(
        STYLE + """
        <div class="container">
            <div class="box">

                <div class="error">
                    البريد الإلكتروني أو كلمة السر غير صحيحة.
                </div>

                <div class="center">
                    <a href="/">العودة</a>
                </div>

            </div>
        </div>
        """
    )


@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect(url_for("home"))

    return render_template_string(
        STYLE + """
        <div class="container">

            <div class="logo">
                <div class="f-logo">f</div>
            </div>

            <div class="box">

                <h2>مرحباً {{ username }} 👋</h2>

                <p>تم تسجيل دخولك بنجاح.</p>

                <div class="center">
                    <a href="/logout">تسجيل الخروج</a>
                </div>

            </div>

        </div>
        """,
        username=session["username"]
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
                )
