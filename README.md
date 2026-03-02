# 🪐 GlowGPT: Adaptive Local AI Studio

<p align="center">
  <img src="https://img.shields.io/badge/Local--First-100%25-blue?style=for-the-badge" alt="Local First">
  <img src="https://img.shields.io/badge/Privacy-Protected-green?style=for-the-badge" alt="Privacy Protected">
  <img src="https://img.shields.io/badge/Hardware-Aware-orange?style=for-the-badge" alt="Hardware Aware">
</p>

A fully configurable, hardware-aware ChatGPT clone, designed to run locally on your system using **FastAPI** and **Ollama**. No hidden defaults, no hardcoded models, and 100% transparent performance.

---

## 📝 Creator's Choice: Why `qwen:1.8b`?

If you check the `.env` or `app.py`, you'll see I started with **`qwen:1.8b`**. Here is why:

*   **Low Footprint:** I built this on a machine with **8GB of RAM**. Larger models (7B+) would make my system crawl or crash if I have Chrome open.
*   **Speed:** On a standard CPU, 1.8B models generate tokens almost as fast as you can read.
*   **Smarts:** For its size, Qwen is surprisingly good at following instructions and coding tasks.
*   **Balance:** It is the "Goldilocks" model for testing—small enough for any modern laptop, but smart enough to feel like a real AI.

> [!TIP]
> **Use this as your baseline.** If it runs smoothly, try upgrading to `gemma:2b` or `mistral:7b`.

---

## 🛠️ How It Works Under The Hood

| Layer | Component | Function |
| :--- | :--- | :--- |
| **🌐 Frontend** | Browser (Vanilla JS) | Captures user input and streams back AI tokens in real-time. |
| **⚡ Backend** | FastAPI (Python) | The bridge that talks to Ollama and pipes data to your screen. |
| **📦 Model Server** | Ollama | The "Engine" that loads the model into your RAM. |
| **🧠 The Model** | LLM (e.g., Llama 3) | The actual intelligence doing the thinking. |
| **💻 Hardware** | Your RAM + CPU/GPU | The physical power source. |

---

## 🧠 Accurate Hardware Model Selection

The performance of local AI is NOT magic—it is limited by your system's physical resources.

### ✨ The RAM Guideline (Crucial!)

*   🔴 **4GB RAM**: Only `< 1B` Parameters (`tinyllama`).
*   🟡 **8GB RAM**: `1B – 2B` Parameters (`qwen2:1.5b`, `gemma:2b`). **(Recommended Start)**
*   🟢 **16GB RAM**: `3B – 7B` Parameters (`mistral:7b-q4_0`, `phi3:mini`).
*   🔵 **32GB+ RAM**: `13B+` Models (`llama3:8b`, `mixtral:8x7b`).

### 📊 Understanding "B" & RAM Math
*   **What is a "B"?**: 1B = 1 Billion Parameters. Think of them as "brain cells".
*   **RAM Calculation**: 1B parameters usually take **~1GB of RAM** when quantized (Q4).
*   **GPU vs. CPU**:
    *   🚀 **NVIDIA GPU**: Ollama auto-accelerates. 10x–50x faster.
    *   🐌 **Integrated Graphics**: Intel/AMD chips use system RAM and will be slower.

---

## ⚙️ Configuration — Make It Yours

Nothing in GlowGPT is hardcoded. Everything is configurable via an **`.env`** file.

1.  Create a file named `.env` in the project root.
2.  **Customize your setup:**

| Variable | Default | 🔥 Pro Tip |
| :--- | :--- | :--- |
| `MODEL_NAME` | `qwen:1.8b` | Change to `mistral:7b` for higher intelligence. |
| `APP_PORT` | `8000` | Use `3000` or `5000` if 8000 is busy. |
| `CONTEXT_WINDOW`| `4096` | Lower to `2048` if you run out of RAM mid-chat. |

---

## 📈 Performance Transparency

*   **🐢 First-Load Delay**: Ollama takes 10–30s to "warm up" the model from SSD to RAM.
*   **🔥 CPU at 100%**: Normal! Your CPU is doing billions of math operations per second.
*   **❄️ System Freezing**: Means you are out of RAM. **Switch to a smaller model immediately.**
*   **🗑️ Memory Limits**: The AI is finite. It will "forget" the beginning of long chats.

---

## ⚠️ Safety & Security Disclaimer

> [!CAUTION]
> **LOCAL ONLY:** This project is private by default.
> **TUNNELING:** If you use **ngrok**, anyone with the link can use your RAM and CPU. Never share your ngrok URL publicly unless you want the internet using your computer!

---

## 🛠️ Step-by-Step Installation

1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Get the model**:
    ```bash
    ollama pull qwen:1.8b
    ```
3.  **Launch**:
    ```bash
    uvicorn app:app --host 0.0.0.0 --port 8000
    ```

---

## ❌ Troubleshooting (Common Issues)

| Problem | Reality Check | The Fix |
| :--- | :--- | :--- |
| **Model 404** | You didn't download the model. | `ollama pull [model_name]` |
| **Connection Refused**| Ollama isn't running. | Run `ollama serve` |
| **Memory Error**| Model is too big for your RAM. | Upgrade RAM or Downgrade Model. |
| **Extreme Lag** | High "Swap" usage (SSD noise). | Close Chrome; reboot; use 1B model. |

---
*✨ Built for educational transparency. No data leaves your machine. ✨*
