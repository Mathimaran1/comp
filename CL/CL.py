from flask import Flask, render_template, request
import openai

# Initialize Flask app
app = Flask(__name__)

# OpenAI API configuration
openai.api_base = "https://api.groq.com/openai/v1"
openai.api_key = "your-openai-api-key"  # Replace with your actual API key

@app.route('/')
def home():
    """Render the main page."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages."""
    user_input = request.form.get('message')

    try:
        # OpenAI API call
        response = openai.ChatCompletion.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert on Composite Labs and Monad."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.5,
            max_tokens=256
        )
        assistant_response = response["choices"][0]["message"]["content"]

    except Exception as e:
        assistant_response = f"Error: {str(e)}"

    return render_template('index.html', user_input=user_input, assistant_response=assistant_response)

if __name__ == "__main__":
    app.run(debug=False)  # Set debug=False for production
