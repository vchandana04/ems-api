from datetime import date
from pydantic import BaseModel
from typing import Optional


class EmployeeCreate(BaseModel):
    """What the client sends to create a new employee."""
    user_id: int
    full_name: str
    designation: Optional[str] = None
    department_id: Optional[int] = None
    manager_id: Optional[int] = None
    date_joined: Optional[date] = None


class EmployeeResponse(BaseModel):
    """What we send back after creating/fetching an employee."""
    id: int
    user_id: int
    full_name: str
    designation: Optional[str] = None
    department_id: Optional[int] = None
    manager_id: Optional[int] = None
    date_joined: Optional[date] = None

    class Config:
        from_attributes = True

class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    designation: Optional[str] = None
    department_id: Optional[int] = None
    manager_id: Optional[int] = None
    date_joined: Optional[date] = None