from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.ai.service import generate_response
from app.db.dependencies import get_db

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)
class AIRequest(BaseModel):
    prompt: str
class AIResponse(BaseModel):
    response: str
@router.post(
    "/chat",
    response_model=AIResponse,
)
def chat_with_ai(
    request: AIRequest,
    db: Session = Depends(get_db),
):
    response = generate_response(
        prompt=request.prompt,
        db=db,
    )

    return AIResponse(
        response=response,
    )