from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.employee import Employee
from app.models.user import User
from app.models.department import Department
from app.schemas.employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from app.core.security import require_role, get_current_user

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    user = db.query(User).filter(User.id == employee_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Linked user account not found")

    existing = db.query(Employee).filter(Employee.user_id == employee_data.user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Employee profile already exists for this user")

    if employee_data.department_id:
        department = db.query(Department).filter(Department.id == employee_data.department_id).first()
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")

    if employee_data.manager_id:
        manager = db.query(Employee).filter(Employee.id == employee_data.manager_id).first()
        if not manager:
            raise HTTPException(status_code=404, detail="Manager (employee) not found")

    new_employee = Employee(**employee_data.model_dump())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


@router.get("/", response_model=List[EmployeeResponse])
def list_employees(
    department_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Employee)

    # Role-based visibility
    if current_user.role.value == "admin":
        pass  # sees everyone
    elif current_user.role.value == "manager":
        # find this manager's own employee record first
        manager_profile = db.query(Employee).filter(Employee.user_id == current_user.id).first()
        if not manager_profile:
            raise HTTPException(status_code=404, detail="Manager profile not found")
        query = query.filter(Employee.manager_id == manager_profile.id)
    else:
        # plain employee: only their own record
        query = query.filter(Employee.user_id == current_user.id)

    if department_id:
        query = query.filter(Employee.department_id == department_id)

    return query.all()


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Access control: admin sees all; others only their own record
    if current_user.role.value != "admin" and employee.user_id != current_user.id: # type: ignore
        raise HTTPException(status_code=403, detail="Not permitted to view this employee")

    return employee


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    if current_user.role.value != "admin" and employee.user_id != current_user.id: # type: ignore
        raise HTTPException(status_code=403, detail="Not permitted to update this employee")

    update_data = employee_data.model_dump(exclude_unset=True)

    if "department_id" in update_data and update_data["department_id"]:
        department = db.query(Department).filter(Department.id == update_data["department_id"]).first()
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")

    if "manager_id" in update_data and update_data["manager_id"]:
        manager = db.query(Employee).filter(Employee.id == update_data["manager_id"]).first()
        if not manager:
            raise HTTPException(status_code=404, detail="Manager (employee) not found")

    for field, value in update_data.items():
        setattr(employee, field, value)

    db.commit()
    db.refresh(employee)
    return employee


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(employee)
    db.commit()
    return None