from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>موقعي الإلكتروني</title>
        <style>
            body {
                font-family: Arial;
                background: #f2f2f2;
                text-align: center;
                padding: 60px 20px;
            }

            .box {
                max-width: 500px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 4px 15px #bbb;
            }

            h1 {
                color: #1877f2;
            }

            p {
                font-size: 18px;
            }

            a {
                display: inline-block;
                margin-top: 20px;
                padding: 12px 25px;
                background: #1877f2;
                color: white;
                text-decoration: none;
                border-radius: 8px;
            }
        </style>
    </head>

    <body>
        <div class="box">
            <h1>مرحباً بك 👋</h1>
            <p>هذا هو موقعي الإلكتروني</p>
            <a href="/about">عن الموقع</a>
        </div>
    </body>
    </html>
    """

@app.route("/about")
def about():
    return """
    <html lang="ar" dir="rtl">
    <meta charset="UTF-8">
    <h1>عن الموقع</h1>
    <p>تم إنشاء هذا الموقع باستخدام Python و Flask.</p>
    <a href="/">العودة للرئيسية</a>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
