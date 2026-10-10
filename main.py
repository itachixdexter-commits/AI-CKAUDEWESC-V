from flask import Flask, request, jsonify
import os
import re
import urllib.request
import json

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    try:
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            return jsonify({"error": "API key missing"}), 500

        data = request.get_json()
        if not data or "prompt" not in data:
            return jsonify({"error": "missing prompt"}), 400

        body = json.dumps({
            "model": "google/gemini-2.0-flash-exp:free",
            "messages": [
                {
                    "role": "user",
                    "content": "Write a Roblox executor Lua script only, no markdown, no explanation, no code blocks:\n" + data["prompt"]
                }
            ]
        }).encode("utf-8")

        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=body,
            headers={
                "Authorization": "Bearer " + api_key,
                "Content-Type": "application/json",
                "HTTP-Referer": "https://roblox.com",
                "X-Title": "RV HUB"
            },
            method="POST"
        )

        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))

        code = result["choices"][0]["message"]["content"]
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
