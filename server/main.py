from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Initialize model - TRY EACH ONE UNTIL IT WORKS
model = genai.GenerativeModel('gemini-2.5-flash')  # Try this first

print(f"✓ Using model: gemini-2.5-flash")

# Models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get("/")
async def root():
    return {"message": "Gemini Chatbot API is running", "status": "ok"}

@app.post("/api/v1/chatbot", response_model=ChatResponse)
async def chatbot(request: ChatRequest):
    try:
        print(f"Received message: {request.message}")
        
        response = model.generate_content(request.message)
        bot_response = response.text
        
        print(f"Bot response: {bot_response}")
        return ChatResponse(response=bot_response)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)