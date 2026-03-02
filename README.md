# 🪐 GlowGPT: Adaptive Local AI Studio

A fully configurable, hardware-aware ChatGPT clone, designed to run locally on your system using **FastAPI** and **Ollama**. No hidden defaults, no hardcoded models, and 100% transparent performance.

---

## 🛠️ How It Works Under The Hood

| Layer | Component | Function |
| :--- | :--- | :--- |
| **Frontend** | Browser (Vanilla JS) | Captures user input and streams back AI tokens in real-time using `fetch`. |
| **Backend** | FastAPI (Python) | Forwards prompts to the model server and manages the streaming bridge. |
| **Model Server** | Ollama | Loads the model file and performs the heavy-duty inference math. |
| **The Model** | LLM (e.g., Llama 3) | The trained intelligence (weights) stored in your RAM. |
| **Hardware** | Your RAM + CPU/GPU | The physical resources doing the work. |

---

## 🧠 Accurate Hardware Model Selection

The performance of local AI is NOT magic—it is limited by your system's physical resources.

### ✨ The RAM Guideline (Crucial!)

| System RAM | Safe Model Choice | Examples | Performance on CPU |
| :---: | :--- | :--- | :--- |
| **4GB** | < 1B Parameters | `tinyllama` | Fast (but limited intelligence) |
| **8GB** | 1B – 2B Parameters | `qwen2:1.5b`, `gemma:2b` | Smooth |
| **16GB** | 3B – 7B Parameters | `mistral:7b-q4_0`, `phi3:mini` | Medium |
| **32GB+** | 13B+ Parameters | `llama3:8b`, `mixtral:8x7b` | Slow (unless you have a Dedicated GPU) |

### 📊 Understanding "B" & RAM Math
*   **What is a "B"?**: 1B = 1 Billion Parameters. Each parameter is a "neuron connection".
*   **RAM Calculation**: 1B parameters usually take **~1GB of RAM** when quantized (Q4).
*   **Context usage**: Increasing the **Context Window** (e.g., from 2048 to 8192) forces your machine to reserve extra RAM for the "KV Cache" (the model's short-term memory).
*   **GPU vs. CPU**:
    *   **Dedicated GPU (NVIDIA)**: If you have one, Ollama will auto-accelerate. It is 10x–50x faster than a CPU.
    *   **Integrated Graphics**: Intel/AMD integrated chips are NOT real LLM accelerators. They still use your system RAM and will be slower.

> [!TIP]
> **Check your RAM on Windows:** Right-click **Taskbar** → **Task Manager** → **Performance** tab → **Memory**.

---

## ⚙️ Configuration — Make It Yours

Nothing in GlowGPT is hardcoded. Everything is configurable via an **`.env`** file.

1.  Create a file named `.env` in the project root (or copy `.env.example`).
2.  Set your desired variables:

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `MODEL_NAME` | `qwen:1.8b` | The model Ollama will load. Change to `gemma:2b`, `mistral:7b`, etc. |
| `APP_PORT` | `8000` | The port the FastAPI server listens on. |
| `APP_HOST` | `0.0.0.0` | Binding. `0.0.0.0` allows external access; `127.0.0.1` restricts to local only. |
| `CONTEXT_WINDOW`| `4096` | How many tokens the AI "remembers". **Larger = More RAM usage**. |
| `OLLAMA_HOST` | `http://localhost:11434` | The internal address of your Ollama server. |

---

## 📈 Performance Transparency

*   **First-Load Delay**: When you send the first message, Ollama must move 2GB–5GB from your SSD into your RAM. This causes a **10–30 second delay**.
*   **CPU at 100%**: It is **Normal** for your CPU to hit 100% during generation if you don't have a high-end GPU.
*   **System Freezing**: If your RAM is nearly full, your system may swap memory to your SSD. This causes the mouse to stutter and windows to freeze. If this happens, **use a smaller model**.
*   **Unlimited Memory?**: Impossible. The AI has a **Finite Context Window**. As the conversation exceeds that window (e.g., 4096 tokens), the AI must forget the oldest parts to make room for new ones. True memory requires a separate database (RAG).

---

## ⚠️ Safety & Security Disclaimer

> [!CAUTION]
> **Local by Design:** This project is intended for local use.
> **Public exposure:** If you use a tool like **ngrok**, your local model, RAM, and terminal are exposed to the internet. Anyone with the URL can consume your machine resources. 

---

## 🛠️ Step-by-Step Installation

1.  **Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Model Pull**:
    ```bash
    ollama pull [your_model_name]
    ```
3.  **Run**:
    ```bash
    uvicorn app:app --host 0.0.0.0 --port 8000
    ```

---

## ❌ Troubleshooting (Common Issues)

| Problem Code | Reality / Why It Happens | Solution Command / Fix |
| :--- | :--- | :--- |
| **Model 404 (Not Found)** | You didn't download the specific model variant. | `ollama pull [model_name]` |
| **Connection Refused** | Ollama API or service is not running. | Open Ollama app or run `ollama serve` |
| **API 405 (Not Allowed)** | Likely using a wrong API endpoint in `.env`. | Ensure `OLLAMA_HOST` matches `http://localhost:11434` |
| **Memory Allocation Failed**| Your RAM is too small for the selected model. | Switch `app.py` to a smaller model (1.8b or 1b). |
| **TLS Handshake Timeout**| Network connection failed during model download. | Toggle VPN / check network; try `ollama pull` again. |
| **ngrok 520 / 524** | The backend is too slow or generating took >60s. | Use a smaller model; close background Chrome tabs. |
| **Extreme Slowness** | High "Swap" usage. System using SSD as fake RAM. | Close all apps; drop `CONTEXT_WINDOW` to `2048`. |

---
*Built for educational transparency. No data leaves your machine unless you explicitly tunnel it.*
