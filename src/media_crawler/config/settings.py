from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Literal

import yaml
from pydantic import BaseModel, Field, FieldValidationInfo, field_validator, model_validator
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict


logger = logging.getLogger(__name__)


CONFIG_LOAD_META: Dict[str, str] = {
    "env_file": "",
    "config_file": "",
    "env_name": "",
    "source": "environment",
}

def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    result: Dict[str, Any] = {**base}
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


class YamlConfigSettingsSource(PydanticBaseSettingsSource):
    """
    A source class that loads variables from a YAML file
    """

    def __init__(self, settings_cls: type[BaseSettings]) -> None:
        super().__init__(settings_cls)

    def _load_yaml(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            return {}
        with path.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
            if not isinstance(data, dict):
                raise ValueError(f"{path} must define a mapping")
            return data

    def __call__(self) -> Dict[str, Any]:
        base_dir = Path(__file__).resolve().parent
        env_yaml = base_dir / "env.yaml"
        env_data = self._load_yaml(env_yaml)
        env_name = os.getenv("PPT_ENV", env_data.get("env", "dev"))
        config_yaml = base_dir / f"{env_name}.yaml"
        config_data = self._load_yaml(config_yaml)
        merged = _deep_merge(env_data, config_data)
        merged["env"] = env_name
        CONFIG_LOAD_META.update(
            {
                "env_file": str(env_yaml),
                "config_file": str(config_yaml),
                "env_name": env_name,
                "source": "yaml+env",
            }
        )
        return merged

    def get_field_value(self, field: Any, field_name: str) -> Any:
        data = self.__call__()
        return data.get(field_name)

    def prepare_field_value(self, field_name: str, field: Any, value: Any, value_is_complex: bool) -> Any:
        return value


class ModuleSettings(BaseModel):
    base_path: str = "pythonprojecttemplate.modules"
    modules: List[str] = Field(default_factory=list)


class LoggingSettings(BaseModel):
    project_name: str = "python_project_template"
    base_log_directory: str = "../log"
    log_level: str = "INFO"


class SchedulerExecutorsSettings(BaseModel):
    default_threads: int = 20
    process_pool: int = 5


class SchedulerJobDefaultsSettings(BaseModel):
    coalesce: bool = False
    max_instances: int = 3


class SchedulerSettings(BaseModel):
    executors: SchedulerExecutorsSettings = SchedulerExecutorsSettings()
    job_defaults: SchedulerJobDefaultsSettings = SchedulerJobDefaultsSettings()


class CommonPortsSettings(BaseModel):
    redis_default: int = 6379
    mysql_default: int = 3306


class CommonSettings(BaseModel):
    time_zone: str = "Asia/Shanghai"
    api_version: str = "v1"
    ports: CommonPortsSettings = CommonPortsSettings()


class ApiSettings(BaseModel):
    title: str = "Python Project Template API"
    description: str = "A production ready FastAPI service"
    version: str = "3.1.0"
    host: str = "0.0.0.0"
    port: int = 8000
    loop: str = "asyncio"
    open_api_on_startup: bool = True
    docs_url: str | None = "/docs"
    cors_origins: List[str] = Field(default_factory=lambda: ["*"])
    max_concurrency: int = 100
    request_timeout: int = 30


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


class CacheRedisSettings(BaseModel):
    host: str = "localhost"
    port: int = 6379
    db: int = 0


class CacheSettings(BaseModel):
    type: str = "memory"
    ttl: int = 3600
    max_size: int = 1000
    redis: CacheRedisSettings = CacheRedisSettings()


class MonitoringSettings(BaseModel):
    prometheus_port: int = 9966
    cpu_threshold: int = 80
    memory_threshold: int = 80
    interval_seconds: int = Field(default=60, ge=5, le=3600)
    max_retries: int = Field(default=3, ge=0, le=50)
    retry_interval_seconds: int = Field(default=5, ge=1, le=300)


class SecurityTokenSettings(BaseModel):
    secret_key: str = Field(default="change-me", min_length=8)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = Field(default=180, ge=5, le=1440)
    refresh_token_expire_days: int = Field(default=7, ge=1, le=90)


class SecurityRedisSettings(BaseModel):
    host: str = "localhost"
    port: int = 6379
    db: int = 2
    username: str | None = None
    password: str | None = None
    ssl: bool = False

    @field_validator("host", mode="before")
    @classmethod
    def _ensure_host(cls, value: str | None) -> str:
        if value is None:
            return "localhost"
        host = value.strip()
        if not host:
            logger.warning("Empty Redis host detected, falling back to 'localhost'")
            return "localhost"
        return host

    @field_validator("port", "db", mode="before")
    @classmethod
    def _ensure_numeric(cls, value: Any, info: FieldValidationInfo) -> Any:
        if value in (None, "", " "):
            defaults = {"port": 6379, "db": 2}
            return defaults[info.field_name]
        return value


class SecurityRevocationSettings(BaseModel):
    backend: Literal["redis", "memory"] = "memory"
    redis: SecurityRedisSettings = SecurityRedisSettings()
    key_prefix: str = "ppt:security"
    default_ttl_seconds: int = Field(default=7 * 24 * 3600, gt=0)
    memory_cleanup_interval_seconds: int = Field(default=120, ge=5, le=3600)

    @field_validator("backend", mode="before")
    @classmethod
    def _normalize_backend(cls, value: str | None) -> str:
        if value is None:
            return "memory"
        backend = str(value).lower().strip()
        if backend not in {"redis", "memory"}:
            logger.warning("Unknown token backend '%s', using in-memory backend", value)
            return "memory"
        return backend


class TokenAuditSettings(BaseModel):
    enabled: bool = True
    include_username: bool = True


class SecuritySettings(BaseModel):
    token: SecurityTokenSettings = SecurityTokenSettings()
    revocation: SecurityRevocationSettings = SecurityRevocationSettings()
    audit: TokenAuditSettings = TokenAuditSettings()


class EncryptionSettings(BaseModel):
    """加密配置管理"""
    aes_key_hex: str = Field(
        default="",
        description="AES加密密钥（十六进制格式，64字符=32字节）"
    )

    @property
    def aes_key(self) -> bytes:
        """
        获取AES密钥（字节格式）

        :return: 32字节的AES密钥
        :raises ValueError: 密钥未配置或格式不正确
        """
        if not self.aes_key_hex:
            raise ValueError(
                "未配置AES密钥！请设置PPT_ENCRYPTION__AES_KEY环境变量\n"
                "生成密钥命令：python -c \"import os; print(os.urandom(32).hex())\""
            )

        if len(self.aes_key_hex) != 64:
            raise ValueError(
                f"AES密钥长度错误：{len(self.aes_key_hex)}，应为64个十六进制字符"
            )

        try:
            key = bytes.fromhex(self.aes_key_hex)
            if len(key) != 32:
                raise ValueError(f"AES密钥长度错误：{len(key)}字节，应为32字节")
            return key
        except ValueError as e:
            raise ValueError(f"AES密钥格式错误：应为64个十六进制字符") from e

    @property
    def is_configured(self) -> bool:
        """检查是否已配置加密密钥"""
        return bool(self.aes_key_hex)


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="PPT_",
        env_file=".env",
        extra="allow",
        populate_by_name=True,
        env_nested_delimiter="__",
    )

    env: str = "dev"
    config_version: str = Field(default="2024.10", alias="config_version")
    module: ModuleSettings = Field(default_factory=ModuleSettings, alias="module_config")
    logging: LoggingSettings = LoggingSettings()
    scheduler: SchedulerSettings = SchedulerSettings()
    common: CommonSettings = CommonSettings()
    api: ApiSettings = ApiSettings()
    database: DatabaseSettings = DatabaseSettings()
    cache: CacheSettings = CacheSettings()
    monitoring: MonitoringSettings = MonitoringSettings()
    security: SecuritySettings = SecuritySettings()
    encryption: EncryptionSettings = Field(default_factory=EncryptionSettings, alias="encryption_config")
    tasks: Dict[str, Any] = Field(default_factory=dict)

    def model_post_init(self, __context: Any) -> None:
        self.load_origin = dict(CONFIG_LOAD_META)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            YamlConfigSettingsSource(settings_cls),
            file_secret_settings,
        )


settings = AppSettings()
