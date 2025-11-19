from __future__ import annotations

import pytest

from pythonprojecttemplate.config.settings import AppSettings


@pytest.fixture(autouse=True)
def clear_security_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """清理可能存在的安全相关环境变量，避免测试之间串扰。"""
    for key in (
        "PPT_SECURITY__TOKEN__SECRET_KEY",
        "PPT_SECURITY__REVOCATION__BACKEND",
        "PPT_SECURITY__REVOCATION__REDIS__HOST",
        "PPT_SECURITY__REVOCATION__REDIS__PORT",
        "PPT_SECURITY__REVOCATION__REDIS__DB",
        "PPT_SECURITY__REVOCATION__REDIS__USERNAME",
        "PPT_SECURITY__REVOCATION__REDIS__PASSWORD",
        "PPT_SECURITY__REVOCATION__REDIS__SSL",
        "SECRET_KEY",
        "PPT_SECRET_KEY",
    ):
        monkeypatch.delenv(key, raising=False)


def test_security_settings_use_namespaced_variables(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PPT_SECURITY__TOKEN__SECRET_KEY", "new-secret")
    monkeypatch.setenv("PPT_SECURITY__REVOCATION__BACKEND", "redis")
    monkeypatch.setenv("PPT_SECURITY__REVOCATION__REDIS__HOST", "redis.internal")
    monkeypatch.setenv("PPT_SECURITY__REVOCATION__REDIS__PORT", "6380")
    monkeypatch.setenv("PPT_SECURITY__REVOCATION__REDIS__DB", "5")
    monkeypatch.setenv("PPT_SECURITY__REVOCATION__REDIS__USERNAME", "svc-user")
    monkeypatch.setenv("PPT_SECURITY__REVOCATION__REDIS__PASSWORD", "svc-pass")
    monkeypatch.setenv("PPT_SECURITY__REVOCATION__REDIS__SSL", "true")

    settings = AppSettings()

    assert settings.security.token.secret_key == "new-secret"
    assert settings.security.revocation.backend == "redis"
    assert settings.security.revocation.redis.host == "redis.internal"
    assert settings.security.revocation.redis.port == 6380
    assert settings.security.revocation.redis.db == 5
    assert settings.security.revocation.redis.username == "svc-user"
    assert settings.security.revocation.redis.password == "svc-pass"
    assert settings.security.revocation.redis.ssl is True


def test_legacy_environment_variables_no_longer_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SECRET_KEY", "legacy-secret")

    settings = AppSettings()

    assert settings.security.token.secret_key != "legacy-secret"
