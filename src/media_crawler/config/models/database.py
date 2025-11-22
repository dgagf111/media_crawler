from __future__ import annotations

from pydantic import BaseModel


class DatabaseSettings(BaseModel):
    driver: str = "mysql+pymysql"
    username: str = "root"
    password: str = "password"
    host: str = "localhost"
    port: int = 3306
    database: str = "pythonprojecttemplate"
    pool_size: int = 5
    max_overflow: int = 10
    pool_recycle: int = 3600
    echo: bool = False

    @property
    def url(self) -> str:
        return (
            f"{self.driver}://{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
        )


__all__ = ["DatabaseSettings"]
