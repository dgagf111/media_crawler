import pytest
import os
import shutil
from datetime import datetime
from pythonprojecttemplate.log.logHelper import LogHelper, get_logger

# 测试开始和结束的钩子函数
def pytest_sessionstart(session):
    print("\n========== 日志测试开始 ==========")

def pytest_sessionfinish(session, exitstatus):
    print("\n========== 日志测试结束 ==========")

@pytest.fixture(scope="module")
def test_logger():
    print("\n----- 设置测试环境 -----")
    test_project_name = "TestProject"
    test_log_dir = "./test_logs"
    logger = LogHelper(project_name=test_project_name, base_log_directory=test_log_dir, log_level="DEBUG")
    yield logger
    print("\n----- 清理测试环境 -----")
    if os.path.exists(test_log_dir):
        shutil.rmtree(test_log_dir)

def test_log_file_creation(test_logger):
    print("\n测试日志文件创建")
    test_logger.info("测试日志信息")
    current_date = datetime.now()
    year, month, day = current_date.strftime('%Y'), current_date.strftime('%Y-%m'), current_date.strftime('%Y-%m-%d')
    expected_log_path = os.path.join(test_logger.base_log_directory, test_logger.project_name, year, month, f"{day}.log")
    assert os.path.exists(expected_log_path), "日志文件未被创建"

def test_log_levels(test_logger):
    print("\n测试不同日志级别")
    test_messages = {
        "debug": "这是一条调试日志",
        "info": "这是一条信息日志",
        "warning": "这是一条警告日志",
        "error": "这是一条错误日志",
        "critical": "这是一条严重错误日志"
    }

    for level, message in test_messages.items():
        getattr(test_logger, level)(message)

    current_date = datetime.now()
    year, month, day = current_date.strftime('%Y'), current_date.strftime('%Y-%m'), current_date.strftime('%Y-%m-%d')
    log_path = os.path.join(test_logger.base_log_directory, test_logger.project_name, year, month, f"{day}.log")

    with open(log_path, 'r', encoding='utf-8') as log_file:
        content = log_file.read()
        for message in test_messages.values():
            assert message in content, f"日志消息 '{message}' 未在日志文件中找到"

def test_singleton():
    print("\n测试单例模式")
    logger1 = get_logger()
    logger2 = get_logger()
    assert logger1 is logger2, "get_logger() 没有返回相同的实例"

if __name__ == "__main__":
    pytest.main([__file__, '-v'])
