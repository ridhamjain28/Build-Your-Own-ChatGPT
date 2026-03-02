# 🚀 GlowGPT: Lightweight Local ChatGPT Clone

A "Batteries-Included" local AI chatbot designed for learners, developers, and low-RAM hardware. No API keys. No Cloud. Just your machine and an LLM.

---

## 🤖 Which Model Can You Run?

Running AI locally depends entirely on your system's **RAM (Memory)**. Here is a guide to selecting the right model for your machine:

| Your RAM Size | Recommended Model Pool | Example Name | Speed Expectation |
| :--- | :--- | :--- | :--- |
| **4GB** | 1B Models Only | `qwen:1.8b` / `tinyllama` | Fast (CPU-only) |
| **8GB** | 1B to 2B Models | `qwen:1.8b` / `gemma:2b` | Smooth |
| **16GB** | 3.5B to 7B Models | `phi3:mini` / `mistral:7b` | Medium (starts to sweat) |
| **32GB+** | 13B+ Models | `llama3:8b` / `nous-hermes` | Slow (requires Patience) |

### Key Hardware Concepts
*   **What is "B"?**: "B" stands for Billions of Parameters. A 7B model has 7 billion "neurons". The more parameters, the more intelligent (and memory-hungry) the model is.
*   **Why No GPU?**: This app is designed for **CPU-only** inference. If you have a Dedicated GPU (NVIDIA), Ollama will automatically use it for massive speed boosts. If not, your CPU will handle the heavy lifting.
*   **Quantization (Q4_0)**: Think of this as "compressing" the model. A 7B model normally takes 14GB+ RAM, but a "Q4" (4-bit quantized) version only needs ~4.5GB. We use Q4 models by default.
*   **Context Window**: The more you talk, the more RAM is used to "remember" the conversation. 

---

## 🛠️ Step-by-Step Setup (Windows)

1.  **Install Python**: Download from [python.org](https://www.python.org/). (Check "Add to PATH" during install).
2.  **Install Ollama**: Download from [ollama.com](https://ollama.com/).
3.  **Install Backend Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Pull Your Chosen Model**:
    ```bash
    # Open a terminal and run:
    ollama pull qwen:1.8b
    ```
5.  **Start the Services**:
    *   **Ollama**: Ensure the Ollama app is running in your taskbar.
    *   **FastAPI**: Run this command in your project folder:
        ```bash
        uvicorn app:app --host 0.0.0.0 --port 8000
        ```
6.  **Open Browser**: Go to `http://localhost:8000/`

---

## ⚙️ How to Change the Model

To switch from the default `qwen:1.8b` to something else (like `gemma:2b`):

1.  Open `app.py`.
2.  Change the top line: `MODEL_NAME = "gemma:2b"`
3.  **Crucial**: You MUST pull the new model first:
    ```bash
    ollama pull gemma:2b
    ```
4.  Restart the FastAPI server.

---

## ⚠️ Troubleshooting (Common Errors)

| Error Message / Issue | Reason | Exact Fix Command |
| :--- | :--- | :--- |
| **404 Model Not Found** | You haven't downloaded the model file. | `ollama pull model_name` |
| **500 / Connection Refused** | Ollama is not actually running. | Open Ollama app or run `ollama serve` |
| **"Memory allocation failed"** | Model is too big for your RAM. | Change `app.py` to a smaller model (1.8b) |
| **Extremely Slow Responses** | You are on a low-spec CPU. | Close Chrome/Background apps; use a 1B model. |
| **Browser doesn't load at all** | Host binding issue. | Verify you used `--host 0.0.0.0` |
| **ngrok 520 / 524 Cloudflare** | Backend is slow/offline. | Restart `uvicorn` and check local console for errors. |

---

## 🧠 Beginner Concepts Simply Explained

*   **LLM (Large Language Model)**: A complex math equation that predicts the "next word" in a sequence based on billions of examples.
*   **Ollama**: A tool that makes "running" those giant math equations as simple as opening an app.
*   **Localhost**: Your own computer's internal address. `localhost:8000` means "Talk to the app on my own machine at gate 8000."
*   **Streaming**: Instead of waiting for the full paragraph, we show you each word as the AI "thinks" it.
*   **Unlimited Memory?**: Impossible. Every word the AI remembers takes up a tiny bit of RAM. Eventually, your system runs out.

---

## ⚡ Performance Expectations

*   **The "First Load" Lag**: The first time you send a message, Ollama must move 1GB+ of data from your SSD to your RAM. This takes 10–20 seconds.
*   **CPU Spikes**: Your CPU will hit 100% while the AI is generating. This is normal behavior for local AI.
*   **8GB Freezes**: If you have 8GB RAM, your mouse might stutter briefly while the model loads. It will stop once it starts typing.

---

## 💾 Optional: Adding Long-Term Memory (Later)

Want the AI to remember things from 3 days ago? Here is how you would build it (Architecture):

1.  **Database**: Store every message in a local `SQLite` file.
2.  **Embeddings**: Convert text into numbers (Vectors) using Ollama's `/embeddings` endpoint.
3.  **Vector Search**: When a user asks a question, search the DB for the most "mathematically similar" past messages.
4.  **Prompt Injection**: Throw those past memories into the "System Prompt" before the AI answers.

---

*This repo is designed for educational MVPs. No data leaves your machine.*
