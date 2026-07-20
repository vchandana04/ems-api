from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.leave_request import LeaveRequest, StatusEnum
from app.models.employee import Employee
from app.models.user import User
from app.schemas.leave_request import LeaveRequestCreate, LeaveRequestResponse
from app.core.security import get_current_user

router = APIRouter(prefix="/leave-requests", tags=["Leave Requests"])


def _get_employee_profile(current_user: User, db: Session) -> Employee:
    """Helper: find the Employee record linked to the logged-in user."""
    employee = db.query(Employee).filter(Employee.user_id == current_user.id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee profile not found for this user")
    return employee


@router.post("/", response_model=LeaveRequestResponse, status_code=status.HTTP_201_CREATED)
def apply_leave(
    leave_data: LeaveRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    employee = _get_employee_profile(current_user, db)

    if leave_data.end_date < leave_data.start_date:
        raise HTTPException(status_code=400, detail="end_date cannot be before start_date")

    new_leave = LeaveRequest(
        employee_id=employee.id,
        start_date=leave_data.start_date,
        end_date=leave_data.end_date,
        reason=leave_data.reason,
        status=StatusEnum.pending,
    )
    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)
    return new_leave


@router.get("/my", response_model=List[LeaveRequestResponse])
def my_leave_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    employee = _get_employee_profile(current_user, db)
    return db.query(LeaveRequest).filter(LeaveRequest.employee_id == employee.id).all()


@router.get("/team", response_model=List[LeaveRequestResponse])
def team_leave_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.value not in ("manager", "admin"):
        raise HTTPException(status_code=403, detail="Only managers or admins can view team requests")

    manager_profile = _get_employee_profile(current_user, db)

    if current_user.role.value == "admin":
        return db.query(LeaveRequest).all()

    # Manager: only requests from employees who report to them
    team_ids = [e.id for e in db.query(Employee).filter(Employee.manager_id == manager_profile.id).all()]
    return db.query(LeaveRequest).filter(LeaveRequest.employee_id.in_(team_ids)).all()


def _decide_leave(leave_id: int, new_status: StatusEnum, db: Session, current_user: User) -> LeaveRequest:
    leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")

    if leave.status != StatusEnum.pending:  # type: ignore
        raise HTTPException(status_code=400, detail=f"Leave request already {leave.status.value}")

    manager_profile = _get_employee_profile(current_user, db)
    employee = db.query(Employee).filter(Employee.id == leave.employee_id).first()

    is_admin = current_user.role.value == "admin"
    is_direct_manager = employee is not None and employee.manager_id == manager_profile.id

    if not (is_admin or is_direct_manager): # type: ignore
        raise HTTPException(status_code=403, detail="Not permitted to decide on this leave request")

    leave.status = new_status  # type: ignore
    leave.approved_by = manager_profile.id  # type: ignore
    db.commit()
    db.refresh(leave)
    return leave


@router.put("/{leave_id}/approve", response_model=LeaveRequestResponse)
def approve_leave(leave_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return _decide_leave(leave_id, StatusEnum.approved, db, current_user)


@router.put("/{leave_id}/reject", response_model=LeaveRequestResponse)
def reject_leave(leave_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return _decide_leave(leave_id, StatusEnum.rejected, db, current_user)