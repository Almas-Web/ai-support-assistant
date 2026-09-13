from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.approval import Approval
from app.services.ticket_service import create_ticket


def create_approval(
    db: Session,
    tool_name: str,
    arguments: dict,
) -> Approval:
    approval = Approval(
        tool_name=tool_name,
        arguments=arguments,
        status="pending",
    )
    db.add(approval)
    db.commit()
    db.refresh(approval)
    return approval


def get_approval(
    db: Session,
    approval_id: int,
) -> Approval | None:
    statement = select(Approval).where(
        Approval.id == approval_id
    )
    return db.scalar(statement)


def approve_action(
    db: Session,
    approval_id: int,
) -> dict:
    approval = get_approval(
        db=db,
        approval_id=approval_id,
    )

    if approval is None:
        return {
            "success": False,
            "error": "Approval request not found.",
        }

    if approval.status != "pending":
        return {
            "success": False,
            "error": f"Approval is already {approval.status}.",
        }

    if approval.tool_name == "create_support_ticket":
        arguments = approval.arguments

        ticket = create_ticket(
            db=db,
            customer_id=int(arguments["customer_id"]),
            subject=str(arguments["subject"]),
            description=str(arguments["description"]),
            priority=str(arguments["priority"]),
        )

        approval.status = "approved"
        db.commit()
        db.refresh(approval)

        return {
            "success": True,
            "approval_id": approval.id,
            "status": approval.status,
            "ticket": {
                "id": ticket.id,
                "customer_id": ticket.customer_id,
                "subject": ticket.subject,
                "description": ticket.description,
                "status": ticket.status,
                "priority": ticket.priority,
                "created_at": ticket.created_at.isoformat(),
            },
        }

    approval.status = "approved"
    db.commit()

    return {
        "success": True,
        "approval_id": approval.id,
        "status": approval.status,
    }


def reject_action(
    db: Session,
    approval_id: int,
) -> dict:
    approval = get_approval(
        db=db,
        approval_id=approval_id,
    )

    if approval is None:
        return {
            "success": False,
            "error": "Approval request not found.",
        }

    if approval.status != "pending":
        return {
            "success": False,
            "error": f"Approval is already {approval.status}.",
        }

    approval.status = "rejected"
    db.commit()
    db.refresh(approval)

    return {
        "success": True,
        "approval_id": approval.id,
        "status": approval.status,
    }