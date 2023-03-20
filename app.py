import os
import json
import openai
from flask import Flask, render_template, request, jsonify
from openai import error
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate-text", methods=["POST"])
def generate_text():
    try:
        prompt = request.form["prompt"]
        print("Prompt:", prompt)
        max_tokens = int(request.form["max_tokens"])
        system_message = request.form["system_message"]
        system_message += ".  " if not system_message.endswith('.') else "  "
        system_message += "If asked to generate code and only code, encapsulate the code in '```'."
        print("System Message:", system_message)
        messages = json.loads(request.form["messages"])
        messages.insert(0, {"role": "system", "content": system_message})
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.7,
        )
        print("Response:", response["choices"]
              [0]["message"]["content"].strip())
        return jsonify(response["choices"][0]["message"]["content"].strip())
    except error.RateLimitError:
        return jsonify({"error": "RateLimitError: The server had an error while processing your request. Sorry about that!"})


@app.route("/clear-context", methods=["POST"])
def clear_context():
    return jsonify({"status": "success"})


if __name__ == "__main__":
    app.run(debug=True)
