from flask import Flask, request, redirect, session
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

DB_NAME = "users.db"


# =========================
# قاعدة البيانات
# =========================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


init_db()


# =========================
# التصميم
# =========================
STYLE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>My Account</title>

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f8fafd;
    color: #202124;
}

.container {
    width: 100%;
    max-width: 450px;
    margin: 70px auto;
    padding: 40px;
    background: white;
    border: 1px solid #dadce0;
    border-radius: 12px;
}

.logo {
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    margin-bottom: 25px;
    color: #4285f4;
}

h1 {
    text-align: center;
    font-size: 25px;
    font-weight: 400;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    color: #5f6368;
    margin-bottom: 30px;
}

input {
    width: 100%;
    padding: 15px;
    margin-bottom: 18px;
    border: 1px solid #dadce0;
    border-radius: 5px;
    font-size: 16px;
    outline: none;
}

input:focus {
    border: 2px solid #4285f4;
}

button {
    width: 100%;
    padding: 13px;
    border: none;
    border-radius: 5px;
    background: #1a73e8;
    color: white;
    font-size: 16px;
    cursor: pointer;
}

button:hover {
    background: #1557b0;
}

.link {
    display: block;
    text-align: center;
    margin-top: 22px;
    color: #1a73e8;
    text-decoration: none;
}

.message {
    background: #fce8e6;
    color: #c5221f;
    padding: 12px;
    border-radius: 5px;
    margin-bottom: 20px;
    text-align: center;
}

.success {
    background: #e6f4ea;
    color: #137333;
}

.footer {
    text-align: center;
    color: #5f6368;
    font-size: 13px;
    margin-top: 25px;
}

@media(max-width:500px) {
    .container {
        margin: 20px;
        padding: 25px;
        border: none;
    }
}
</style>
</head>

<body>
"""


# =========================
# الصفحة الرئيسية
# =========================
@app.route("/")
def home():

    if "user" in session:
        return STYLE + f"""
        <div class="container">

            <div class="logo">My Account</div>

            <h1>مرحباً بك</h1>

            <p class="subtitle">
                {session["user"]}
            </p>

            <a href="/logout" class="link">
                تسجيل الخروج
            </a>

        </div>
        </body>
        </html>
        """

    return STYLE + """
    <div class="container">

        <div class="logo">My Account</div>

        <h1>تسجيل الدخول</h1>

        <p class="subtitle">
            استخدم حسابك للمتابعة
        </p>

        <form action="/login" method="POST">

            <input
                type="email"
                name="email"
                placeholder="البريد الإلكتروني"
                required
            >

            <input
                type="password"
                name="password"
                placeholder="كلمة المرور"
                required
            >

            <button type="submit">
                تسجيل الدخول
            </button>

        </form>

        <a href="/register" class="link">
            إنشاء حساب جديد
        </a>

        <div class="footer">
            حسابك محمي بكلمة مرور مشفرة
        </div>

    </div>
    </body>
    </html>
    """


# =========================
# إنشاء حساب
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            return STYLE + """
            <div class="container">
                <div class="message">
                    أدخل البريد الإلكتروني وكلمة المرور
                </div>
                <a href="/register" class="link">
                    العودة
                </a>
            </div>
            </body>
            </html>
            """

        password_hash = generate_password_hash(password)

        try:
            conn = sqlite3.connect(DB_NAME)

            conn.execute(
                "INSERT INTO users (email, password) VALUES (?, ?)",
                (email, password_hash)
            )

            conn.commit()
            conn.close()

            return redirect("/")

        except sqlite3.IntegrityError:

            return STYLE + """
            <div class="container">

                <div class="message">
                    هذا البريد مسجل مسبقاً
                </div>

                <a href="/register" class="link">
                    العودة لإنشاء الحساب
                </a>

            </div>
            </body>
            </html>
            """

    return STYLE + """
    <div class="container">

        <div class="logo">My Account</div>

        <h1>إنشاء حساب</h1>

        <p class="subtitle">
            أنشئ حسابك الجديد
        </p>

        <form action="/register" method="POST">

            <input
                type="email"
                name="email"
                placeholder="البريد الإلكتروني"
                required
            >

            <input
                type="password"
                name="password"
                placeholder="كلمة المرور"
                minlength="6"
                required
            >

            <button type="submit">
                إنشاء الحساب
            </button>

        </form>

        <a href="/" class="link">
            لديك حساب؟ تسجيل الدخول
        </a>

    </div>
    </body>
    </html>
    """


# =========================
# تسجيل الدخول
# =========================
@app.route("/login", methods=["POST"])
def login():

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT email, password FROM users WHERE email = ?",
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    if user and check_password_hash(user[1], password):

        session["user"] = user[0]

        return redirect("/")

    return STYLE + """
    <div class="container">

        <div class="message">
            البريد الإلكتروني أو كلمة المرور غير صحيحة
        </div>

        <a href="/" class="link">
            المحاولة مرة أخرى
        </a>

    </div>
    </body>
    </html>
    """


# =========================
# تسجيل الخروج
# =========================
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# =========================
# تشغيل التطبيق - Render
# =========================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
