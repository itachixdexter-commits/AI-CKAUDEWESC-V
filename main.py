from flask import Flask, request, jsonify
import anthropic
import os
import re

app = Flask(__name__)

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    if not data or "prompt" not in data:
        return jsonify({"error": "missing prompt"}), 400

    prompt = data["prompt"]

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"اكتب سكريبت Lua لـ Roblox executor فقط الكود بدون شرح ولا ماركداون ولا ```:\n{prompt}"
            }
        ]
    )

    code = message.content[0].text
    code = re.sub(r"```(?:lua)?|```", "", code).strip()

    return jsonify({"code": code})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
