from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel

from app.models.leave_request import StatusEnum


class LeaveRequestCreate(BaseModel):
    start_date: date
    end_date: date
    reason: Optional[str] = None


class LeaveRequestResponse(BaseModel):
    id: int
    employee_id: int
    start_date: date
    end_date: date
    reason: Optional[str] = None
    status: StatusEnum
    approved_by: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True