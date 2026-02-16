import os
from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)

# --- CONFIGURATION ---
API_KEY = os.environ.get("GEMINI_API_KEY")

# Initialize Gemini client
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY environment variable not set!")

client = genai.Client(api_key=API_KEY)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(silent=True)

    if not data or "message" not in data:
        return jsonify({"error": "Invalid JSON or 'message' missing"}), 400

    user_input = data["message"].strip()

    if not user_input:
        return jsonify({"error": "Message is empty"}), 400

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=user_input
        )

        return jsonify({
            "reply": response.text
        })

    except Exception as e:
        return jsonify({
            "error": "Gemini API error",
            "details": str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

