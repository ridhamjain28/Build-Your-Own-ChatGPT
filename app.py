from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import httpx
import json
import asyncio

# ==========================================
# CONFIGURATION & HARDWARE LIMITS
# ==========================================
# 1B - 2B models: Great for 4GB - 8GB RAM (Fast)
# 7B models: Requires 16GB RAM (Medium speed on CPU)
# 13B+ models: Requires 32GB+ RAM (Slow on CPU)
MODEL_NAME = "qwen:1.8b" 
OLLAMA_URL = "http://localhost:11434/api/generate"

app = FastAPI()

# Enable CORS for local development and tunneling (like ngrok)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        message = data.get("message")
        
        if not message:
            raise HTTPException(status_code=400, detail="Missing 'message' in request body. Please send some text!")

        async def generate_stream():
            payload = {
                "model": MODEL_NAME,
                "prompt": message,
                "stream": True
            }
            
            # timeout=None is critical for local LLMs as they can take time to think
            async with httpx.AsyncClient(timeout=None) as client:
                try:
                    async with client.stream("POST", OLLAMA_URL, json=payload) as response:
                        if response.status_code == 404:
                            yield f"Error: Model '{MODEL_NAME}' not found. Run 'ollama pull {MODEL_NAME}' in your terminal."
                            return
                        
                        if response.status_code != 200:
                            yield f"Error: Ollama returned status {response.status_code}. Check your Ollama logs."
                            return

                        async for line in response.aiter_lines():
                            if line:
                                try:
                                    chunk = json.loads(line)
                                    # We yield the text content immediately to the browser
                                    if "response" in chunk:
                                        yield chunk["response"]
                                    if chunk.get("done"):
                                        break
                                except json.JSONDecodeError:
                                    continue
                except httpx.ConnectError:
                    yield "Error: Cannot connect to Ollama. Ensure 'ollama serve' is running in the background."

        return StreamingResponse(generate_stream(), media_type="text/plain")

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format.")
    except Exception as e:
        # Generic error fallback for better debugging
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Serve the frontend (index.html) from the 'static' folder
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    # 0.0.0.0 allows external devices on your network (or ngrok) to connect
    print(f"Starting server... Model: {MODEL_NAME}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
