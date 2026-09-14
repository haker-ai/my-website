from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>SBook - تسجيل الدخول</title>

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: #f0f2f5;
    font-family: Arial, sans-serif;
    color: #333;
}

.top {
    text-align: center;
    padding-top: 45px;
}

.languages {
    color: #4267a9;
    font-size: 17px;
    margin-bottom: 55px;
}

.logo {
    width: 82px;
    height: 82px;
    border-radius: 50%;
    background: #1877f2;
    color: white;
    font-size: 55px;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: auto;
}

.card {
    width: 92%;
    max-width: 620px;
    margin: 35px auto;
}

input {
    width: 100%;
    height: 70px;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 0 20px;
    font-size: 18px;
    margin-bottom: 12px;
    background: white;
}

.login {
    width: 100%;
    height: 68px;
    border: none;
    border-radius: 9px;
    background: #1877f2;
    color: white;
    font-size: 23px;
    font-weight: bold;
}

.forgot {
    display: block;
    text-align: center;
    margin: 25px;
    color: #1877f2;
    font-size: 18px;
}

.line {
    border-top: 1px solid #ddd;
    margin: 35px 0;
}

.create {
    display: block;
    width: 100%;
    height: 65px;
    border: 2px solid #42b72a;
    border-radius: 9px;
    background: transparent;
    color: #42b72a;
    font-size: 21px;
    font-weight: bold;
}

.footer {
    text-align: center;
    margin-top: 50px;
    color: #777;
    font-size: 14px;
}
</style>
</head>

<body>

<div class="top">

    <div class="languages">
        العربية | English | Français
    </div>

    <div class="logo">S</div>

</div>

<div class="card">

    <form method="POST" action="/login">

        <input
            type="email"
            name="email"
            placeholder="البريد الإلكتروني أو رقم الهاتف"
            required
        >

        <input
            type="password"
            name="password"
            placeholder="كلمة السر"
            required
        >

        <button class="login" type="submit">
            تسجيل الدخول
        </button>

    </form>

    <a class="forgot" href="#">
        هل نسيت كلمة السر؟
    </a>

    <div class="line"></div>

    <button class="create" onclick="location.href='/register'">
        إنشاء حساب جديد
    </button>

</div>

<div class="footer">
    SBook © 2026
</div>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/login", methods=["POST"])
def login():
    # هنا يمكنك لاحقاً ربط تسجيل الدخول بقاعدة بياناتك
    return """
    <div style="text-align:center;font-family:Arial;margin-top:100px">
        <h2>تم إرسال طلب تسجيل الدخول</h2>
        <a href="/">العودة</a>
    </div>
    """


@app.route("/register")
def register():
    return """
    <div style="text-align:center;font-family:Arial;margin-top:100px">
        <h2>إنشاء حساب جديد</h2>
        <a href="/">العودة لتسجيل الدخول</a>
    </div>
    """


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
