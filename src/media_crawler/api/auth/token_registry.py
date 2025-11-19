from __future__ import annotations

import hashlib
import json
import asyncio
from contextlib import suppress
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from typing import Dict, Optional, Protocol

from prometheus_client import Counter, Gauge
from redis import Redis
from redis.exceptions import RedisError

from pythonprojecttemplate.config.settings import settings
from pythonprojecttemplate.log.logHelper import get_logger

logger = get_logger()


@dataclass
class TokenRecord:
    username: str
    access_token: str
    refresh_token: str
    access_expires_at: datetime
    refresh_expires_at: datetime
    issued_at: datetime

    def to_dict(self) -> Dict[str, str]:
        payload = asdict(self)
        payload["access_expires_at"] = self.access_expires_at.isoformat()
        payload["refresh_expires_at"] = self.refresh_expires_at.isoformat()
        payload["issued_at"] = self.issued_at.isoformat()
        return payload

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "TokenRecord":
        return cls(
            username=data["username"],
            access_token=data["access_token"],
            refresh_token=data["refresh_token"],
            access_expires_at=datetime.fromisoformat(data["access_expires_at"]),
            refresh_expires_at=datetime.fromisoformat(data["refresh_expires_at"]),
            issued_at=datetime.fromisoformat(data["issued_at"]),
        )

_IN_MEMORY_TOKEN_GAUGE = Gauge(
    "token_registry_memory_records",
    "Number of active token records temporarily held in memory.",
)
_IN_MEMORY_REVOKED_GAUGE = Gauge(
    "token_registry_memory_revocations",
    "Revoked token entries tracked in memory.",
)
_IN_MEMORY_CLEANUP_COUNTER = Counter(
    "token_registry_memory_cleanup_runs_total",
    "Number of background cleanup sweeps executed by the memory token store.",
)


class TokenStore(Protocol):
    def save(self, username: str, record: TokenRecord, ttl_seconds: int) -> None: ...

    def read(self, username: str) -> Optional[TokenRecord]: ...

    def delete(self, username: str) -> None: ...

    def mark_revoked(self, token_hash: str, ttl_seconds: int) -> None: ...

    def is_revoked(self, token_hash: str) -> bool: ...


class RedisTokenStore:
    def __init__(self, client: Redis | None = None) -> None:
        cfg = settings.security.revocation
        redis_cfg = cfg.redis
        self._client = client or Redis(
            host=redis_cfg.host,
            port=redis_cfg.port,
            db=redis_cfg.db,
            username=redis_cfg.username or None,
            password=redis_cfg.password or None,
            ssl=redis_cfg.ssl,
            decode_responses=True,
        )
        self._client.ping()
        self._prefix = cfg.key_prefix
        self._default_ttl = cfg.default_ttl_seconds

    def _user_key(self, username: str) -> str:
        return f"{self._prefix}:active:{username}"

    def _revoked_key(self, token_hash: str) -> str:
        return f"{self._prefix}:revoked:{token_hash}"

    def save(self, username: str, record: TokenRecord, ttl_seconds: int) -> None:
        ttl = ttl_seconds if ttl_seconds > 0 else self._default_ttl
        ttl = max(ttl, 1)
        payload = json.dumps(record.to_dict())
        self._client.setex(self._user_key(username), ttl, payload)

    def read(self, username: str) -> Optional[TokenRecord]:
        raw = self._client.get(self._user_key(username))
        if not raw:
            return None
        return TokenRecord.from_dict(json.loads(raw))

    def delete(self, username: str) -> None:
        self._client.delete(self._user_key(username))

    def mark_revoked(self, token_hash: str, ttl_seconds: int) -> None:
        ttl = ttl_seconds if ttl_seconds > 0 else self._default_ttl
        ttl = max(ttl, 1)
        self._client.setex(self._revoked_key(token_hash), ttl, "1")

    def is_revoked(self, token_hash: str) -> bool:
        return bool(self._client.exists(self._revoked_key(token_hash)))


