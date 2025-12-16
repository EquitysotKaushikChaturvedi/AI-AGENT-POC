import os
import google.generativeai as genai
from openai import OpenAI

def generate_ai_response(prompt: str) -> str:
    """
    Generates a response from the configured AI provider (Gemini or OpenAI).
    
    Args:
        prompt (str): The prompt to send to the AI.
        
    Returns:
        str: The plain text response from the AI.
    """
    provider = os.environ.get("AI_PROVIDER", "gemini").lower()
    
    try:
        if provider == "openai":
            return _generate_openai_response(prompt)
        else:
            return _generate_gemini_response(prompt)
    except Exception as e:
        print(f"Error generating AI response with provider '{provider}': {e}")
        return "I apologize, but I am currently unable to process your request. Please try again later."

def _generate_gemini_response(prompt: str) -> str:
    """Internal function to call Google Gemini API."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-flash-latest')
    response = model.generate_content(prompt)
    return response.text.strip()

def _generate_openai_response(prompt: str) -> str:
    """Internal function to call OpenAI chat API."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")
        
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()
