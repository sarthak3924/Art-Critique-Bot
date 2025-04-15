from flask import Flask, render_template, request, send_from_directory
import google.generativeai as genai
import json
import os

# ─────── CONFIGURE GEMINI ───────
genai.configure(api_key="AIzaSyCPSUqQbwi3eawAupE6_lm-kqsKs7OMDSc")  # Your key
model = genai.GenerativeModel("gemini-2.0-flash")

# ─────── SYSTEM PROMPT ───────
SYSTEM_PROMPT = (
    "You are ArtBot — a thoughtful, supportive art critique assistant. "
    "You offer constructive feedback on art, including digital art, paintings, sketches, and design work. "
    "Your tone is encouraging, insightful, and respectful. "
    "You focus on elements like color use, composition, style, mood, and creativity. "
    "Avoid harsh criticism. If someone asks unrelated questions, reply with: "
    "'I'm here to chat about art and creativity only 🎨'. "
    "You can remember names and previous artworks if the user shares them."
)

# ─────── MEMORY SETUP ───────
HISTORY_FILE = "art_chat_history.json"
chat_history = []

if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, 'r') as file:
        try:
            chat_history = json.load(file)
        except json.JSONDecodeError:
            chat_history = []

# Setup Gemini chat with system prompt
chat = model.start_chat(history=[{"role": "user", "parts": SYSTEM_PROMPT}])

app = Flask(_name_)

@app.route('/')
def index():
    try:
        # Render the index.html template from the 'templates' folder
        return render_template('index.html')  
    except Exception as e:
        print(f"Error loading index.html: {e}")
        return f"Error loading index.html: {e}"

@app.route('/style.css')
def serve_css():
    # Serve the CSS file from the 'static' directory
    return send_from_directory('static', 'style.css')

@app.route('/artbot', methods=['POST'])
def artbot_reply():
    user_input = request.form['prompt']

    # Get response from Gemini model
    response = chat.send_message(user_input)
    reply = response.text

    # Save to history
    chat_history.append({"role": "user", "text": user_input})
    chat_history.append({"role": "artbot", "text": reply})
    with open(HISTORY_FILE, "w") as file:
        json.dump(chat_history, file, indent=2)

    return reply  # Return just the reply text

if _name_ == '_main_':
    app.run(debug=True)