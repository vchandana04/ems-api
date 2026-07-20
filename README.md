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

app/
├── main.py # App entry point
├── core/
│ ├── config.py # Environment variable loading
│ └── security.py # Password hashing, JWT, RBAC dependencies
├── db/
│ └── database.py # SQLAlchemy engine/session setup
├── models/ # SQLAlchemy ORM models (DB tables)
├── schemas/ # Pydantic request/response schemas
└── routers/ # API route handlers

## Database Schema

- **users** — login credentials, role
- **employees** — profile data, linked to users, self-referencing `manager_id`
- **departments** — department names
- **leave_requests** — leave applications with approval workflow

## API Endpoints

### Auth
| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/auth/register` | Register a new user | Public |
| POST | `/auth/login` | Login, returns JWT | Public |
| GET | `/auth/me` | Get current user profile | Authenticated |

### Employees
| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/employees/` | Create employee profile | Admin |
| GET | `/employees/` | List employees (filtered by role) | Authenticated |
| GET | `/employees/{id}` | Get employee by ID | Owner or Admin |
| PUT | `/employees/{id}` | Update employee | Owner or Admin |
| DELETE | `/employees/{id}` | Delete employee | Admin |

### Departments
| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/departments/` | Create department | Admin |
| GET | `/departments/` | List departments | Authenticated |
| DELETE | `/departments/{id}` | Delete department | Admin |

### Leave Requests
| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/leave-requests/` | Apply for leave | Authenticated |
| GET | `/leave-requests/my` | View own leave requests | Authenticated |
| GET | `/leave-requests/team` | View team's leave requests | Manager/Admin |
| PUT | `/leave-requests/{id}/approve` | Approve a leave request | Direct Manager/Admin |
| PUT | `/leave-requests/{id}/reject` | Reject a leave request | Direct Manager/Admin |

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/vchandana04/ems-api.git
cd ems-api
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=mysql+pymysql://root:@localhost:3306/ems_db

### 5. Create the database

In MySQL/MariaDB, create a database named `ems_db`. Tables are auto-created on first run.

### 6. Run the server
```bash
uvicorn app.main:app --reload
```

### 7. Access the API docs

Open `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

## Author

Built as a learning project to demonstrate backend engineering fundamentals: authentication, authorization, relational database design, and RESTful API development.