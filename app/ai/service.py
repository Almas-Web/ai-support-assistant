import json
from sqlalchemy.orm import Session
from app.ai.client import client
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
        arguments = function_call.args

        if function_call.name == "get_customer":
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

        elif function_call.name == "get_invoice":
            result = get_invoice(
                db=db,
                invoice_id=int(arguments["invoice_id"]),
            )
            tool_results.append(
                {
                    "name": function_call.name,
                    "result": result,
                }
            )

        elif function_call.name == "get_payment_status":
            result = get_payment_status(
                db=db,
                payment_id=int(arguments["payment_id"]),
            )
            tool_results.append(
                {
                    "name": function_call.name,
                    "result": result,
                }
            )

        elif function_call.name == "get_subscription":
            result = get_subscription(
                db=db,
                subscription_id=int(arguments["subscription_id"]),
            )
            tool_results.append(
                {
                    "name": function_call.name,
                    "result": result,
                }
            )

        elif function_call.name == "get_ticket":
            result = get_ticket(
                db=db,
                ticket_id=int(arguments["ticket_id"]),
            )
            tool_results.append(
                {
                    "name": function_call.name,
                    "result": result,
                }
            )

        elif function_call.name == "create_support_ticket":
            result = create_support_ticket(
                db=db,
                customer_id=int(arguments["customer_id"]),
                subject=str(arguments["subject"]),
                description=str(arguments["description"]),
                priority=str(arguments["priority"]),
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
If the invoice was not found, clearly tell the user that the invoice was not found.
If the payment was not found, clearly tell the user that the payment was not found.
If the subscription was not found, clearly tell the user that the subscription was not found.
If the support ticket was not found, clearly tell the user that the support ticket was not found.
If a new support ticket was created, clearly provide the ticket ID, subject, status, and priority.
"""

    final_response = client.models.generate_content(
        model=settings.gemini_model,
        contents=final_prompt,
    )

    return final_response.text