from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Dict, List

import yaml
from pydantic_settings import PydanticBaseSettingsSource

from .base import (
    BASE_FILENAMES,
    CONFIG_ENV_FILE_ENV_VAR,
    CONFIG_ENV_VAR,
    CONFIG_LOAD_TRACE,
    LoadRecord,
    deep_merge,
    expand_path,
    record_load,
    resolve_config_dir,
)

logger = logging.getLogger(__name__)


def _load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
        if not isinstance(data, dict):
            raise ValueError(f"{path} must define a mapping")
        return data


def _discover_env(config_dir: Path) -> str:
    if os.getenv(CONFIG_ENV_VAR):
        return os.getenv(CONFIG_ENV_VAR, "dev")

    for name in BASE_FILENAMES:
        base_path = config_dir / name
        data = _load_yaml(base_path)
        if "env" in data and data["env"]:
            return str(data["env"])

    return "dev"


class YamlConfigSettingsSource(PydanticBaseSettingsSource):
    """
    YAML 配置源：支持 base/env 组合与自定义覆盖。
    加载顺序：
      1. BASE_FILENAMES（env.yaml/base.yaml）
      2. <env>.yaml
      3. PPT_ENV_FILE 指定的其他文件（若设置则替换步骤 2）
    """

    def __call__(self) -> Dict[str, Any]:
        config_dir = resolve_config_dir()
        env_name = _discover_env(config_dir)
        files = self._build_files(config_dir, env_name)

        merged: Dict[str, Any] = {}
        for path in files:
            try:
                data = _load_yaml(path)
                merged = deep_merge(merged, data)
                record_load(
                    LoadRecord(
                        source="yaml",
                        path=path if path.exists() else None,
                        keys=list(data.keys()) if isinstance(data, dict) else [],
                        status="ok" if path.exists() else "missing",
                        env=env_name,
                        message=None
                        if path.exists()
                        else f"{path} not found",
                    )
                )
            except Exception as exc:
                record_load(
                    LoadRecord(
                        source="yaml",
                        path=path,
                        keys=[],
                        status="error",
                        env=env_name,
                        message=str(exc),
                    )
                )
                raise

        merged["env"] = env_name
        return merged

    def _build_files(self, config_dir: Path, env_name: str) -> List[Path]:
        override_env_file = os.getenv(CONFIG_ENV_FILE_ENV_VAR)
        if override_env_file:
            return [expand_path(Path(override_env_file))]

        files = [config_dir / name for name in BASE_FILENAMES]
        files.append(config_dir / f"{env_name}.yaml")
        return files

    def get_field_value(self, field: Any, field_name: str) -> Any:
        data = self.__call__()
        return data.get(field_name)

    def prepare_field_value(
        self, field_name: str, field: Any, value: Any, value_is_complex: bool
    ) -> Any:
        return value
