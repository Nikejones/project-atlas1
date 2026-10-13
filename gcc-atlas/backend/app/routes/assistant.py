"""
AI GCC Research Assistant routes
"""

from fastapi import APIRouter, HTTPException
from app.models import AssistantChatRequest, AssistantChatResponse
from app.services.llm_service import ask_assistant

router = APIRouter(prefix="/assistant", tags=["AI Assistant"])


@router.post("/chat", response_model=AssistantChatResponse)
async def chat_with_assistant(request: AssistantChatRequest):
    """
    Query the AI GCC Research Assistant.
    Retrieves database records and synthesizes a grounded answer with citations.
    """
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Query message cannot be empty.")

    try:
        response = await ask_assistant(request.message.strip(), request.history)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Research assistant error: {str(e)}")
