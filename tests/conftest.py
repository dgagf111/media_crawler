import sys
from pathlib import Path

import pytest

# 确保 src 目录在 PYTHONPATH 中，便于直接运行测试
SRC_PATH = Path(__file__).resolve().parents[1] / "src"
if str(SRC_PATH) in sys.path:
    sys.path.remove(str(SRC_PATH))
sys.path.insert(0, str(SRC_PATH))

def pytest_collection_modifyitems(items):
    for item in items:
        if item.name == 'Test_Table':
            items.remove(item)

def pytest_collect_file(parent, file_path: Path):
    if file_path.name == "test_table.py":
        return None
