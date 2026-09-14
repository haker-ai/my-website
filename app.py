from flask import Flask, request, session
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "my-secret-key")


HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">

<head>
<meta charset="UTF-8">
<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>تسجيل الدخول</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: #f0f2f5;
    font-family: Arial, sans-serif;
    color: #1c1e21;
}

/* المساحة العلوية */
.top {
    min-height: 430px;
    display: flex;
    justify-content: center;
    align-items: flex-end;
    padding-bottom: 25px;
}

/* شعار موقعك */
.logo {
    width: 86px;
    height: 86px;
    border-radius: 50%;
    background: #287be8;
    color: white;

    display: flex;
    justify-content: center;
    align-items: center;

    font-size: 70px;
    font-weight: bold;
    font-family: Arial, sans-serif;

    box-shadow: 0 2px 8px #0002;
}

/* صندوق تسجيل الدخول */
.login-box {
    width: 100%;
    max-width: 690px;
    margin: 0 auto;
    background: white;

    padding: 42px 35px 30px;

    border-radius: 16px 16px 0 0;
    box-shadow: 0 -2px 10px #0001;
}

/* اللغات */
.languages {
    text-align: center;
    font-size: 17px;
    color: #4267a5;
    margin-bottom: 35px;
}

.languages span {
    margin: 0 7px;
}

/* الحقول */
input {
    width: 100%;
    height: 62px;

    border: 1px solid #d0d4d9;
    border-radius: 8px;

    padding: 0 20px;

    font-size: 18px;
    color: #333;

    margin-bottom: 14px;

    outline: none;
}

input:focus {
    border: 2px solid #287be8;
}

/* زر الدخول */
.login-button {
    width: 100%;
    height: 64px;

    border: none;
    border-radius: 8px;

    background: #287be8;
    color: white;

    font-size: 22px;
    font-weight: bold;

    cursor: pointer;
}

.login-button:active {
    transform: scale(0.99);
}

/* نسيت كلمة المرور */
.forgot {
    display: block;

    text-align: center;

    margin-top: 25px;

    color: #287be8;
    text-decoration: none;

    font-size: 17px;
}

/* الخط */
.line {
    border: none;
    border-top: 1px solid #ddd;

    margin: 35px 0 25px;
}

/* إنشاء الحساب */
.create {
    display: block;

    width: 300px;
    max-width: 90%;

    margin: auto;

    padding: 15px;

    text-align: center;

    border: 2px solid #42b72a;
    border-radius: 8px;

    color: #329522;

    text-decoration: none;

    font-size: 19px;
    font-weight: bold;
}

/* أسفل الصفحة */
.footer {
    text-align: center;

    color: #777;

    font-size: 14px;

    padding: 28px;
}

/* الهاتف */
@media (max-width: 600px) {

    .top {
        min-height: 400px;
    }

    .login-box {
        padding: 30px 28px 25px;
    }

    .logo {
        width: 78px;
        height: 78px;
        font-size: 62px;
    }

    input {
        height: 60px;
        font-size: 17px;
    }

    .login-button {
        height: 62px;
        font-size: 21px;
    }
}

</style>

</head>

<body>


<!-- الشعار -->

<div class="top">

    <div class="logo">
        f
    </div>

</div>


<!-- صندوق الدخول -->

<div class="login-box">

    <!-- اللغات -->

    <div class="languages">

        <span>العربية</span>
        |
        <span>English</span>
        |
        <span>Français</span>

    </div>


    <!-- تسجيل الدخول -->

    <form action="/login" method="POST">

        <input
            type="text"
            name="email"
            placeholder="رقم الهاتف أو البريد الإلكتروني"
            required
        >

        <input
            type="password"
            name="password"
            placeholder="كلمة السر"
            required
        >

        <button
            type="submit"
            class="login-button">

            تسجيل الدخول

        </button>

    </form>


    <!-- نسيت كلمة السر -->

    <a href="#" class="forgot">

        هل نسيت كلمة السر؟

    </a>


    <hr class="line">


    <!-- إنشاء حساب -->

    <a href="/register" class="create">

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
    return HTML


@app.route("/login", methods=["POST"])
def login():

    email = request.form.get("email", "")

    # تسجيل تجريبي لموقعك
    session["user"] = email

    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>تم الدخول</title>
    </head>

    <body style="
        font-family:Arial;
        text-align:center;
        padding-top:100px;
        background:#f0f2f5;
    ">

        <h2>مرحباً بك 👋</h2>

        <p>تم تسجيل الدخول إلى موقعك.</p>

        <a href="/" style="
            color:#287be8;
            text-decoration:none;
        ">
            العودة
        </a>

    </body>
    </html>
    """


@app.route("/register")
def register():

    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">

    <head>
        <meta charset="UTF-8">
        <title>إنشاء حساب</title>
    </head>

    <body style="
        font-family:Arial;
        text-align:center;
        padding-top:100px;
        background:#f0f2f5;
    ">

        <h2>إنشاء حساب جديد</h2>

        <p>هذه صفحة إنشاء حساب لموقعك.</p>

        <a href="/" style="
            color:#287be8;
            text-decoration:none;
        ">
            العودة لتسجيل الدخول
        </a>

    </body>

    </html>
    """


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
