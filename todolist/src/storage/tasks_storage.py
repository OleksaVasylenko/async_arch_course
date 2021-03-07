from typing import List, Dict, Any, Optional

from storage.models import Task


class TasksStorage:
    model = Task

    async def create(self, payload: Dict[str, Any]) -> Task:
        return await self.model.create(**payload)

    async def get(self, id: int) -> Optional[Task]:
        return await self.model.get(id)

    async def get_all(self) -> List[Task]:
        return await self.model.query.gino.all()

    async def get_by_employee(self, id_: int) -> List[Task]:
        return await self.model.query.where(self.model.id == id_).gino.all()

    async def update(self, id_: int, fields: Dict[str, Any]) -> None:
        await self.model.update.values(**fields).where(self.model.id == id_).gino.status()
