import os
import json
import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load configurations from .env file if it exists
load_dotenv()

# ==========================================
# ⚙️ CONFIGURATION (Environment Driven)
# ==========================================
# No hidden defaults. These can be overridden in your .env file.
MODEL_NAME = os.getenv("MODEL_NAME", "qwen:1.8b")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", 8000))

# Standard Ollama Generation Endpoint
OLLAMA_GENERATE_URL = f"{OLLAMA_HOST}/api/generate"

app = FastAPI(title="GlowGPT Local Studio")

# Enable CORS for internal networking and external tunnels (ngrok)
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
            raise HTTPException(status_code=400, detail="Payload missing 'message' field.")

        async def generate_stream():
            payload = {
                "model": MODEL_NAME,
                "prompt": message,
                "stream": True,
                # Options can be expanded here for context_length etc.
                "options": {
                    "num_ctx": int(os.getenv("CONTEXT_WINDOW", 4096))
                }
            }
            
            # Using a large timeout for local model loading/inference
            async with httpx.AsyncClient(timeout=None) as client:
                try:
                    async with client.stream("POST", OLLAMA_GENERATE_URL, json=payload) as response:
                        if response.status_code == 404:
                            yield f"⚠️ ERROR: Model '{MODEL_NAME}' not found. Please run 'ollama pull {MODEL_NAME}' in your terminal."
                            return
                        
                        if response.status_code != 200:
                            error_detail = await response.aread()
                            yield f"⚠️ ERROR: Ollama returned code {response.status_code}. Detail: {error_detail.decode()}"
                            return

                        async for line in response.aiter_lines():
                            if line:
                                try:
                                    chunk = json.loads(line)
                                    if "response" in chunk:
                                        yield chunk["response"]
                                    if chunk.get("done"):
                                        break
                                except json.JSONDecodeError:
                                    continue
                except httpx.ConnectError:
                    yield "⚠️ ERROR: Connection Refused. Is Ollama running? Try 'ollama serve'."
                except Exception as e:
                    yield f"⚠️ ERROR: {str(e)}"

        return StreamingResponse(generate_stream(), media_type="text/plain")

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")

# Mount the static frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    print(f"--- GlowGPT Local Studio ---")
    print(f"Target Model: {MODEL_NAME}")
    print(f"Host: {APP_HOST} | Port: {APP_PORT}")
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)
