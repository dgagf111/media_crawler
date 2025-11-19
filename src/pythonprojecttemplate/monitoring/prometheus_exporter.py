from prometheus_client import Counter, Gauge, Histogram
import psutil

# 定义一些示例指标
REQUEST_COUNT = Counter('app_requests_total', 'Total app HTTP requests')
RESPONSE_TIME = Histogram('app_response_latency_seconds', 'Response latency in seconds')
CPU_USAGE = Gauge('system_cpu_usage', 'Current CPU usage')
MEMORY_USAGE = Gauge('system_memory_usage', 'Current memory usage')
MONITORING_ERRORS = Counter('monitoring_errors_total', 'Total monitoring loop errors', ['reason'])

def setup_metrics():
    MONITORING_ERRORS.labels(reason="server_error").inc(0)
    MONITORING_ERRORS.labels(reason="check_failure").inc(0)
    MONITORING_ERRORS.labels(reason="timeout").inc(0)

def record_request():
    REQUEST_COUNT.inc()

def record_response_time(latency):
    RESPONSE_TIME.observe(latency)

def update_system_metrics():
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.virtual_memory().percent)


def record_monitoring_error(reason: str) -> None:
    MONITORING_ERRORS.labels(reason=reason).inc()
