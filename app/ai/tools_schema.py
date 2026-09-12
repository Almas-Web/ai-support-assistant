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