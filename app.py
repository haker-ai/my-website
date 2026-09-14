from flask import Flask, render_template_string, request

app = Flask(__name__)

PAGE = """
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
    min-height: 100vh;
    background: #f8fafd;
    font-family: Arial, sans-serif;
    color: #202124;
}

.container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.card {
    width: 450px;
    max-width: 92%;
    background: white;
    border: 1px solid #dadce0;
    border-radius: 12px;
    padding: 40px;
}

.logo {
    text-align: center;
    font-size: 38px;
    font-weight: bold;
    color: #1877f2;
    margin-bottom: 20px;
}

h1 {
    text-align: center;
    font-size: 28px;
    font-weight: 400;
    margin: 10px;
}

.subtitle {
    text-align: center;
    font-size: 16px;
    margin-bottom: 35px;
}

input {
    width: 100%;
    height: 55px;
    border: 1px solid #777;
    border-radius: 5px;
    padding: 0 15px;
    font-size: 16px;
    margin-bottom: 15px;
}

.next {
    width: 100%;
    height: 48px;
    background: #1877f2;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 17px;
    cursor: pointer;
}

.links {
    margin-top: 25px;
    text-align: center;
}

.links a {
    color: #1877f2;
    text-decoration: none;
    margin: 0 8px;
}

.footer {
    text-align: center;
    margin-top: 30px;
    font-size: 13px;
    color: #777;
}

@media(max-width:500px) {
    .card {
        border: none;
        padding: 25px;
    }
}
</style>
</head>

<body>

<div class="container">

<div class="card">

    <div class="logo">SBook</div>

    <h1>تسجيل الدخول</h1>

    <div class="subtitle">
        استخدام حسابك على SBook
    </div>

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
            placeholder="كلمة المرور"
            required
        >

        <button class="next" type="submit">
            التالي
        </button>

    </form>

    <div class="links">
        <a href="#">هل نسيت البريد الإلكتروني؟</a>
    </div>

    <div class="links">
        <a href="/register">إنشاء حساب</a>
    </div>

    <div class="footer">
        العربية | English | Français
    </div>

</div>

</div>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(PAGE)


@app.route("/login", methods=["POST"])
def login():
    # معالجة تسجيل الدخول لموقعك أنت
    return "تم إرسال طلب تسجيل الدخول."


@app.route("/register")
def register():
    return "صفحة إنشاء الحساب"


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
)
