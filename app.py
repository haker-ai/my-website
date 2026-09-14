from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>موقعي - تسجيل الدخول</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f0f2f5;
            color: #333;
        }

        .logo {
            text-align: center;
            padding-top: 90px;
            padding-bottom: 25px;
        }

        .logo-circle {
            width: 85px;
            height: 85px;
            margin: auto;
            border-radius: 50%;
            background: #1877f2;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 55px;
            font-weight: bold;
        }

        .site-name {
            margin-top: 15px;
            font-size: 30px;
            font-weight: bold;
            color: #1877f2;
        }

        .login-box {
            background: white;
            max-width: 500px;
            margin: 0 auto;
            padding: 30px 35px 35px;
            border-radius: 15px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.15);
        }

        .languages {
            text-align: center;
            margin-bottom: 25px;
            color: #666;
            font-size: 17px;
        }

        .languages span {
            margin: 0 7px;
        }

        input {
            width: 100%;
            padding: 18px;
            margin-bottom: 15px;
            border: 1px solid #ddd;
            border-radius: 10px;
            font-size: 17px;
            text-align: right;
            outline: none;
        }

        input:focus {
            border-color: #1877f2;
            box-shadow: 0 0 0 2px rgba(24,119,242,0.15);
        }

        .login-button {
            width: 100%;
            padding: 17px;
            border: none;
            border-radius: 10px;
            background: #1877f2;
            color: white;
            font-size: 21px;
            font-weight: bold;
            cursor: pointer;
        }

        .login-button:hover {
            background: #166fe5;
        }

        .forgot {
            display: block;
            text-align: center;
            margin-top: 22px;
            color: #1877f2;
            text-decoration: none;
            font-size: 17px;
        }

        .message {
            text-align: center;
            margin-bottom: 15px;
            color: #1877f2;
            font-weight: bold;
        }

        .footer {
            text-align: center;
            margin-top: 30px;
            color: #777;
            font-size: 14px;
        }

        @media (max-width: 550px) {
            .logo {
                padding-top: 55px;
            }

            .login-box {
                margin: 0 12px;
                padding: 25px 20px 30px;
            }
        }
    </style>
</head>

<body>

    <div class="logo">
        <div class="logo-circle">م</div>
        <div class="site-name">موقعي</div>
    </div>

    <div class="login-box">

        <div class="languages">
            <span>Français</span>
            |
            <span>English</span>
            |
            <span>العربية</span>
        </div>

        {% if message %}
            <div class="message">{{ message }}</div>
        {% endif %}

        <form method="POST">

            <input
                type="text"
                name="username"
                placeholder="البريد الإلكتروني أو رقم الهاتف"
                required
            >

            <input
                type="password"
                name="password"
                placeholder="كلمة السر"
                required
            >

            <button class="login-button" type="submit">
                تسجيل الدخول
            </button>

        </form>

        <a href="#" class="forgot">
            هل نسيت كلمة السر؟
        </a>

    </div>

    <div class="footer">
        © 2026 موقعي - جميع الحقوق محفوظة
    </div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():

    message = ""

    if request.method == "POST":
        username = request.form.get("username", "")

        # عرض رسالة تجريبية فقط.
        # لا يتم حفظ كلمة المرور أو إرسالها لأي جهة.
        if username:
            message = "تم إرسال طلب تسجيل الدخول بشكل تجريبي."

    return render_template_string(HTML, message=message)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )
