# 使用官方Python 3.12镜像作为基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器中
COPY . /app

# 安装项目依赖
RUN pip install --no-cache-dir -r dependencies/requirements.txt

# python 不缓存输出
ENV PYTHONUNBUFFERED=1

# 暴露API服务端口
EXPOSE 8000

# 需要设置的环境变量：
# MYSQL_USERNAME
# MYSQL_PASSWORD
# MYSQL_HOST
# MYSQL_PORT
# MYSQL_DATABASE
# REDIS_HOST
# REDIS_PORT
# API_VERSION

# 运行测试，然后启动应用
CMD python tests/run_tests.py framework && python main.py
