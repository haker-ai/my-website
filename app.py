from flask import Flask, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-me")

@app.route("/", methods=["GET"])
def home():
    return """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>G-Account</title>

<style>
body{
    margin:0;
    font-family:Arial,sans-serif;
    background:#f7f9fc;
    color:#202124;
}

.card{
    width:420px;
    max-width:88%;
    margin:70px auto;
    padding:35px;
    background:white;
    border-radius:18px;
    box-shadow:0 4px 20px #00000018;
}

.logo{
    text-align:center;
    font-size:32px;
    font-weight:bold;
    color:#2864d7;
    margin-bottom:28px;
}

h1{
    text-align:center;
    font-weight:400;
    font-size:27px;
}

p{
    text-align:center;
    color:#666;
}

input{
    width:100%;
    padding:16px;
    margin-top:18px;
    border:1px solid #ccc;
    border-radius:9px;
    font-size:16px;
    box-sizing:border-box;
}

button{
    width:100%;
    margin-top:25px;
    padding:14px;
    border:0;
    border-radius:9px;
    background:#2864d7;
    color:white;
    font-size:16px;
}

a{
    display:block;
    text-align:center;
    margin-top:22px;
    color:#2864d7;
    text-decoration:none;
}

.footer{
    text-align:center;
    margin-top:35px;
    color:#777;
    font-size:13px;
}
</style>
</head>

<body>

<div class="card">

<div class="logo">G-Account</div>

<h1>تسجيل الدخول</h1>

<p>استخدم حسابك للمتابعة</p>

<form action="/login" method="POST">

<input
type="email"
name="email"
placeholder="البريد الإلكتروني أو الهاتف"
required>

<input
type="password"
name="password"
placeholder="كلمة المرور"
required>

<a href="#">هل نسيت البريد الإلكتروني؟</a>

<button type="submit">التالي</button>

</form>

<a href="/register">إنشاء حساب</a>

<div class="footer">
الخصوصية · الشروط
</div>

</div>

</body>
</html>
"""


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "")
    session["user"] = email

    return """
    <div style="text-align:center;font-family:Arial;margin-top:100px">
        <h2>تم تسجيل الدخول</h2>
        <p>مرحباً بك في G-Account</p>
        <a href="/">العودة</a>
    </div>
    """


@app.route("/register")
def register():
    return """
    <div style="text-align:center;font-family:Arial;margin-top:100px">
        <h2>إنشاء حساب</h2>
        <p>هذه صفحة إنشاء حساب لموقعك.</p>
        <a href="/">العودة</a>
    </div>
    """


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
