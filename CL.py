from flask import Flask, request, jsonify, render_template
import openai
from IPython.display import display, Markdown
from IPython import get_ipython

app = Flask(__name__)

# Set the Groq API base URL and your API key for OpenAI
openai.api_base = "https://api.groq.com/openai/v1"
openai.api_key = "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"  # Replace with your actual OpenAI API key

conversation_history = []

def execute_code(code):
    try:
        # Capture the output of the code execution
        ipython = get_ipython()
        if ipython is not None:
            result = ipython.run_cell(code)
            return result.result
        else:
            exec(code, globals())
            return "Code executed successfully."
    except Exception as e:
        return f"Error executing code: {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form.get('message')
    if user_input.lower() == "exit":
        return render_template('index.html', user_input=user_input, assistant_response="Goodbye!")

    # Add user's input to the conversation history
    conversation_history.append({"role": "user", "content": user_input})

    # Create a dynamic system prompt or fetch data from external sources if needed
    system_prompt = "You are an expert chatbot. Provide concise, accurate, and relevant answers to user queries."
    if len(conversation_history) == 1:  # If it's the first query
        conversation_history.insert(0, {"role": "system", "content": system_prompt})

    try:
        # Call the OpenAI API for chat completion using the specified model and API URL
        response = openai.ChatCompletion.create(
            model="llama-3.3-70b-versatile",  # Use the Llama model as requested
            messages=conversation_history,
            temperature=0.5,
            max_tokens=256,
            top_p=1.0
        )

        # Extract the assistant's response
        assistant_message = response["choices"][0]["message"]["content"]

        # Check if the response contains code to execute
        if "```python" in assistant_message:
            code_block = assistant_message.split("```python")[1].split("```")[0].strip()
            code_output = execute_code(code_block)
            assistant_message += f"\n\nCode Output:\n```\n{code_output}\n```"

        # Add the assistant's response to the conversation history
        conversation_history.append({"role": "assistant", "content": assistant_message})

        return render_template('index.html', user_input=user_input, assistant_response=assistant_message)

    except Exception as e:
        return render_template('index.html', user_input=user_input, assistant_response=f"Sorry, something went wrong. ({e})")

if __name__ == '__main__':
    app.run(debug=True)
