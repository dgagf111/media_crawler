import asyncio
import socket
from contextlib import suppress
from typing import Callable

from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from pythonprojecttemplate.config.settings import settings
from pythonprojecttemplate.log.logHelper import get_logger

from .alerting import setup_alerting, check_cpu_usage, check_memory_usage
from .prometheus_exporter import record_monitoring_error, setup_metrics

logger = get_logger()


class MonitoringCenter:
    def __init__(self):
        self.running = False
        self.alert_task: asyncio.Task | None = None
        self._alert_shutdown = asyncio.Event()
        self._metrics_server: asyncio.AbstractServer | None = None
        self._metrics_task: asyncio.Task | None = None
        self.metrics_port = settings.monitoring.prometheus_port
        self._interval = settings.monitoring.interval_seconds
        self._max_retries = settings.monitoring.max_retries
        self._retry_interval = settings.monitoring.retry_interval_seconds
        self._check_timeout = max(5, min(self._interval, 30))

    async def start(self, test_mode: bool = False):
        if self.running:
            logger.warning("监控中心已经在运行")
            return

        logger.info("启动监控模块（asyncio 模式）")

        try:
            self.running = True
            port = self._select_port(settings.monitoring.prometheus_port)
            setup_metrics()
            await self._start_metrics_server(port)

            self._alert_shutdown = asyncio.Event()

            if not test_mode:
                self.alert_task = asyncio.create_task(self._run_alerting())
                logger.info("监控告警异步任务已启动")

            logger.info("监控模块已启动，Prometheus 指标地址 http://127.0.0.1:%s", self.metrics_port)
        except Exception as e:
            logger.error(f"监控模块启动失败: {e}", exc_info=True)
            self.running = False
            if test_mode:
                raise

    def _select_port(self, preferred_port: int) -> int:
        if self._is_port_available(preferred_port):
            return preferred_port
        return self._find_available_port()

    async def _start_metrics_server(self, port: int) -> None:
        await self._create_metrics_server(port)
        self._metrics_task = asyncio.create_task(self._monitor_metrics_server())

    async def _create_metrics_server(self, port: int) -> None:
        if self._metrics_server:
            self._metrics_server.close()
            await self._metrics_server.wait_closed()
        try:
            self._metrics_server = await asyncio.start_server(
                self._handle_metrics_request,
                host="127.0.0.1",
                port=port,
            )
        except OSError as exc:
            record_monitoring_error("server_error")
            logger.error("无法启动指标服务: %s", exc)
            raise

        self.metrics_port = port
        logger.info("Prometheus 指标服务监听端口 %s", port)

    async def _monitor_metrics_server(self) -> None:
        retries = 0
        base_port = settings.monitoring.prometheus_port
        while self.running and self._metrics_server:
            try:
                await self._metrics_server.serve_forever()
                break
            except asyncio.CancelledError:
                raise
            except OSError as exc:
                record_monitoring_error("server_error")
                retries += 1
                logger.error("Monitoring server error: %s", exc)
                if self._max_retries and retries > self._max_retries:
                    logger.error("监控指标服务重启超过最大次数(%s)，停止重试", self._max_retries)
                    break
                await asyncio.sleep(self._retry_interval)
                try:
                    await self._create_metrics_server(self._select_port(base_port))
                except OSError:
                    continue
            except Exception as exc:
                record_monitoring_error("server_error")
                logger.exception("Unexpected monitoring server failure: %s", exc)
                break
        logger.info("监控指标服务循环退出")

    def _is_port_available(self, port):
        """检查端口是否可用"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(('localhost', port))
                return True
        except OSError:
            return False

    def _find_available_port(self):
        """查找可用端口"""
        for port in range(9967, 9999):
            if self._is_port_available(port):
                return port
        return settings.monitoring.prometheus_port

    async def _handle_metrics_request(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        try:
            with suppress(asyncio.IncompleteReadError):
                await reader.readuntil(b"\r\n\r\n")
        except asyncio.LimitOverrunError:
            logger.warning("Metrics request header too large")

        body = generate_latest()
        response = (
            b"HTTP/1.1 200 OK\r\n"
            + f"Content-Type: {CONTENT_TYPE_LATEST}\r\n".encode()
            + f"Content-Length: {len(body)}\r\n".encode()
            + b"Connection: close\r\n\r\n"
            + body
        )
        writer.write(response)
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    async def _run_alerting(self):
        setup_alerting()
        logger.info("监控告警循环启动，间隔 %s 秒", self._interval)
        while not self._alert_shutdown.is_set():
            await self._execute_check(check_cpu_usage, "cpu", settings.monitoring.cpu_threshold)
            await self._execute_check(check_memory_usage, "memory", settings.monitoring.memory_threshold)

            try:
                await asyncio.wait_for(self._alert_shutdown.wait(), timeout=self._interval)
            except asyncio.TimeoutError:
                continue

        logger.info("监控告警循环已停止")

    async def _execute_check(self, func: Callable[[int], float], label: str, threshold: int) -> None:
        try:
            await asyncio.wait_for(asyncio.to_thread(func, threshold), timeout=self._check_timeout)
        except asyncio.TimeoutError:
            record_monitoring_error("timeout")
            logger.error("%s 检查在 %s 秒内未完成", label, self._check_timeout)
        except Exception as exc:
            record_monitoring_error("check_failure")
            logger.error("%s 检查失败: %s", label, exc)

    async def shutdown(self):
        logger.info("正在关闭监控模块...")
        self._alert_shutdown.set()
        self.running = False

        if self.alert_task:
            self.alert_task.cancel()
            with suppress(asyncio.CancelledError):
                await self.alert_task
        self.alert_task = None

        if self._metrics_server:
            self._metrics_server.close()
            await self._metrics_server.wait_closed()
            self._metrics_server = None

        if self._metrics_task:
            self._metrics_task.cancel()
            with suppress(asyncio.CancelledError):
                await self._metrics_task
        self._metrics_task = None

        logger.info("监控模块已关闭")


monitoring_center = MonitoringCenter()
