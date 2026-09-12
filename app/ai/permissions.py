READ_ONLY_TOOLS = {
    "get_customer",
    "get_invoice",
    "get_payment_status",
    "get_subscription",
    "get_ticket",
}

WRITE_TOOLS = {
    "create_support_ticket",
}


def is_tool_allowed(
    tool_name: str,
    allow_write: bool = False,
) -> bool:
    if tool_name in READ_ONLY_TOOLS:
        return True

    if tool_name in WRITE_TOOLS:
        return allow_write

    return False