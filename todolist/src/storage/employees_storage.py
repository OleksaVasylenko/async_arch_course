from typing import Any, Dict, List

from storage.models import Employee


class EmployeesStorage:
    model = Employee

    async def create(self, fields: Dict[str, Any]) -> Employee:
        return await self.model.create(**fields)

    async def get_all(self) -> List[Employee]:
        return await self.model.query.gino.all()
