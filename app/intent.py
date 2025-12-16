import os
from typing import Tuple
from app.llm_provider import generate_ai_response

def detect_intent(message: str) -> Tuple[str, float]:
    """
    Detects the intent of the user's message using the configured AI provider.
    
    Supported Intents:
      - business_growth
      - service_info
      - support
      - company_info
      - unknown
      
    Args:
        message (str): The user's input message.
        
    Returns:
        Tuple[str, float]: A dictionary containing 'intent' (str) and 'confidence' (float).
    """

    # Direct Keyword Detection for Greetings (High Priority)
    greeting_keywords = ["hi", "hello", "hey", "good morning", "good evening", "help", "can you help me"]
    if message.strip().lower() in greeting_keywords:
        return "greeting", 0.90

    try:
        prompt = f"""
        Identify the specific intent of the user's message from the following list:
        1. leadership_info (questions specific to founders, directors, CEO, leadership team, or who runs the company)
        2. services_info (questions specific to services, offerings, products, or what the company does)
        3. company_overview (general questions about the company history, founding year, culture, or mission)
        4. business_growth (questions about expansion, future plans, or scaling)
        5. support (questions about contact, help, technical issues, or support channels)
        6. greeting (simple salutations like hi, hello, help)
        7. unknown (if the message is unrelated to the business or gibberish)

        Return ONLY the intent name.
        Example: services_info

        User Message: "{message}"
        """

        intent_text = generate_ai_response(prompt).strip().lower()
        
        # Clean up potential extra chars (like "intent: services_info")
        if ":" in intent_text:
            intent_text = intent_text.split(":")[-1].strip()
        
        # Define allowed intents
        allowed_intents = {
            "business_growth", "services_info", "support", 
            "company_overview", "leadership_info", "greeting", "unknown"
        }
        
        # Fallback validation
        intent = intent_text if intent_text in allowed_intents else "unknown"

        # Heuristic Confidence Calculation
        # We assume the LLM is generally correct, but we boost confidence if keywords match
        keywords = {
            "leadership_info": ["founder", "ceo", "director", "owner", "partner", "lead", "who runs"],
            "services_info": ["service", "offer", "product", "provide", "do you do", "solution"],
            "business_growth": ["scale", "grow", "future", "expand", "plan"],
            "support": ["contact", "issue", "bug", "support", "email", "phone"],
            "company_overview": ["history", "founded", "about", "profile", "mission", "vision"],
            "greeting": ["hi", "hello", "hey", "help", "morning", "evening"]
        }

        # Base confidence
        confidence = 0.70 
        
        if intent in keywords:
            # Check for strong specific keyword matches
            if any(k in message.lower() for k in keywords[intent]):
                confidence = 0.95
            else:
                # Contextual match likely
                confidence = 0.80
        elif intent == "unknown":
             confidence = 0.50

        return intent, confidence

    except Exception as e:
        print(f"Error in intent detection: {e}")
        # Fail gracefully
        return "unknown", 0.0
