from contextlib import asynccontextmanager

from async_exit_stack import AsyncExitStack

from aiohttp.web_app import Application
from gino import Gino

from src.config import DatabaseConfig, Config

db = Gino()


def has_connection() -> bool:
    return db.is_bound()


async def db_connect(config: DatabaseConfig) -> None:
    if has_connection():
        return

    await db.set_bind(bind=config.dsn)


async def db_disconnect() -> None:
    if not has_connection():
        return
    await db.pop_bind().close()


@asynccontextmanager
async def setup_db(config: DatabaseConfig) -> None:
    await db_connect(config)
    yield
    await db_disconnect()


async def setup_storage(app: Application) -> None:
    config: Config = app["config"]
    async with AsyncExitStack() as exit_stack:
        await exit_stack.enter_async_context(setup_db(config.database))
        yield
