import psutil

from pythonprojecttemplate.log.logHelper import get_logger

logger = get_logger()


def check_cpu_usage(threshold: int = 80) -> float:
    cpu_usage = psutil.cpu_percent(interval=0)
    if cpu_usage > threshold:
        logger.warning("CPU 使用率过高: %s%%", cpu_usage)
    return cpu_usage


def check_memory_usage(threshold: int = 80) -> float:
    memory_usage = psutil.virtual_memory().percent
    if memory_usage > threshold:
        logger.warning("内存使用率过高: %s%%", memory_usage)
    return memory_usage


def setup_alerting():
    logger.info("设置报警系统...")
    check_cpu_usage()
    check_memory_usage()
