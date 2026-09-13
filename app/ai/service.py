import json
from sqlalchemy.orm import Session
from app.ai.client import client
from app.ai.permissions import is_tool_allowed, requires_human_approval
from app.ai.tools import (
    create_support_ticket,
    get_customer,
    get_invoice,
    get_payment_status,
    get_subscription,
    get_ticket,
)
from app.ai.tools_schema import (
    CREATE_TICKET_TOOL,
    CUSTOMER_TOOL,
    INVOICE_TOOL,
    PAYMENT_STATUS_TOOL,
    SUBSCRIPTION_TOOL,
    TICKET_TOOL,
)
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
                        INVOICE_TOOL,
                        PAYMENT_STATUS_TOOL,
                        SUBSCRIPTION_TOOL,
                        TICKET_TOOL,
                        CREATE_TICKET_TOOL,
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
        tool_name = function_call.name

        if requires_human_approval(tool_name):
            tool_results.append(
                {
                    "name": tool_name,
                    "result": {
                        "success": False,
                        "requires_approval": True,
                        "message": "Human approval is required before this action can be executed.",
                    },
                }
            )
            continue

        if not is_tool_allowed(
            tool_name=tool_name,
            allow_write=False,
        ):
            tool_results.append(
                {
                    "name": tool_name,
                    "result": {
                        "success": False,
                        "error": "This tool is not allowed.",
                    },
                }
            )
            continue

        arguments = function_call.args

        if tool_name == "get_customer":
            result = get_customer(
                db=db,
                customer_id=int(arguments["customer_id"]),
            )

        elif tool_name == "get_invoice":
            result = get_invoice(
                db=db,
                invoice_id=int(arguments["invoice_id"]),
            )

        elif tool_name == "get_payment_status":
            result = get_payment_status(
                db=db,
                payment_id=int(arguments["payment_id"]),
            )

        elif tool_name == "get_subscription":
            result = get_subscription(
                db=db,
                subscription_id=int(arguments["subscription_id"]),
            )

        elif tool_name == "get_ticket":
            result = get_ticket(
                db=db,
                ticket_id=int(arguments["ticket_id"]),
            )

        elif tool_name == "create_support_ticket":
            result = create_support_ticket(
                db=db,
                customer_id=int(arguments["customer_id"]),
                subject=str(arguments["subject"]),
                description=str(arguments["description"]),
                priority=str(arguments["priority"]),
            )

        else:
            result = {
                "success": False,
                "error": "Unknown tool.",
            }

        tool_results.append(
            {
                "name": tool_name,
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

The application processed the following tool request:
{tool_response}

Use the result to answer the user's request accurately.
Do not mention internal tools or function calling.

If the customer was not found, clearly tell the user that the customer was not found.
If the invoice was not found, clearly tell the user that the invoice was not found.
If the payment was not found, clearly tell the user that the payment was not found.
If the subscription was not found, clearly tell the user that the subscription was not found.
If the support ticket was not found, clearly tell the user that the support ticket was not found.

If requires_approval is true, clearly tell the user that human approval is required before creating the support ticket.
Do not claim that the ticket was created when approval is required.

If a new support ticket was created, clearly provide the ticket ID, subject, status, and priority.
"""

    final_response = client.models.generate_content(
        model=settings.gemini_model,
        contents=final_prompt,
    )

    return final_response.text