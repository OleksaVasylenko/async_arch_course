import os
from typing import NamedTuple, Optional, Mapping, Any


class DatabaseConfig(NamedTuple):
    host: str
    port: int
    name: str
    user: str
    password: str

    @classmethod
    def from_env(cls, env: Optional[Mapping[str, Any]] = None) -> "DatabaseConfig":
        env = env or os.environ
        return cls(
            host=env["DB_HOST"],
            port=int(env["DB_PORT"]),
            name=env["DB_NAME"],
            user=env["DB_USER"],
            password=env["DB_PASSWORD"],
        )

    @property
    def dsn(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class Config(NamedTuple):
    database: DatabaseConfig

    @classmethod
    def from_env(cls, env: Optional[Mapping[str, Any]] = None) -> "Config":
        database = DatabaseConfig.from_env(env)
        return cls(database=database)
