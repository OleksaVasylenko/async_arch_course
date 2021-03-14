import logging

from aiohttp import web
from aiohttp.abc import Application

from service import TodoService
from src.config import Config
from src.storage import setup_storage
from src.handlers import TasksHandler, ping, EmployeesHandler
from storage.employees_storage import EmployeesStorage
from storage.tasks_storage import TasksStorage


def create_app() -> Application:
    app = web.Application()
    app["config"] = Config.from_env()
    app["todo_service"] = create_todo_service()
    app.cleanup_ctx.append(setup_storage)
    return app


def create_tasks_storage() -> TasksStorage:
    return TasksStorage()


def create_employees_storage() -> EmployeesStorage:
    return EmployeesStorage()


def create_todo_service() -> TodoService:
    tasks_storage = create_tasks_storage()
    employees_storage = create_employees_storage()
    return TodoService(tasks_storage=tasks_storage, employees_storage=employees_storage)


def setup_routes(app: Application) -> None:
    app.router.add_get("/ping", ping)
    setup_tasks_routes(app)
    setup_employees_routes(app)


def setup_tasks_routes(app: Application) -> None:
    todo_service = app["todo_service"]
    handler = TasksHandler(todo_service)
    app.router.add_post("/tasks", handler.create)
    app.router.add_get("/tasks", handler.get_all)
    app.router.add_get("/tasks/{id}", handler.get)
    app.router.add_put("/tasks/{id}/status", handler.change_status)
    app.router.add_put("/tasks/{id}/employee", handler.change_employee)


def setup_employees_routes(app: Application) -> None:
    todo_service = app["todo_service"]
    handler = EmployeesHandler(todo_service)
    app.router.add_post("/employees", handler.create)
    app.router.add_get("/employees", handler.get_all)


def init_logging():
    logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    init_logging()
    app = create_app()
    setup_routes(app)
    web.run_app(app)
