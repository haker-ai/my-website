from flask import Flask, request, redirect, url_for, session, render_template_string
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# مفتاح الجلسات
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

DATABASE = "users.db"


# =========================
# قاعدة البيانات
# =========================
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
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


# =========================
# التصميم العام
# =========================
STYLE = """
<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f0f2f5;
    direction: rtl;
}

.navbar {
    background: #1877f2;
    color: white;
    padding: 15px 25px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 28px;
    font-weight: bold;
}

.container {
    max-width: 430px;
    margin: 50px auto;
    padding: 20px;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.12);
}

h1, h2 {
    text-align: center;
}

input {
    width: 100%;
    padding: 14px;
    margin: 8px 0;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 16px;
}

button {
    width: 100%;
    padding: 14px;
    margin-top: 10px;
    border: none;
    border-radius: 8px;
    background: #1877f2;
    color: white;
    font-size: 17px;
    cursor: pointer;
}

button:hover {
    background: #166fe5;
}

a {
    color: #1877f2;
    text-decoration: none;
}

.message {
    text-align: center;
    color: red;
    margin: 10px;
}

.profile {
    text-align: center;
}

.avatar {
    width: 90px;
    height: 90px;
    background: #1877f2;
    color: white;
    border-radius: 50%;
    margin: auto;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 40px;
    font-weight: bold;
}
</style>
"""


# =========================
# الصفحة الرئيسية
# =========================
@app.route("/")
def home():

    if "user_id" in session:
        return redirect(url_for("profile"))

    return render_template_string(STYLE + """
    <div class="navbar">
        <div class="logo">SBook</div>
        <div>
            <a href="/login" style="color:white;">تسجيل الدخول</a>
        </div>
    </div>

    <div class="container">
        <div class="card">
            <h1>مرحباً بك في SBook 👋</h1>

            <p style="text-align:center;">
                شبكة اجتماعية خاصة بك
            </p>

            <a href="/register">
                <button>إنشاء حساب جديد</button>
            </a>

            <a href="/login">
                <button style="background:#42b72a;">
                    تسجيل الدخول
                </button>
            </a>
        </div>
    </div>
    """)


# =========================
# التسجيل
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():

    message = ""

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not username or not email or not password:
            message = "يرجى ملء جميع الحقول."

        elif len(password) < 6:
            message = "كلمة المرور يجب أن تكون 6 أحرف على الأقل."

        else:
            password_hash = generate_password_hash(password)

            try:
                conn = sqlite3.connect(DATABASE)
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO users
                    (username, email, password_hash)
                    VALUES (?, ?, ?)
                """, (username, email, password_hash))

                conn.commit()
                conn.close()

                return redirect(url_for("login"))

            except sqlite3.IntegrityError:
                message = "هذا البريد الإلكتروني مسجل بالفعل."

    return render_template_string(STYLE + """
    <div class="navbar">
        <div class="logo">SBook</div>
    </div>

    <div class="container">
        <div class="card">

            <h2>إنشاء حساب جديد</h2>

            {% if message %}
                <div class="message">{{ message }}</div>
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
                    placeholder="كلمة المرور"
                    required
                >

                <button type="submit">
                    إنشاء الحساب
                </button>

            </form>

            <p style="text-align:center;">
                لديك حساب؟
                <a href="/login">تسجيل الدخول</a>
            </p>

        </div>
    </div>
    """, message=message)


# =========================
# تسجيل الدخول
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():

    message = ""

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, username, password_hash FROM users WHERE email = ?",
            (email,)
        )

        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user[2], password):

            session["user_id"] = user[0]
            session["username"] = user[1]

            return redirect(url_for("profile"))

        else:
            message = "البريد الإلكتروني أو كلمة المرور غير صحيحة."

    return render_template_string(STYLE + """
    <div class="navbar">
        <div class="logo">SBook</div>
    </div>

    <div class="container">
        <div class="card">

            <h2>تسجيل الدخول</h2>

            {% if message %}
                <div class="message">{{ message }}</div>
            {% endif %}

            <form method="POST">

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

            <p style="text-align:center;">
                ليس لديك حساب؟
                <a href="/register">إنشاء حساب</a>
            </p>

        </div>
    </div>
    """, message=message)


# =========================
# الملف الشخصي
# =========================
@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect(url_for("login"))

    username = session.get("username", "مستخدم")

    return render_template_string(STYLE + """
    <div class="navbar">
        <div class="logo">SBook</div>
        <a href="/logout" style="color:white;">
            تسجيل الخروج
        </a>
    </div>

    <div class="container">
