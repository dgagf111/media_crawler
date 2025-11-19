import re
from importlib.metadata import version, PackageNotFoundError

"""
这个脚本用于自动生成 requirements.txt 文件。
它可以从用户输入的 pip 安装命令中提取包名，并获取已安装的包版本。

使用方法：
1. 在脚本底部的 user_input 变量中输入 pip 安装命令。
2. 运行脚本：python update_requirements.py
3. 脚本将在当前目录生成或更新 requirements.txt 文件。

特性：
- 支持处理多行 pip 安装命令
- 可以处理一行中包含多个包名的情况
- 自动获取已安装包的版本
- 生成符合 pip 要求格式的 requirements.txt 文件

注意事项：
- 生成的 requirements.txt 文件会包含具体的版本号，有助于保持环境一致性
- 如果某个包未安装，脚本会跳过该包，不会将其添加到 requirements 中
- 每次运行脚本都会覆盖现有的 requirements.txt 文件，请注意备份
- 脚本不会自动解析包的依赖关系，只会包含明确指定的包
- 生成的 requirements 基于当前 Python 环境中已安装的包版本
- 在正式环境中，建议仔细审查生成的 requirements.txt 文件，确保所有必要的依赖都已包含，并且版本兼容
"""

def get_installed_version(package):
    """
    获取已安装包的版本。
    
    参数：
    package (str): 包名

    返回：
    str: 包的版本号，如果包未安装则返回 None
    """
    try:
        return version(package)
    except PackageNotFoundError:
        return None

def process_pip_commands(input_commands):
    """
    处理 pip 安装命令，提取包名并获取版本。

    参数：
    input_commands (str): 包含多行 pip 安装命令的字符串

    返回：
    str: 格式化的 requirements 字符串，每行一个包
    """
    requirements = []
    for command in input_commands.split('\n'):
        match = re.search(r'pip install\s+(.+)', command.strip())
        if match:
            packages = match.group(1).split()
            for package in packages:
                version = get_installed_version(package)
                if version:
                    requirements.append(f"{package}=={version}")
    
    return '\n'.join(requirements)

def write_requirements(requirements, filename='requirements.txt'):
    """
    将 requirements 写入文件。

    参数：
    requirements (str): 格式化的 requirements 字符串
    filename (str): 输出文件名，默认为 'requirements.txt'
    """
    with open(filename, 'w') as f:
        f.write(requirements)

# 用户输入
user_input = """
pip install pyyaml
pip install sqlalchemy
pip install pyyaml python-dotenv
pip install mysql-connector-python
pip install pytest
pip install pymysql
pip install apscheduler
pip install cachetools redis
pip install prometheus_client psutil
pip install requests
pip install alembic
pip install fastapi uvicorn
pip install httpx
pip install pipreqs
pip install setuptools
pip install openpyxl
pip install python-jose cryptography passlib bcrypt
pip install python-multipart
pip install pytest-mock
"""

# 处理用户输入并生成 requirements
requirements = process_pip_commands(user_input)

# 将 requirements 写入文件
write_requirements(requirements)

print("requirements.txt 文件已更新。")
