from __future__ import annotations

import importlib
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI

from pythonprojecttemplate.config.settings import settings
from pythonprojecttemplate.log.logHelper import get_logger

from .base import BaseModule

logger = get_logger()


def _resolve_module(path: str) -> BaseModule:
    module = importlib.import_module(path)
    if hasattr(module, "get_module"):
        instance = module.get_module()
    elif hasattr(module, "Module"):
        attr = module.Module
        instance = attr() if callable(attr) else attr
    elif hasattr(module, "module"):
        instance = module.module
    else:
        raise RuntimeError(f"Module {path} must expose get_module()/Module/module")
    if not isinstance(instance, BaseModule):
        raise TypeError(f"Module {path} does not implement BaseModule protocol")
    return instance


@asynccontextmanager
async def module_lifespan(app: FastAPI):
    modules: List[BaseModule] = []
    for entry in settings.module.modules:
        full_path = entry if "." in entry else f"{settings.module.base_path}.{entry}"
        try:
            module_instance = _resolve_module(full_path)
            modules.append(module_instance)
        except Exception as exc:
            logger.error(f"Failed to load module {full_path}: {exc}")
            continue

    for module in modules:
        await module.on_startup(app)

    try:
        yield
    finally:
        for module in reversed(modules):
            try:
                await module.on_shutdown(app)
            except Exception as exc:
                logger.error(f"Failed to shut down module {module}: {exc}")

