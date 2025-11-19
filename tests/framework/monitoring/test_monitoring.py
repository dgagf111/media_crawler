import asyncio
from unittest.mock import patch

import pytest
import requests

from pythonprojecttemplate.log.logHelper import get_logger
from pythonprojecttemplate.monitoring.alerting import check_cpu_usage, check_memory_usage
from pythonprojecttemplate.monitoring.main import monitoring_center
from pythonprojecttemplate.monitoring.prometheus_exporter import (
    CPU_USAGE,
    MEMORY_USAGE,
    REQUEST_COUNT,
    RESPONSE_TIME,
)

logger = get_logger()


def _run_monitoring_test(body, *, test_mode: bool = True):
    async def runner():
        try:
            await monitoring_center.start(test_mode=test_mode)
        except OSError:
            pytest.skip("监控模块无法在当前环境中启动网络服务")
        try:
            await body()
        finally:
            await monitoring_center.shutdown()

    asyncio.run(runner())


def test_prometheus_server():
    async def body():
        response = await asyncio.to_thread(
            requests.get, f"http://127.0.0.1:{monitoring_center.metrics_port}"
        )
        assert response.status_code == 200

    _run_monitoring_test(body)


def test_metrics_creation():
    assert REQUEST_COUNT._name == "app_requests"
    assert RESPONSE_TIME._name == "app_response_latency_seconds"
    assert CPU_USAGE._name == "system_cpu_usage"
    assert MEMORY_USAGE._name == "system_memory_usage"


def test_metrics_update():
    initial_count = REQUEST_COUNT._value.get()
    REQUEST_COUNT.inc()
    assert REQUEST_COUNT._value.get() == initial_count + 1

    RESPONSE_TIME.observe(0.1)
    assert RESPONSE_TIME._sum.get() > 0


@patch("psutil.cpu_percent")
@patch("psutil.virtual_memory")
def test_system_metrics_update(mock_memory, mock_cpu):
    mock_cpu.return_value = 50.0
    mock_memory.return_value.percent = 60.0

    CPU_USAGE.set(mock_cpu.return_value)
    MEMORY_USAGE.set(mock_memory.return_value.percent)

    assert CPU_USAGE._value.get() == 50.0
    assert MEMORY_USAGE._value.get() == 60.0


@patch("pythonprojecttemplate.monitoring.alerting.logger.warning")
def test_alerting(mock_logger):
    assert not check_cpu_usage(threshold=90)
    mock_logger.assert_not_called()

    assert check_cpu_usage(threshold=80)
    mock_logger.assert_called_with("CPU 使用率过高: 85%")

    mock_logger.reset_mock()

    check_memory_usage(threshold=80)
    mock_logger.assert_not_called()

    check_memory_usage(threshold=70)
    mock_logger.assert_called_with("内存使用率过高: 75%")


def test_monitoring_reload_without_leaks():
    async def body():
        for _ in range(100):
            try:
                await monitoring_center.start(test_mode=True)
            except OSError:
                pytest.skip("监控模块无法在当前环境中启动网络服务")
            assert monitoring_center.running
            await monitoring_center.shutdown()
            assert not monitoring_center.running

    asyncio.run(body())
