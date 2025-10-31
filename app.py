# app.py
from flask import Flask, render_template, request
from draw_bot import process_command
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def command():
    prompt = request.form.get('prompt', '')
    if not prompt:
        return "No prompt provided.", 400
    try:
        result = process_command(prompt)
        return f"[{prompt}] -> {result}"
    except Exception as e:
        logging.exception("Error while processing command")
        return f"ERROR: {e}", 500

if __name__ == "__main__":
    app.run(debug=True)
