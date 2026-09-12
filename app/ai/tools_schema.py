CUSTOMER_TOOL = {
    "name": "get_customer",
    "description": "Get customer information by customer ID.",
    "parameters": {
        "type": "object",
        "properties": {
            "customer_id": {
                "type": "integer",
                "description": "The unique ID of the customer.",
            }
        },
        "required": ["customer_id"],
    },
}
INVOICE_TOOL = {
    "name": "get_invoice",
    "description": "Get invoice information by invoice ID.",
    "parameters": {
        "type": "object",
        "properties": {
            "invoice_id": {
                "type": "integer",
                "description": "The unique ID of the invoice.",
            }
        },
        "required": ["invoice_id"],
    },
}
PAYMENT_STATUS_TOOL = {
    "name": "get_payment_status",
    "description": "Get payment status and payment details by payment ID.",
    "parameters": {
        "type": "object",
        "properties": {
            "payment_id": {
                "type": "integer",
                "description": "The unique ID of the payment.",
            }
        },
        "required": ["payment_id"],
    },
}

SUBSCRIPTION_TOOL = {
    "name": "get_subscription",
    "description": "Get subscription information by subscription ID.",
    "parameters": {
        "type": "object",
        "properties": {
            "subscription_id": {
                "type": "integer",
                "description": "The unique ID of the subscription.",
            }
        },
        "required": ["subscription_id"],
    },
}

TICKET_TOOL = {
    "name": "get_ticket",
    "description": "Get support ticket information by ticket ID.",
    "parameters": {
        "type": "object",
        "properties": {
            "ticket_id": {
                "type": "integer",
                "description": "The unique ID of the support ticket.",
            }
        },
        "required": ["ticket_id"],
    },
}

CREATE_TICKET_TOOL = {
    "name": "create_support_ticket",
    "description": "Create a new support ticket for a customer.",
    "parameters": {
        "type": "object",
        "properties": {
            "customer_id": {
                "type": "integer",
                "description": "The unique ID of the customer.",
            },
            "subject": {
                "type": "string",
                "description": "The subject of the support ticket.",
            },
            "description": {
                "type": "string",
                "description": "A detailed description of the customer's issue.",
            },
            "priority": {
                "type": "string",
                "description": "Ticket priority: low, medium, or high.",
            },
        },
        "required": [
            "customer_id",
            "subject",
            "description",
            "priority",
        ],
    },
}