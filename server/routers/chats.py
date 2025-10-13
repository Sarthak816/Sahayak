from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load API key from .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY missing in .env file!")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

router = APIRouter(prefix="/api/chat", tags=["Chatbot"])

class ChatInput(BaseModel):
    message: str

def ask_gemini(prompt: str, model: str = "gemini-1.5-flash"):
    
    try:
        model_obj = genai.GenerativeModel(model)
        response = model_obj.generate_content(prompt)
        return getattr(response, "text", str(response))
    except Exception as e:
        return f"Error contacting Gemini API: {e}"

@router.post("/")
async def chatbot_response(input: ChatInput):
    user_message = input.message.strip()

    system_prompt = (
        "You are SAHAY, a helpful assistant for POWERGRID employees. "
        "Answer in a polite, clear, and concise way. "
        "Do not use technical jargon unless necessary."
    )

    prompt = f"{system_prompt}\n\nEmployee: {user_message}\nSahay:"
    reply = ask_gemini(prompt)

    return {"reply": reply}

