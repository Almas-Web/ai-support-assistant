from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.services.approval_service import (
    approve_action,
    get_approval,
    reject_action,
)

router = APIRouter(
    prefix="/approvals",
    tags=["Approvals"],
)


class ApprovalResponse(BaseModel):
    id: int
    tool_name: str
    arguments: dict
    status: str
    created_at: datetime


@router.get("/{approval_id}", response_model=ApprovalResponse)
def get_approval_api(
    approval_id: int,
    db: Session = Depends(get_db),
):
    approval = get_approval(
        db=db,
        approval_id=approval_id,
    )

    if approval is None:
        raise HTTPException(
            status_code=404,
            detail="Approval request not found.",
        )

    return approval


@router.post("/{approval_id}/approve")
def approve_approval(
    approval_id: int,
    db: Session = Depends(get_db),
):
    result = approve_action(
        db=db,
        approval_id=approval_id,
    )

    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["error"],
        )

    return result


@router.post("/{approval_id}/reject")
def reject_approval(
    approval_id: int,
    db: Session = Depends(get_db),
):
    result = reject_action(
        db=db,
        approval_id=approval_id,
    )

    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["error"],
        )

    return result