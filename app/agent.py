from app.schemas import ChatRequest, ChatResponse
from app.intent import detect_intent
from app.context import load_business_profile
from app.responses import generate_response

class AIAgent:
    """
    The central orchestration class for the AI Agent.
    """
    
    def __init__(self):
        # In a production app, we load once. 
        # For this POC, we reload per request to allow file editing.
        pass

    def process_request(self, request: ChatRequest) -> ChatResponse:
        """
        Process the incoming chat request through the agent pipeline.
        
        Pipeline:
        1. Intent Detection
        2. Context Retrieval (Reloaded per request)
        3. Response Generation
        """
        # Step 0: Load Context Dynamically
        context = load_business_profile()
        
        # Step 1: Detect Intent
        intent, confidence = detect_intent(request.message)
        
        # Step 2: Generate Response using Context and Intent
        response_text = generate_response(intent, context, request.message)
        
        # Step 3: Return Structured Output
        return ChatResponse(
            intent=intent,
            confidence=confidence,
            response=response_text
        )

# Singleton instance can be created here or in main
agent_instance = AIAgent()
