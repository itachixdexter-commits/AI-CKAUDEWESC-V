from flask import Flask, request, jsonify
import google.generativeai as genai
import os
import re

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return jsonify({"error": "API key missing"}), 500

        data = request.get_json()
        if not data or "prompt" not in data:
            return jsonify({"error": "missing prompt"}), 400

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(
            "Write a Roblox executor Lua script only, no markdown, no explanation, no code blocks:\n" + data["prompt"]
        )

        code = response.text
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
