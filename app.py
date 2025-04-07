from flask import Flask, render_template, request, jsonify,send_from_directory
from flask_cors import CORS  
from chatbot.chatbot import chatbot_response  # Import chatbot function
import os

# # Create Flask app
# app = Flask(__name__, static_folder="../../frontend/chatbot-react/build", static_url_path="/")  
# CORS(app)  # Enable CORS for frontend-backend communication

# Serve React frontend
# @app.route("/")
# def serve_react():
#     return send_from_directory(app.static_folder, "index.html")
app = Flask(__name__)
@app.route("/")
def home():
    """Serves the chatbot UI."""
    return render_template("index.html")
# API endpoint for chatbot
@app.route("/chatbot", methods=["POST"])
def chat():
    """Handles chatbot messages and returns responses."""
    user_message = request.json.get("message", "")

    if not user_message:
        return jsonify({"response": "No message received."}), 400  # Handle empty input

    try:
        bot_reply = chatbot_response(user_message)  # Call chatbot function
        return jsonify({"response": bot_reply})
    except Exception as e:
        print(f"❌ [ERROR] {e}")  # Debugging
        return jsonify({"response": "Sorry, an error occurred."}), 500

# Serve static files (CSS, JS, images, etc.)
@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


