# Employee Management System (EMS) API

A backend REST API for managing employees, departments, and leave requests, built with role-based access control (Admin, Manager, Employee).

## Features

- JWT-based authentication (register, login)
- Role-Based Access Control (Admin / Manager / Employee)
- Employee CRUD with role-based visibility
- Department management
- Leave request workflow: apply → manager approval/rejection
- Self-referencing employee hierarchy (manager-employee relationships)

## Tech Stack

- **Language**: Python 3.13
- **Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0
- **Database**: MySQL / MariaDB
- **Authentication**: JWT (python-jose), bcrypt password hashing (passlib)
- **Validation**: Pydantic

## Project Structure