from flask import Flask, request, session
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-key")


PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>F-Connect</title>

<style>
*{box-sizing:border-box}

body{
    margin:0;
    background:#f0f2f5;
    font-family:Arial,sans-serif;
}

.top{
    text-align:center;
    padding-top:45px;
}

.logo{
    display:inline-flex;
    width:70px;
    height:70px;
    border-radius:18px;
    align-items:center;
    justify-content:center;
    background:#2867d8;
    color:white;
    font-size:52px;
    font-weight:bold;
}

.name{
    font-size:22px;
    color:#2867d8;
    font-weight:bold;
    margin-top:10px;
}

.card{
    width:400px;
    max-width:92%;
    margin:25px auto;
    background:white;
    padding:22px;
    border-radius:10px;
    box-shadow:0 2px 12px #0002;
}

h1{
    text-align:center;
    font-size:25px;
    font-weight:400;
}

input{
    width:100%;
    padding:16px;
    margin-top:12px;
    border:1px solid #ccd0d5;
    border-radius:7px;
    font-size:16px;
}

button{
    width:100%;
    margin-top:15px;
    padding:14px;
    border:0;
    border-radius:7px;
    background:#2867d8;
    color:white;
    font-size:18px;
    font-weight:bold;
}

.link{
    display:block;
    text-align:center;
    margin:18px;
    color:#2867d8;
    text-decoration:none;
}

hr{
    border:0;
    border-top:1px solid #ddd;
}

.create{
    display:block;
    width:70%;
    margin:20px auto 5px;
    padding:13px;
    text-align:center;
    border:1px solid #42b72a;
    color:#309b20;
    border-radius:7px;
    text-decoration:none;
    font-weight:bold;
}

.footer{
    text-align:center;
    color:#777;
    font-size:13px;
    margin-top:25px;
}
</style>
</head>

<body>

<div class="top">
    <div class="logo">f</div>
    <div class="name">F-Connect</div>
</div>

<div class="card">

<h1>تسجيل الدخول</h1>

<form action="/login" method="POST">

<input
type="text"
name="email"
placeholder="البريد الإلكتروني أو رقم الهاتف"
required>

<input
type="password"
name="password"
placeholder="كلمة المرور"
required>

<button type="submit">
تسجيل الدخول
</button>

</form>

<a class="link" href="#">
هل نسيت كلمة المرور؟
</a>

<hr>

<a class="create" href="/register">
إنشاء حساب جديد
</a>

</div>

<div class="footer">
الخصوصية · الشروط
</div>

</body>
</html>
"""


@app.route("/")
def home():
    return PAGE


@app.route("/login", methods=["POST"])
def login():
    # تسجيل دخول تجريبي لموقعك فقط
    email = request.form.get("email", "")
    session["user"] = email

    return """
    <div style="text-align:center;font-family:Arial;margin-top:100px">
        <h2>مرحباً بك في F-Connect</h2>
        <p>تم تسجيل الدخول إلى الحساب التجريبي.</p>
        <a href="/">العودة</a>
    </div>
    """


@app.route("/register")
def register():
    return """
    <div style="text-align:center;font-family:Arial;margin-top:100px">
        <h2>إنشاء حساب جديد</h2>
        <p>هذه صفحة إنشاء حساب لموقع F-Connect.</p>
        <a href="/">العودة لتسجيل الدخول</a>
    </div>
    """


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
