from enum import Enum
from typing import Any, Dict

from src.storage import db


class TaskStatus(str, Enum):
    open = "open"
    done = "done"


valid_task_statuses = tuple(TaskStatus)


def default_status() -> str:
    return TaskStatus.open.value


class EmployeeType(str, Enum):
    worker = "worker"
    admin = "admin"
    accountant = "accountant"
    manager = "manager"


valid_employee_types = tuple(EmployeeType)


class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Enum(EmployeeType), nullable=False)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
        }


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Unicode(), nullable=False)
    status = db.Column(db.Enum(TaskStatus), nullable=False, default=default_status)
    employee_id = db.Column(
        db.Integer,
        db.ForeignKey("employees.id", ondelete="SET NULL"),
        nullable=True,
    )

    def as_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "employee_id": self.employee_id,
        }
