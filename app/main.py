from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from fastapi import FastAPI, HTTPException
from app.schemas import ChatRequest, ChatResponse
from app.agent import agent_instance

app = FastAPI(
    title="AI Agent POC",
    description="A Botpress-style AI Agent API POC.",
    version="1.0.0"
)

@app.get("/")
async def root():
    """
    Root endpoint to verify the API is running.
    """
    return {
        "message": "AI Agent API is running.",
        "usage": "Send a POST request to /chat with {'message': '...'}"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    POST /chat
    
    Receives a user message and returns the AI agent's structured response.
    """
    try:
        response = agent_instance.process_request(request)
        return response
    except Exception as e:
        # Log the error (print for POC)
        print(f"Internal Server Error: {e}")
        # In a real app, we wouldn't expose the exception details so rawly
        raise HTTPException(status_code=500, detail="Internal Server Error processing request")

if __name__ == "__main__":
    import uvicorn
    # Allow running directly for debug purposes
    uvicorn.run(app, host="0.0.0.0", port=8000)