class InMemoryTokenStore:
    def __init__(self) -> None:
        self._records: Dict[str, tuple[TokenRecord, datetime]] = {}
        self._revoked: Dict[str, datetime] = {}
        self._cleanup_task: asyncio.Task | None = None
        self._cleanup_shutdown: asyncio.Event | None = None
        self._cleanup_interval = settings.security.revocation.memory_cleanup_interval_seconds
        self._record_metrics()

    def save(self, username: str, record: TokenRecord, ttl_seconds: int) -> None:
        self._purge_expired_user(username)
        expires_at = datetime.now(UTC) + timedelta(seconds=max(ttl_seconds, 1))
        self._records[username] = (record, expires_at)
        self._record_metrics()

    def read(self, username: str) -> Optional[TokenRecord]:
        item = self._records.get(username)
        if not item:
            return None
        record, expires_at = item
        if expires_at < datetime.now(UTC):
            self.delete(username)
            return None
        return record

    def delete(self, username: str) -> None:
        self._records.pop(username, None)
        self._record_metrics()

    def mark_revoked(self, token_hash: str, ttl_seconds: int) -> None:
        self._purge_expired_revoked(token_hash)
        self._revoked[token_hash] = datetime.now(UTC) + timedelta(seconds=max(ttl_seconds, 1))
        self._record_metrics()

    def is_revoked(self, token_hash: str) -> bool:
        expiry = self._revoked.get(token_hash)
        if not expiry:
            return False
        if expiry < datetime.now(UTC):
            self._revoked.pop(token_hash, None)
            self._record_metrics()
            return False
        return True

    async def start_auto_cleanup(self) -> None:
        if self._cleanup_task and not self._cleanup_task.done():
            return
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            logger.warning("Unable to start in-memory token cleanup task: no running event loop detected")
            return

        self._cleanup_shutdown = asyncio.Event()
        self._cleanup_task = loop.create_task(self._cleanup_loop())
        logger.info(
            "Started in-memory token cleanup loop (interval=%ss)",
            self._cleanup_interval,
        )

    async def stop_auto_cleanup(self) -> None:
        if not self._cleanup_task:
            return
        if self._cleanup_shutdown:
            self._cleanup_shutdown.set()
        self._cleanup_task.cancel()
        with suppress(asyncio.CancelledError):
            await self._cleanup_task
        self._cleanup_task = None
        self._cleanup_shutdown = None
        logger.info("Stopped in-memory token cleanup loop")

    async def _cleanup_loop(self) -> None:
        assert self._cleanup_shutdown is not None
        try:
            while not self._cleanup_shutdown.is_set():
                try:
                    await asyncio.wait_for(self._cleanup_shutdown.wait(), timeout=self._cleanup_interval)
                    break
                except asyncio.TimeoutError:
                    self._run_cleanup_sweep()
        except asyncio.CancelledError:
            self._run_cleanup_sweep()
            raise

    def _run_cleanup_sweep(self) -> None:
        self._purge_expired_entries()
        _IN_MEMORY_CLEANUP_COUNTER.inc()
        self._record_metrics()

    def _purge_expired_entries(self) -> None:
        now = datetime.now(UTC)
        expired_users = [user for user, (_, expires_at) in self._records.items() if expires_at < now]
        for user in expired_users:
            self._records.pop(user, None)

        expired_revocations = [token for token, expires_at in self._revoked.items() if expires_at < now]
        for token in expired_revocations:
            self._revoked.pop(token, None)

    def _purge_expired_user(self, username: str) -> None:
        item = self._records.get(username)
        if not item:
            return
        _, expires_at = item
        if expires_at < datetime.now(UTC):
            self._records.pop(username, None)

    def _purge_expired_revoked(self, token_hash: str) -> None:
        expiry = self._revoked.get(token_hash)
        if expiry and expiry < datetime.now(UTC):
            self._revoked.pop(token_hash, None)

    def _record_metrics(self) -> None:
        _IN_MEMORY_TOKEN_GAUGE.set(len(self._records))
        _IN_MEMORY_REVOKED_GAUGE.set(len(self._revoked))


class TokenRegistry:
    def __init__(self, store: TokenStore | None = None):
        self.store = store or self._build_store()
        self._cleanup_started = False

    def _build_store(self) -> TokenStore:
        cfg = settings.security.revocation
        if cfg.backend == "redis":
            try:
                logger.info("Initializing Redis token store for revocation tracking")
                return RedisTokenStore()
            except RedisError as exc:
                logger.warning(
                    "Redis token store unavailable (%s); using in-memory fallback that does not persist tokens",
                    exc,
                )
        else:
            logger.warning(
                "Token revocation backend configured for '%s'; using in-memory fallback."
                " Tokens will be lost on process restart without Redis enabled.",
                cfg.backend,
            )
        return InMemoryTokenStore()

    async def startup(self) -> None:
        if self._cleanup_started:
            return
        store = self.store
        start_cleanup = getattr(store, "start_auto_cleanup", None)
        if callable(start_cleanup):
            await start_cleanup()
            self._cleanup_started = True

    async def shutdown(self) -> None:
        store = self.store
        stop_cleanup = getattr(store, "stop_auto_cleanup", None)
        if callable(stop_cleanup):
            await stop_cleanup()
        self._cleanup_started = False

    def persist(self, record: TokenRecord) -> TokenRecord:
        ttl_seconds = max(int((record.refresh_expires_at - datetime.now(UTC)).total_seconds()), 1)
        self.store.save(record.username, record, ttl_seconds)
        return record

    def read(self, username: str) -> Optional[TokenRecord]:
        return self.store.read(username)

    def delete(self, username: str) -> None:
        self.store.delete(username)

    def mark_revoked_token(self, token: str, expires_at: datetime) -> None:
        ttl_seconds = max(int((expires_at - datetime.now(UTC)).total_seconds()), 1)
        self.store.mark_revoked(self._hash_token(token), ttl_seconds)

    def is_token_revoked(self, token: str) -> bool:
        return self.store.is_revoked(self._hash_token(token))

    def revoke_user(self, username: str) -> None:
        record = self.read(username)
        if not record:
            return
        self.mark_revoked_token(record.access_token, record.access_expires_at)
        self.mark_revoked_token(record.refresh_token, record.refresh_expires_at)
        self.delete(username)

    @staticmethod
    def _hash_token(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()


class TokenAuditLogger:
    def __init__(self):
        self._settings = settings.security.audit

    def log(self, action: str, username: str, **context: object) -> None:
        if not self._settings.enabled:
            return
        safe_username = username if self._settings.include_username else "***"
        flattened = ", ".join(f"{key}={value}" for key, value in context.items() if value is not None)
        suffix = f" {flattened}" if flattened else ""
        logger.info("token.%s user=%s%s", action, safe_username, suffix)


token_registry = TokenRegistry()
token_audit_logger = TokenAuditLogger()
