from datetime import UTC, datetime, timedelta

import pytest

fakeredis = pytest.importorskip("fakeredis")

from pythonprojecttemplate.api.auth.token_registry import (
    RedisTokenStore,
    TokenRecord,
    TokenRegistry,
)


def test_redis_token_registry_coherence():
    fake_client = fakeredis.FakeRedis(decode_responses=True)
    store_a = RedisTokenStore(client=fake_client)
    store_b = RedisTokenStore(client=fake_client)
    registry_a = TokenRegistry(store=store_a)
    registry_b = TokenRegistry(store=store_b)

    issued_at = datetime.now(UTC)
    record = TokenRecord(
        username="alice",
        access_token="access-1",
        refresh_token="refresh-1",
        access_expires_at=issued_at + timedelta(minutes=5),
        refresh_expires_at=issued_at + timedelta(hours=1),
        issued_at=issued_at,
    )

    registry_a.persist(record)

    loaded = registry_b.read("alice")
    assert loaded is not None
    assert loaded.access_token == "access-1"

    registry_b.revoke_user("alice")

    assert registry_a.read("alice") is None
    assert registry_a.is_token_revoked("access-1")
    assert registry_a.is_token_revoked("refresh-1")
