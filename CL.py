from flask import Flask, request, jsonify, render_template
import openai
from IPython.display import display, Markdown
from IPython import get_ipython

app = Flask(__name__)

# Set the OpenAI API base URL and your API key
openai.api_base = "https://api.groq.com/openai/v1"
openai.api_key = "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"  # Replace with your actual OpenAI API key

# Initial knowledge about Composite Labs and Monad
initial_context = """
You are an expert on Composite Labs and Monad. Provide concise, accurate, and relevant answers to user queries based on the following comprehensive information:

### Composite Labs:
- A venture-backed startup developing a next-generation decentralized exchange (DEX) entirely on-chain.
- **Key Offerings**:
  - **Spot Trading**: Facilitates direct cryptocurrency trading on the blockchain, ensuring transparency and deep liquidity.
  - **Perpetual Contracts**: Offers perpetual contracts for speculative trading without expiry, supporting leverage for traders.
  - **On-Chain Lending**: Enables decentralized lending and borrowing, allowing users to earn interest or access liquidity without intermediaries.
- **Unique Features**:
  - **Central Limit Order Book (CLOB)**: A traditional order-matching system offering efficient price discovery, reduced slippage, and a professional trading experience.
  - **Cross-Margin Mechanism**: Allows traders to use their entire portfolio as collateral for enhanced capital efficiency and risk management.
  - **Low Fees**: Offers a cost-effective trading experience with uniform fees for trades of all sizes.
  - **Fully On-Chain**: The DEX is fully composable, permissionless, and decentralized, deployable on any Ethereum Virtual Machine (EVM)-compatible blockchain.
  - **No App-Chains or Hybrids**: Transparent, public on-chain code with no hidden backdoors or compromises.
- **Integration with Monad**: Leverages Monad’s high-performance blockchain infrastructure for scalability, low latency, and operational efficiency.

### Monad:
- A high-performance Layer 1 blockchain designed to support Composite Labs and other applications requiring scalability, efficiency, and low fees.
- **Key Features**:
  - **High Throughput**: Capable of handling 10,000 transactions per second (TPS).
  - **Low Latency**: Achieves 1-second block times with immediate transaction finality.
  - **Single-Slot Finality**: Guarantees immediate and secure transaction confirmation without rollbacks.
  - **100% EVM Compatibility**: Fully compatible with Ethereum-based applications, enabling seamless migration of projects to Monad.
  - **Advanced Innovations**:
    - **Optimistic Parallel Execution**: Executes transactions in parallel to maximize throughput.
    - **Asynchronous Execution**: Improves performance with non-blocking transaction processing.
    - **MonadDB**: A specialized state storage solution for efficient on-chain data management.
- **Funding and Support**:
  - Backed by $225M in funding from investors including Paradigm, Electric Capital, and Greenoaks.
  - Designed to meet the demands of large-scale decentralized applications (dApps) while maintaining affordability and reliability.

### Key Individuals and Contributors:
- **Composite Labs Founders**:
  - **Francesco Adiliberti (CEO)**: Over 25 years in capital markets and six years in blockchain technology.
  - **Moh (CTO)**: 40+ years of software development experience, leading technological innovation at Composite Labs.
  - **Akul Penugonda (Co-founder)**: Background in tech, with roles at Yext, Qualcomm, and education from Carnegie Mellon, Harvard, and The University of Hong Kong.
  - **Lucas Gaylord (COO)**: Previously Co-founder and CTO of Nomisma, specializing in digital asset derivatives.
- **Monad Founders**:
  - **Keone Hon (CEO)**: Previously worked at Jump Trading, building high-frequency trading systems.
  - **Eunice Giarta and James Hunsaker**: Co-founders with expertise in blockchain scalability and infrastructure.
- **DoctorPreballin**:
  - An online alias active in the DeFi community, contributing through music-themed content and promoting community engagement.
- **Kiddo**:
  - Active within Monad, known for launching "Mach 2: NFT," an accelerator program to support NFT projects through expert guidance and marketing strategies.

### Vision and Goals:
Composite Labs and Monad work symbiotically to address the shortcomings of existing decentralized exchanges:
1. **Unified Trading**: Combines spot trading, perpetual contracts, and lending under a single venue using a high-performance CLOB-based system.
2. **Capital Efficiency**: Introduces portfolio margining and cross-collateral mechanisms for enhanced trading efficiency.
3. **Scalability and Speed**: Leverages Monad's performance to provide real-time trading experiences with low fees and high security.
4. **Decentralization**: Ensures that all processes are transparent, permissionless, and entirely on-chain.

### Why Composite Labs and Monad Are Unique:
- Composite Labs redefines DeFi by combining a professional trading experience with the flexibility of blockchain technology.
- Monad serves as the scalable infrastructure for the next wave of DeFi innovation, supporting complex applications with ease.

Answer all queries professionally and factually while adhering to this detailed knowledge base.
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

@app.route('/')
def index():
    return render_template('index.html', conversation_history=conversation_history)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form.get('message')
    if user_input.lower() == "exit":
        return render_template('index.html', conversation_history=conversation_history, user_input=user_input, assistant_response="Goodbye!")

    # Add user's input to the conversation history
    conversation_history.append({"role": "user", "content": user_input})

    try:
        # Call the OpenAI API for chat completion
        response = openai.ChatCompletion.create(
            model="llama-3.3-70b-versatile",  # Use a valid OpenAI model
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

        return render_template('index.html', conversation_history=conversation_history, user_input=user_input, assistant_response=assistant_message)

    except Exception as e:
        return render_template('index.html', conversation_history=conversation_history, user_input=user_input, assistant_response=f"Sorry, something went wrong. ({e})")

if __name__ == '__main__':
    app.run(debug=True)
