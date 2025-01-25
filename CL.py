import openai
from IPython.display import display, Markdown
from IPython import get_ipython

# Set the OpenAI API base URL and your API key
openai.api_base = "https://api.openai.com/v1"
openai.api_key = "your_openai_api_key_here"

# Initial knowledge about Composite Labs and Monad
initial_context = """
You are an expert on Composite Labs and Monad. Provide concise, accurate, and relevant answers to user queries.

### Composite Labs:
- A venture-backed startup developing a next-generation decentralized exchange (DEX) entirely on-chain.
- Key offerings: spot trading, perpetual contracts, and on-chain lending.
- Unique features: central limit order book (CLOB), cross-margin mechanism, enhanced leverage, and low fees.
- Builds on the Monad blockchain for scalability and efficiency.

### Monad:
- A high-performance layer 1 blockchain designed for 10,000 transactions per second, 1-second block times, and single-slot finality.
- 100% Ethereum Virtual Machine (EVM) compatible.
- Innovations include optimistic parallel execution, asynchronous execution, and MonadDB for efficient state storage.
- Backed by $225M funding from Paradigm, Electric Capital, and Greenoaks.

Answer queries in a professional manner, sticking to the scope of Composite Labs and Monad.
"""

conversation_history = [
    {"role": "system", "content": initial_context}
]

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

def chatbot():
    print("Chatbot is ready to discuss Composite Labs and Monad! Type 'exit' to end the chat.\n")

    while True:
        # Get user input
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break

        # Add user's input to the conversation history
        conversation_history.append({"role": "user", "content": user_input})

        try:
            # Call the OpenAI API for chat completion
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Use a valid OpenAI model
                messages=conversation_history,
                temperature=0.5,
                max_tokens=256,
                top_p=1.0
            )

            # Extract and print the assistant's response
            assistant_message = response["choices"][0]["message"]["content"]

            # Check if the response contains code to execute
            if "```python" in assistant_message:
                code_block = assistant_message.split("```python")[1].split("```")[0].strip()
                code_output = execute_code(code_block)
                assistant_message += f"\n\nCode Output:\n```\n{code_output}\n```"

            print(f"Chatbot: {assistant_message}")

            # Add the assistant's response to the conversation history
            conversation_history.append({"role": "assistant", "content": assistant_message})

        except Exception as e:
            print(f"Chatbot: Sorry, something went wrong. ({e})")

if __name__ == "__main__":
    chatbot()
