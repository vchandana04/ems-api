from fastapi import FastAPI
from app.db.database import Base, engine
from app.models import user, department, employee, leave_request
from app.routers import auth
from app.routers import auth, employees
from app.routers import auth, employees, departments
from app.routers import auth, employees, departments, leave_requests

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(employees.router)
app.include_router(departments.router)
app.include_router(leave_requests.router)

@app.get("/")
def read_root():
    return {"message": "Employee Management System API is running"}