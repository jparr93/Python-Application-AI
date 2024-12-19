from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = "your-openai-api-key"

@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    if request.method == "POST":
        user_input = request.form["user_input"]
        if user_input:
            try:
                # Call OpenAI API
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": user_input}
                    ]
                )
                response_text = response["choices"][0]["message"]["content"]
            except Exception as e:
                response_text = f"Error: {str(e)}"
    return render_template("index.html", response_text=response_text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
