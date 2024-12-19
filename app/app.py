from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT = "https://oai-jp-app-test.openai.azure.com/"
AZURE_OPENAI_API_KEY = "CFKJHXGlMyA8TP8l5ymQFTYjLQw3gAMlBLhasxbfkl9GC3YdXeCkJQQJ99ALACmepeSXJ3w3AAABACOG9JOw"
DEPLOYMENT_NAME = "gpt-4"  # Replace with the name of your deployed model
API_VERSION = "2023-05-15"

@app.route("/", methods=["GET", "POST"])
def index():
    chatbot_response = ""
    if request.method == "POST":
        user_input = request.form["user_input"]
        if user_input.strip():
            try:
                # Make a request to Azure OpenAI Service
                url = f"{AZURE_OPENAI_ENDPOINT}openai/deployments/{DEPLOYMENT_NAME}/chat/completions?api-version={API_VERSION}"
                headers = {
                    "Content-Type": "application/json",
                    "api-key": AZURE_OPENAI_API_KEY
                }
                payload = {
                    "messages": [{"role": "user", "content": user_input}],
                    "max_tokens": 150,
                    "temperature": 0.7
                }
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()
                response_data = response.json()
                chatbot_response = response_data["choices"][0]["message"]["content"]
            except Exception as e:
                chatbot_response = f"Error: {str(e)}"
    return render_template("index.html", chatbot_response=chatbot_response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
