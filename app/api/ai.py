from fastapi import APIRouter
from pydantic import BaseModel

from app.ai.service import generate_response


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
def chat_with_ai(request: AIRequest):
    response = generate_response(request.prompt)

    return AIResponse(
        response=response,
    )