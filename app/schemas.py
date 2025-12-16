from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    """
    Request model for the chat endpoint.
    """
    message: str = Field(..., description="The user's input message to the bot.", min_length=1)

class ChatResponse(BaseModel):
    """
    Response model for the chat endpoint structure.
    """
    intent: str = Field(..., description="The detected intent of the user's message.")
    confidence: float = Field(..., description="Confidence score of the intent detection (0.0 to 1.0).")
    response: str = Field(..., description="The generated response text.")
