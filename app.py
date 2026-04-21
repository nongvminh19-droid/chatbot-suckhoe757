from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# ===== LOAD DATA =====
try:
    with open("dataset.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    print("Lỗi load dataset:", e)
    data = []

# ===== BIẾN NGỮ CẢNH =====
context = ""

# ===== STOPWORDS =====
stopwords = ["tôi", "bị", "là", "có", "hay", "và", "cảm", "thấy"]

def preprocess(text):
    text = text.lower()
    words = text.split()
    words = [w for w in words if w not in stopwords]
    return " ".join(words)

# ===== CHECK NGUY HIỂM =====
def check_danger(text):
    danger_keywords = ["khó thở", "đau ngực", "ngất"]
    for k in danger_keywords:
        if k in text:
            return "⚠️ Dấu hiệu nguy hiểm! Hãy đi bệnh viện ngay."
    return None

# ===== MATCH TRIỆU CHỨNG =====
def find_best_match(text):
    best = None
    max_score = 0

    for item in data:
        score = 0
        for s in item.get("symptoms", []):
            if s in text:
                score += 1

        if score > max_score:
            max_score = score
            best = item

    return best, max_score

# ===== FORMAT TRẢ LỜI =====
def format_response(item):
    return f"""
🩺 {item.get('disease', 'Không rõ')}

👉 {item.get('advice', '')}

🏠 {item.get('home_care', '')}

⚠️ {item.get('when_to_see_doctor', '')}
"""

# ===== ROUTE TRANG CHÍNH =====
@app.route("/")
def home():
    return render_template("index.html")

# ===== CHAT API =====
@app.route("/chat", methods=["POST"])
def chat():
    global context
    try:
        user_input = request.json.get("message", "").strip()
        print("User:", user_input)

        if not user_input:
            return jsonify({"reply": "Bạn chưa nhập nội dung."})

        processed = preprocess(user_input)
        context += " " + processed

        # ⚠️ check nguy hiểm
        danger = check_danger(context)
        if danger:
            context = ""
            return jsonify({"reply": danger})

        # 🔍 tìm bệnh
        best, score = find_best_match(context)

        if best and score >= 2:
            reply = format_response(best)
            context = ""
        else:
            reply = "Bạn có thể mô tả rõ hơn triệu chứng không?"

        return jsonify({"reply": reply})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"reply": "⚠️ Server đang lỗi, thử lại sau."})

# ===== CHẠY APP =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)