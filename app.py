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

    <title>eFootball - المكافآت</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, Tahoma, sans-serif;
            background: #07101f;
            color: white;
        }

        .container {
            width: 92%;
            max-width: 700px;
            margin: auto;
            padding: 15px 0 40px;
        }

        /* الصور */
        .banner {
            width: 100%;
            border-radius: 16px;
            overflow: hidden;
            margin-bottom: 20px;
            border: 1px solid #26364d;
            box-shadow: 0 5px 20px rgba(0,0,0,.5);
            background: #101b2d;
        }

        .banner img {
            width: 100%;
            display: block;
        }

        /* البطاقة الرئيسية */
        .card {
            background: #1b283b;
            border-radius: 22px;
            padding: 28px 20px;
            box-shadow: 0 8px 30px rgba(0,0,0,.4);
        }

        h1 {
            text-align: center;
            color: #39bfff;
            font-size: 29px;
            margin: 0 0 22px;
            line-height: 1.5;
        }

        .description {
            color: #d5dce7;
            font-size: 18px;
            line-height: 2;
            text-align: center;
            margin-bottom: 22px;
        }

        /* المكافآت */
        .rewards {
            display: flex;
            justify-content: space-around;
            align-items: center;
            background: #0d1729;
            border: 1px solid #293852;
            border-radius: 15px;
            padding: 20px 8px;
            margin-bottom: 25px;
        }

        .reward {
            text-align: center;
            width: 33%;
        }

        .reward .number {
            color: #ffd21c;
            font-size: 21px;
            font-weight: bold;
            margin-bottom: 8px;
        }

        .reward .label {
            color: #aab4c5;
            font-size: 14px;
        }

        /* زر الاستلام */
        .claim {
            display: block;
            width: 100%;
            border: none;
            border-radius: 10px;
            padding: 17px;
            background: linear-gradient(90deg,#ed174b,#f5264f);
            color: white;
            font-size: 21px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 5px 15px rgba(237,23,75,.3);
        }

        .claim:active {
            transform: scale(.98);
        }

        .note {
            text-align: center;
            color: #8794a8;
            font-size: 13px;
            margin-top: 18px;
            line-height: 1.8;
        }

        /* نافذة المكافأة */
        .popup {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,.75);
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .popup-box {
            width: 100%;
            max-width: 400px;
            background: #1b283b;
            border-radius: 20px;
            padding: 30px 20px;
            text-align: center;
            border: 1px solid #344761;
        }

        .popup-box h2 {
            color: #39bfff;
            margin-top: 0;
        }

        .close {
            margin-top: 20px;
            background: #33435a;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            font-size: 16px;
        }

        /* الهاتف */
        @media(max-width:450px) {

            h1 {
                font-size: 25px;
            }

            .description {
                font-size: 16px;
            }

            .reward .number {
                font-size: 17px;
            }

            .reward .label {
                font-size: 12px;
            }
        }
    </style>
</head>

<body>

<div class="container">

    <!-- الصورة الأولى -->
    <div class="banner">
        <img src="https://placehold.co/700x380/080b55/ffffff?text=eFootball+2027+Pack"
             alt="eFootball Pack">
    </div>

    <!-- الصورة الثانية -->
    <div class="banner">
        <img src="https://placehold.co/700x380/080b55/ffffff?text=Lionel+Messi+Pack"
             alt="Player Pack">
    </div>

    <!-- المحتوى -->
    <div class="card">

        <h1>
            فعالية شحن ومكافآت eFootball<br>
            الحصرية
        </h1>

        <div class="description">
            احتفالاً بالموسم الجديد، نقدم مكافآت
            تجريبية للاعبين تشمل عملات وعناصر
            ومحتوى خاص باللعبة.
        </div>

        <div class="rewards">

            <div class="reward">
                <div class="number">⭐ L. Yamal</div>
                <div class="label">حزمة النجوم</div>
            </div>

            <div class="reward">
                <div class="number">⭐ L. Messi</div>
                <div class="label">حزمة الأساطير</div>
            </div>

            <div class="reward">
                <div class="number">🪙 1000</div>
                <div class="label">عملة كوينز</div>
            </div>

        </div>

        <button class="claim" onclick="claimReward()">
            🎁 استلام المكافأة الآن
        </button>

        <div class="note">
            هذا الموقع نموذج تجريبي غير رسمي.
            لا تدخل كلمة مرور حسابك أو بياناتك الشخصية.
        </div>

    </div>

</div>

<!-- النافذة -->
<div class="popup" id="popup">

    <div class="popup-box">

        <h2>🎁 المكافأة</h2>

        <p>
            تم الضغط على زر استلام المكافأة.
        </p>

        <p>
            هذا نموذج تجريبي فقط.
        </p>

        <button class="close" onclick="closePopup()">
            إغلاق
        </button>

    </div>

</div>

<script>

function claimReward() {
    document.getElementById("popup").style.display = "flex";
}

function closePopup() {
    document.getElementById("popup").style.display = "none";
}

</script>

</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
