import json
import random

# Load dataset
with open("dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def get_response(user_input):
    user_input = user_input.lower()

    for item in data:
        question = item["messages"][0]["content"].lower()
        answer = item["messages"][1]["content"]

        if question in user_input:
            return answer

    return "Xin lỗi, tôi chưa hiểu rõ. Bạn có thể nói rõ hơn không?"