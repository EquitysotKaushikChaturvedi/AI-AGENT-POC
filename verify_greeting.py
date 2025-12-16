import sys
import os

# Add current directory to path so we can import app modules
sys.path.append(os.getcwd())

from app.intent import detect_intent
from app.responses import generate_response

def test_greeting():
    messages = ["hello", "hi", "help", "can you help me"]
    
    for msg in messages:
        print(f"Testing message: '{msg}'")
        intent, confidence = detect_intent(msg)
        print(f"  Detected Intent: {intent}, Confidence: {confidence}")
        
        response = generate_response(intent, {}, msg)
        print(f"  Response: {response}")
        print("-" * 20)
        
        if intent != "greeting":
            print(f"FAILED: Expected 'greeting' intent for '{msg}'")
            return False
            
    return True

if __name__ == "__main__":
    if test_greeting():
        print("ALL TESTS PASSED")
    else:
        print("TESTS FAILED")
