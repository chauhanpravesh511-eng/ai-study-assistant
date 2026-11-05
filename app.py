from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

GROQ_API_KEY = "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"  # Render ke Environment me daal dena, yahan khaali hi rakh

# Memory ke liye - pichli baat yaad rahegi
chat_history = []

SYSTEM_PROMPT = """You are PA.AI, made by Nitesh. Answer like Meta AI in Hinglish.
Rules:
1. Hamesha simple Hinglish me, short me jawab do, MAX 250 words.
2. Points me samjhao, **bold** use karo.
3. Code hamesha ```python block me do.
4. Agar user DP bole to Dynamic Programming samjho, pichli baat yaad rakho.
"""

def get_ai_reply(user_msg):
    global chat_history
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}

    # Naya msg history me daalo
    chat_history.append({"role": "user", "content": user_msg})
    # Sirf aakhri 10 msg yaad rakho, zyada lamba na ho
    if len(chat_history) > 10:
        chat_history = chat_history[-10:]

    data = {
        "model": "openai/gpt-oss-20b",
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + chat_history
    }
    try:
        r = requests.post(url, headers=headers, json=data, timeout=30)
        res = r.json()
        print(res)
        if "choices" in res:
            reply = res["choices"][0]["message"]["content"]
            chat_history.append({"role": "assistant", "content": reply})
            return reply
        else:
            return f"Groq Error: {res}"
    except Exception as e:
        return f"Error: {e}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_msg = request.json.get('message')
    ai_reply = get_ai_reply(user_msg)
    return jsonify({'reply': ai_reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)