"""
Shared Gemini client used by all agents.
Uses google-generativeai (free tier: 15 req/min, 1M tokens/day).
"""
import os
import google.generativeai as genai

def get_model():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not set. "
            "Get a free key at https://aistudio.google.com/app/apikey"
        )
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")

def call_gemini(system_prompt: str, user_message: str) -> str:
    model = get_model()
    full_prompt = f"{system_prompt}\n\n---\n\n{user_message}"
    response = model.generate_content(full_prompt)
    return response.text.strip()
