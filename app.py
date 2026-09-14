from flask import Flask, redirect, request, session, url_for
import os
import secrets
import requests

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))

FACEBOOK_APP_ID = os.environ.get("FACEBOOK_APP_ID")
FACEBOOK_APP_SECRET = os.environ.get("FACEBOOK_APP_SECRET")

# غيّر هذا إذا استخدمت إصدار Graph API آخر في تطبيق Meta
FACEBOOK_API_VERSION = os.environ.get("FACEBOOK_API_VERSION", "v23.0")

REDIRECT_URI = os.environ.get(
    "FACEBOOK_REDIRECT_URI",
    "https://my-website-9rh8.onrender.com/auth/facebook/callback"
)


@app.route("/")
def home():

    if "facebook_user" in session:
        user = session["facebook_user"]

        name = user.get("name", "المستخدم")

        return f"""
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport"
                  content="width=device-width, initial-scale=1.0">
            <title>حسابي</title>

            <style>
                body {{
                    font-family: Arial;
                    background: #f0f2f5;
                    text-align: center;
                    padding-top: 100px;
                }}

                .box {{
                    background: white;
                    max-width: 400px;
                    margin: auto;
                    padding: 30px;
                    border-radius: 15px;
                    box-shadow: 0 3px 15px #0002;
                }}

                a {{
                    color: #1877f2;
                    text-decoration: none;
                }}
            </style>
        </head>

        <body>

            <div class="box">

                <h2>مرحباً {name} 👋</h2>

                <p>تم تسجيل الدخول بنجاح.</p>

                <a href="/logout">
                    تسجيل الخروج
                </a>

            </div>

        </body>
        </html>
        """

    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <title>تسجيل الدخول</title>

        <style>

            body {
                margin: 0;
                background: #f0f2f5;
                font-family: Arial;
                text-align: center;
            }

            .box {
                max-width: 400px;
                margin: 100px auto;
                background: white;
                padding: 35px;
                border-radius: 15px;
                box-shadow: 0 3px 15px #0002;
            }

            h1 {
                color: #1877f2;
            }

            .facebook {
                display: block;
                background: #1877f2;
                color: white;
                padding: 15px;
                border-radius: 8px;
                text-decoration: none;
                font-size: 18px;
                margin-top: 25px;
            }

        </style>
    </head>

    <body>

        <div class="box">

            <h1>موقعي</h1>

            <h2>تسجيل الدخول</h2>

            <p>
                يمكنك استخدام حساب Facebook
                لتسجيل الدخول بأمان.
            </p>

            <a class="facebook" href="/login/facebook">
                تسجيل الدخول باستخدام Facebook
            </a>

        </div>

    </body>

    </html>
    """


@app.route("/login/facebook")
def facebook_login():

    if not FACEBOOK_APP_ID:
        return "FACEBOOK_APP_ID غير موجود في إعدادات Render", 500

    state = secrets.token_urlsafe(32)
    session["oauth_state"] = state

    facebook_url = (
        f"https://www.facebook.com/{FACEBOOK_API_VERSION}/dialog/oauth"
        f"?client_id={FACEBOOK_APP_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&state={state}"
        f"&scope=email,public_profile"
    )

    return redirect(facebook_url)


@app.route("/auth/facebook/callback")
def facebook_callback():

    if request.args.get("error"):
        return """
        <h2 style="text-align:center">
            تم إلغاء تسجيل الدخول.
        </h2>
        <p style="text-align:center">
            يمكنك العودة والمحاولة مرة أخرى.
        </p>
        """

    state = request.args.get("state")

    if not state or state != session.get("oauth_state"):
        return "طلب OAuth غير صالح.", 400

    code = request.args.get("code")

    if not code:
        return "لم يتم الحصول على رمز تسجيل الدخول.", 400

    if not FACEBOOK_APP_ID or not FACEBOOK_APP_SECRET:
        return "إعدادات Facebook غير مكتملة في Render.", 500

    # الحصول على Access Token
    token_url = (
        f"https://graph.facebook.com/"
        f"{FACEBOOK_API_VERSION}/oauth/access_token"
    )

    token_response = requests.get(
        token_url,
        params={
            "client_id": FACEBOOK_APP_ID,
            "client_secret": FACEBOOK_APP_SECRET,
            "redirect_uri": REDIRECT_URI,
            "code": code
        },
        timeout=15
    )

    token_data = token_response.json()

    access_token = token_data.get("access_token")

    if not access_token:
        return "فشل الحصول على Access Token.", 400

    # الحصول على معلومات المستخدم المسموح بها
    user_response = requests.get(
        f"https://graph.facebook.com/"
        f"{FACEBOOK_API_VERSION}/me",
        params={
            "fields": "id,name,email",
            "access_token": access_token
        },
        timeout=15
    )

    user_data = user_response.json()

    if "error" in user_data:
        return "تعذر الحصول على معلومات الحساب.", 400

    session["facebook_user"] = user_data

    session.pop("oauth_state", None)

    return redirect(url_for("home"))


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
      )
