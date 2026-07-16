"""Shared LLM — reuses existing Gemini API key."""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

GEMINI_API_KEY = "AIzaSyD4BMcy9_CepkclmgW_zG5CH1J7g61JsDg"

def call_gemini(prompt: str, fallback: str = "") -> str:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash")
        return model.generate_content(prompt).text
    except Exception as e:
        return fallback or f"[AI Error: {e}]"
