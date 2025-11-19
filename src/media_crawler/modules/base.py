from __future__ import annotations

from typing import Protocol, runtime_checkable

from fastapi import FastAPI


@runtime_checkable
class BaseModule(Protocol):
    async def on_startup(self, app: FastAPI) -> None: ...

    async def on_shutdown(self, app: FastAPI) -> None: ...

