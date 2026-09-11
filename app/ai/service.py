from app.ai.client import client
from app.core.config import settings


def generate_response(prompt: str) -> str:
    interaction = client.interactions.create(
        model=settings.gemini_model,
        input=prompt,
    )

    return interaction.output_text