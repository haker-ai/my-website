from flask import Flask, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "my-secret-key")


HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>تسجيل الدخول</title>

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: white;
    font-family: Arial, sans-serif;
    color: #202124;
}

.box {
    width: 100%;
    max-width: 450px;
    margin: 55px auto;
    padding: 35px;
}

.logo {
    text-align: center;
    font-size: 34px;
    font-weight: bold;
    margin-bottom: 25px;
    letter-spacing: -2px;
}

.logo span:nth-child(1) { color:#4285f4; }
.logo span:nth-child(2) { color:#ea4335; }
.logo span:nth-child(3) { color:#fbbc05; }
.logo span:nth-child(4) { color:#34a853; }

h1 {
    text-align: center;
    font-size: 28px;
    font-weight: 400;
    margin: 10px 0;
}

.subtitle {
    text-align: center;
    color: #5f6368;
    font-size: 16px;
    margin-bottom: 35px;
}

input {
    width: 100%;
    height: 55px;
    border: 1px solid #dadce0;
    border-radius: 4px;
    padding: 0 15px;
    font-size: 16px;
    margin-bottom: 18px;
    outline: none;
}

input:focus {
    border: 2px solid #4285f4;
}

.forgot {
    color: #1a73e8;
    font-size: 15px;
    margin-bottom: 35px;
    display: block;
    text-decoration: none;
}

.info {
    color: #5f6368;
    font-size: 14px;
    line-height: 1.6;
    margin-bottom: 30px;
}

.info a {
    color: #1a73e8;
    text-decoration: none;
}

.actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.create {
    color: #1a73e8;
    text-decoration: none;
    font-weight: 500;
}

button {
    background: #1a73e8;
    color: white;
    border: 0;
    border-radius: 4px;
    padding: 12px 25px;
    font-size: 15px;
    cursor: pointer;
}

button:hover {
    background: #1765cc;
}

.footer {
    text-align: center;
    margin-top: 45px;
    color: #777;
    font-size: 13px;
}

@media(max-width:500px) {
    .box {
        margin: 20px auto;
        padding: 25px;
    }
}
</style>
</head>

<body>

<div class="box">

    <div class="logo">
        <span>A</span><span>c</span><span>c</span><span>o</span>
    </div>

    <h1>تسجيل الدخول</h1>

    <div class="subtitle">
        باستخدام حسابك للمتابعة
    </div>

    <form method="POST" action="/login">

        <input
            type="email"
            name="email"
            placeholder="البريد الإلكتروني أو الهاتف"
            required
        >

        <input
            type="password"
            name="password"
            placeholder="كلمة المرور"
            required
        >

        <a href="#" class="forgot">
            هل نسيت البريد الإلكتروني؟
        </a>

        <div class="info">
            ليس لديك حساب؟
            <a href="/register">إنشاء حساب</a>
        </div>

        <div class="actions">
            <a href="/register" class="create">
                إنشاء حساب
            </a>

            <button type="submit">
                التالي
            </button>
        </div>

    </form>

    <div class="footer">
        الخصوصية · الشروط
    </div>

</div>

</body>
</html>
"""


@app.route("/")
def home():
    return HTML


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "")

    # لا يتم إرسال كلمة المرور إلى Google أو أي جهة خارجية
    session["user"] = email

    return f"""
    <h2 style="text-align:center;margin-top:100px;">
    مرحباً بك
    </h2>
    <p style="text-align:center;">
    تم تسجيل الدخول إلى حسابك التجريبي.
    </p>
    """


@app.route("/register")
def register():
    return """
    <div style="text-align:center;margin-top:100px;font-family:Arial">
        <h1>إنشاء حساب</h1>
        <p>صفحة إنشاء حساب لموقعك الخاص</p>
        <a href="/">العودة لتسجيل الدخول</a>
    </div>
    """


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
