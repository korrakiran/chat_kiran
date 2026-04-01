from fastapi import APIRouter, HTTPException, Request, Body
from fastapi.responses import StreamingResponse
from typing import List, Dict
from ..services.sarvam import SarvamService

router = APIRouter()
sarvam_service = SarvamService()

@router.post("/{id}/message")
async def create_message(id: str, payload: Dict[str, str] = Body(...)):
    # Pure stateless chat: No DB, no memory logic
    user_prompt = payload.get("content", "")
    if not user_prompt:
        raise HTTPException(status_code=400, detail="Missing content")
    
    # Simple history (just current message for now, or what frontend sends)
    messages = [{"role": "user", "content": user_prompt}]

    async def stream_response():
        try:
            async for chunk in sarvam_service.generate_response(messages):
                yield chunk
        except Exception as e:
            yield f"data: Error during generation: {str(e)}\n\n"

    return StreamingResponse(stream_response(), media_type="text/event-stream")
