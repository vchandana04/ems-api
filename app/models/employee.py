from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    full_name = Column(String(150), nullable=False)
    designation = Column(String(100))
    department_id = Column(Integer, ForeignKey("departments.id"), index=True)
    manager_id = Column(Integer, ForeignKey("employees.id"), nullable=True, index=True)
    date_joined = Column(Date)

    # Relationships let us access related objects easily in Python
    department = relationship("Department")
    manager = relationship("Employee", remote_side=[id])