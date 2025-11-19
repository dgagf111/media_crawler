"""
注意：这个文件仅用于演示和验证业务测试的执行。
当实际的业务测试代码被添加到这个目录后，可以安全地删除此文件。
此文件的目的是确保业务测试的路径和执行机制正常工作。
"""

import pytest
from pythonprojecttemplate.modules.test.main import run

def test_run_function(caplog):
    """测试 test 模块的 run 函数"""
    # 由于 run 函数记录日志，我们可以捕获日志并验证
    run()

    # 验证日志输出
    assert "测试业务逻辑运行" in caplog.text
    assert "INFO" in caplog.text

def test_example():
    """一个简单的示例测试"""
    assert True

def test_addition():
    """测试简单的加法"""
    assert 1 + 1 == 2

def test_string_manipulation():
    """测试字符串操作"""
    text = "Hello, World!"
    assert text.lower() == "hello, world!"
    assert text.split(", ")[0] == "Hello"

@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
    (5, 25),
])
def test_square(input, expected):
    """参数化测试：测试平方函数"""
    assert input ** 2 == expected
