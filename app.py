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
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f2f4f8;
            color: #222;
        }

        .container {
            max-width: 600px;
            margin: 80px auto;
            padding: 20px;
        }

        .card {
            background: white;
            padding: 40px 25px;
            border-radius: 25px;
            text-align: center;
            box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        }

        h1 {
            color: #1877f2;
            font-size: 32px;
        }

        p {
            font-size: 20px;
            margin: 25px 0;
        }

        button {
            border: none;
            background: #1877f2;
            color: white;
            padding: 15px 35px;
            border-radius: 12px;
            font-size: 18px;
            cursor: pointer;
        }

        button:hover {
            background: #0d65d9;
        }
    </style>
</head>

<body>

<div class="container">
    <div class="card">

        <h1>👋 مرحباً بك</h1>

        <p>هذا هو موقعي الإلكتروني</p>

        <button onclick="alert('أهلاً بك في موقعي!')">
            عن الموقع
        </button>

    </div>
</div>

</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
