import json

from sqlalchemy.orm import Session

from app.ai.client import client
from app.ai.tools import get_customer
from app.ai.tools_schema import CUSTOMER_TOOL
from app.core.config import settings


def generate_response(
    prompt: str,
    db: Session,
) -> str:
    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config={
            "tools": [
                {
                    "function_declarations": [
                        CUSTOMER_TOOL,
                    ],
                }
            ],
        },
    )

    function_calls = response.function_calls

    if not function_calls:
        return response.text

    tool_results = []

    for function_call in function_calls:
        if function_call.name == "get_customer":
            arguments = function_call.args

            result = get_customer(
                db=db,
                customer_id=int(arguments["customer_id"]),
            )

            tool_results.append(
                {
                    "name": function_call.name,
                    "result": result,
                }
            )

    if not tool_results:
        return response.text

    tool_response = json.dumps(tool_results)

    final_prompt = f"""
You are a customer support assistant.

User request:
{prompt}

The application executed the following tool:
{tool_response}

Use the tool result to answer the user's request accurately.
Do not mention internal tools or function calling.
If the customer was not found, clearly tell the user that the customer was not found.
"""

    final_response = client.models.generate_content(
        model=settings.gemini_model,
        contents=final_prompt,
    )

    return final_response.text