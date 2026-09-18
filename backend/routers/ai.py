import time
from fastapi import APIRouter, HTTPException, status
from backend.models import AIChatRequest
from backend.database import db
from backend.ai_service import ask_mistral_ai

router = APIRouter(prefix="/api/ai", tags=["ai"])

@router.post("/chat")
async def chat_with_ai(req: AIChatRequest):
    if not req.message or not req.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message is required."
        )

    conv_id = req.conversation_id or int(time.time()) % 1000000
    user_id = req.user_id or 1

    # Record user message
    db.add_chat_message(
        conversation_id=conv_id,
        user_id=user_id,
        sender="user",
        content=req.message.strip()
    )

    # Call Mistral AI
    ai_reply = await ask_mistral_ai(req.message.strip())

    # Record assistant message
    db.add_chat_message(
        conversation_id=conv_id,
        user_id=user_id,
        sender="assistant",
        content=ai_reply
    )

    return {
        "response": ai_reply,
        "conversation_id": conv_id,
    }
