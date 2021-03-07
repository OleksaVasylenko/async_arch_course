from typing import Any, Dict, List, Optional

from storage.employees_storage import EmployeesStorage
from storage.models import Task, Employee
from storage.tasks_storage import TasksStorage


class TodoService:
    def __init__(self, tasks_storage: TasksStorage, employees_storage: EmployeesStorage):
        self._tasks_storage = tasks_storage
        self._employees_storage = employees_storage

    async def create_task(self, payload: Dict[str, Any]) -> Task:
        return await self._tasks_storage.create(payload)

    async def get_multiple_tasks(self, employee_id: Optional[str] = None) -> List[Task]:
        if employee_id:
            return await self._tasks_storage.get_by_employee(int(employee_id))
        return await self._tasks_storage.get_all()

    async def get_single_task(self, id_: str) -> Optional[Task]:
        return await self._tasks_storage.get(int(id_))

    async def update_task(self, id_: str, fields: Dict[str, Any]) -> None:
        await self._tasks_storage.update(int(id_), fields)

    async def create_employee(self, fields: Dict[str, Any]) -> Employee:
        return await self._employees_storage.create(fields)

    async def get_multiple_employees(self) -> List[Employee]:
        return await self._employees_storage.get_all()
