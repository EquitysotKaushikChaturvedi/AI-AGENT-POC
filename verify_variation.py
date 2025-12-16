import sys
import os

# Add current directory to path so we can import app modules
sys.path.append(os.getcwd())

from app.responses import generate_response

def test_variation():
    responses = set()
    num_tests = 10
    
    print(f"Generating {num_tests} greeting responses...")
    
    for i in range(num_tests):
        resp = generate_response("greeting", {}, "hello")
        print(f"  {i+1}: {resp}")
        responses.add(resp)
        
    print("-" * 20)
    print(f"Unique responses generated: {len(responses)}")
    
    if len(responses) > 1:
        print("PASS: Responses are varying.")
        return True
    else:
        print("FAIL: Responses are identical.")
        return False

if __name__ == "__main__":
    if test_variation():
        print("VERIFICATION SUCCEEDED")
    else:
        print("VERIFICATION FAILED")
