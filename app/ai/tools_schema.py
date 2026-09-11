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