
from flask import Flask, request, jsonify
import anthropic
import os
import re

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    try:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            return jsonify({"error": "API key missing"}), 500

        data = request.get_json()
        if not data or "prompt" not in data:
            return jsonify({"error": "missing prompt"}), 400

        client = anthropic.Anthropic(api_key=api_key)

        message = client.messages.create(
            model="claude-opus-5-5",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Write a Roblox executor Lua script only, no markdown, no explanation, no code blocks:\n" + data["prompt"]
                }
            ]
        )

        code = message.content[0].text
        code = re.sub(r"```(?:lua)?|```", "", code).strip()

        return jsonify({"code": code})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
