from flask import Flask, request, jsonify
import openai

# Initialize the Flask app
app = Flask(__name__)

# Set the Groq API base URL and API key
openai.api_base = "https://api.groq.com/openai/v1"
openai.api_key = "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"

# Initial context for Composite Labs and Monad
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

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("user_input", "")
    conversation_history = data.get("conversation_history", [{"role": "system", "content": initial_context}])

    if not user_input:
        return jsonify({"error": "No user input provided"}), 400

    conversation_history.append({"role": "user", "content": user_input})

    try:
        response = openai.ChatCompletion.create(
            model="llama-3.3-70b-versatile",  # Use an accessible Llama model
            messages=conversation_history,
            temperature=0.5,
            max_tokens=256,
            top_p=1.0,
        )

        assistant_message = response["choices"][0]["message"]["content"]
        conversation_history.append({"role": "assistant", "content": assistant_message})
        return jsonify({"response": assistant_message, "conversation_history": conversation_history})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
