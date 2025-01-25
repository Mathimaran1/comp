from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Route for root
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the chatbot API!"})

# Existing chatbot route
@app.route('/chat', methods=['POST'])
def chatbot():
    user_input = request.json.get("user_input")
    if not user_input:
        return jsonify({"error": "No user input provided"}), 400

    # Add user's input to the conversation history
    conversation_history.append({"role": "user", "content": user_input})

    try:
        # Call OpenAI's API for chat completion
        response = openai.ChatCompletion.create(
            model="llama-3.3-70b-versatile",  # Update this if necessary
            messages=conversation_history,
            temperature=0.5,
            max_tokens=256,
            top_p=1.0
        )

        # Extract assistant's response
        assistant_message = response["choices"][0]["message"]["content"]

        # Add assistant's response to the conversation history
        conversation_history.append({"role": "assistant", "content": assistant_message})

        # Return the assistant's response in JSON format
        return jsonify({"response": assistant_message})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Start the Flask app
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
