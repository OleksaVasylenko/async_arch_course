from typing import Any, Callable

from aiohttp import web
from aiohttp.web_exceptions import HTTPBadRequest, HTTPNotFound
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from service import TodoService
from storage.models import valid_task_statuses, valid_employee_types


async def ping(_: Any) -> web.Response:
    return web.Response(text="OK")


async def parse_json_payload(request: Request) -> Any:
    try:
        return await request.json()
    except (ValueError, TypeError):
        raise HTTPBadRequest


class TasksHandler:
    def __init__(self, service: TodoService):
        self._service = service

    async def create(self, request: Request) -> Response:
        payload = await parse_json_payload(request)
        task = await self._service.create_task(payload)
        return web.json_response({"id": task.id}, status=201)

    async def get_all(self, request: Request) -> Response:
        employee_id = request.query.get("employee_id")
        tasks = await self._service.get_multiple_tasks(employee_id)
        dict_represented = [task.as_dict() for task in tasks]
        return web.json_response(dict_represented)

    async def get(self, request: Request) -> Response:
        id_ = request.match_info["id"]
        task = await self._service.get_single_task(id_)
        if task:
            return web.json_response(task.as_dict())
        raise HTTPNotFound

    async def change_status(self, request: Request) -> Response:
        return await self._change_field(
            request=request,
            field_name="status",
            check_func=lambda arg: arg in valid_task_statuses,
        )

    async def change_employee(self, request: Request) -> Response:
        return await self._change_field(
            request=request,
            field_name="employee_id",
            check_func=lambda arg: bool(arg),
        )

    async def _change_field(
            self, request: Request, field_name: str, check_func: Callable[[Any], bool]
    ) -> Response:
        id_ = request.match_info["id"]
        payload = await parse_json_payload(request)
        value = payload.get(field_name)
        if check_func(value):
            await self._service.update_task(id_, fields={field_name: value})
            return Response()
        raise HTTPBadRequest


class EmployeesHandler:
    def __init__(self, service: TodoService):
        self._service = service

    async def create(self, request: Request) -> Response:
        payload = await parse_json_payload(request)
        type_ = payload.get("type")
        if type_ not in valid_employee_types:
            raise HTTPBadRequest
        fields = {"type": type_}
        employee = await self._service.create_employee(fields)
        return web.json_response({"id": employee.id}, status=201)

    async def get_all(self, _: Request) -> Response:
        employees = await self._service.get_multiple_employees()
        dict_represented = [employee.as_dict() for employee in employees]
        return web.json_response(dict_represented)
