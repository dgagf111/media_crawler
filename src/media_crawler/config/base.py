from __future__ import annotations

import importlib.resources as resources
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List

CONFIG_ENV_VAR = "PPT_ENV"
CONFIG_DIR_ENV_VAR = "PPT_CONFIG_DIR"
CONFIG_ENV_FILE_ENV_VAR = "PPT_ENV_FILE"
DEFAULT_CONFIG_DIRNAME = "config"
BASE_FILENAMES = ("env.yaml", "base.yaml")


@dataclass
class LoadRecord:
    source: str
    path: Path | None
    keys: List[str] = field(default_factory=list)
    status: str = "ok"
    env: str | None = None
    message: str | None = None


CONFIG_LOAD_TRACE: List[LoadRecord] = []


def clear_load_trace() -> None:
    CONFIG_LOAD_TRACE.clear()


def record_load(record: LoadRecord) -> None:
    CONFIG_LOAD_TRACE.append(record)


def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    result: Dict[str, Any] = {**base}
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def _traversable_to_path(traversable: resources.abc.Traversable) -> Path:
    return Path(str(traversable))


def resolve_config_dir() -> Path:
    custom_dir = os.getenv(CONFIG_DIR_ENV_VAR)
    if custom_dir:
        return Path(custom_dir).expanduser().resolve()

    try:
        traversable = resources.files("pythonprojecttemplate.config").joinpath(
            DEFAULT_CONFIG_DIRNAME
        )
        if traversable.exists():
            return _traversable_to_path(traversable)
    except Exception:
        pass

    return Path(__file__).resolve().parent


def expand_path(path: Path) -> Path:
    return path.expanduser().resolve()


def redact_keys(data: Dict[str, Any], sensitive_keys: Iterable[str]) -> Dict[str, Any]:
    lowered = {key.lower() for key in sensitive_keys}
    redacted: Dict[str, Any] = {}
    for key, value in data.items():
        if key.lower() in lowered:
            redacted[key] = "***"
        elif isinstance(value, dict):
            redacted[key] = redact_keys(value, lowered)
        else:
            redacted[key] = value
    return redacted
