# 🚀 部署指南

Python Project Template 生产环境部署完整指南。

## 📋 目录

- [部署概览](#部署概览)
- [环境准备](#环境准备)
- [Docker部署](#docker部署)
- [传统部署](#传统部署)
- [配置管理](#配置管理)
- [监控配置](#监控配置)
- [安全配置](#安全配置)
- [故障排除](#故障排除)

## 🏗️ 部署概览

### 系统要求

| 组件 | 最低配置 | 推荐配置 |
|------|----------|----------|
| CPU | 2核 | 4核+ |
| 内存 | 4GB | 8GB+ |
| 存储 | 20GB | 50GB+ SSD |
| 网络 | 100Mbps | 1Gbps+ |

### 依赖服务

- **Python**: 3.12+
- **数据库**: MySQL 8.0
- **缓存**: Redis 7.0
- **Web服务器**: Nginx
- **容器**: Docker + Docker Compose

## 🛠️ 环境准备

### 系统依赖安装

#### Ubuntu/Debian

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装基础依赖
sudo apt install -y python3.12 python3.12-pip python3.12-dev
sudo apt install -y git curl wget nginx mysql-server redis-server

# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 安装Docker Compose
sudo pip3 install docker-compose
```

#### CentOS/RHEL

```bash
# 更新系统
sudo yum update -y

# 安装基础依赖
sudo yum install -y python3.12 python3.12-pip python3.12-dev
sudo yum install -y git curl wget nginx mysql-server redis

# 安装Docker
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install -y docker-ce docker-ce-cli containerd.io

# 启动服务
sudo systemctl enable --now docker nginx mysql redis
```

### 环境变量配置

```bash
# 创建生产环境配置
sudo mkdir -p /etc/pythonapp
sudo tee /etc/pythonapp/production.env << 'EOF'
# 应用配置
ENV=production
DEBUG=false
PPT_SECURITY__TOKEN__SECRET_KEY=your-super-secret-key-here
PPT_API__HOST=0.0.0.0
PPT_API__PORT=8000

# 数据库配置
PPT_DATABASE__HOST=localhost
PPT_DATABASE__PORT=3306
PPT_DATABASE__USERNAME=app_user
PPT_DATABASE__PASSWORD=secure_password_here
PPT_DATABASE__DATABASE=production_db

# Redis配置
PPT_CACHE__REDIS__HOST=localhost
PPT_CACHE__REDIS__PORT=6379
PPT_CACHE__REDIS__DB=0
PPT_SECURITY__REVOCATION__BACKEND=redis
PPT_SECURITY__REVOCATION__REDIS__HOST=localhost
PPT_SECURITY__REVOCATION__REDIS__PORT=6379
PPT_SECURITY__REVOCATION__REDIS__PASSWORD=redis_password_here

# （可选）为了兼容现有docker-compose模板中对MySQL/Redis容器的引用，保留旧变量
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USERNAME=app_user
MYSQL_PASSWORD=secure_password_here
MYSQL_DATABASE=production_db
REDIS_PASSWORD=redis_password_here

# 日志配置
PPT_LOGGING__LOG_LEVEL=INFO
PPT_LOGGING__BASE_LOG_DIRECTORY=/var/log/pythonapp

# 监控配置
PPT_MONITORING__PROMETHEUS_PORT=9966
PPT_MONITORING__CPU_THRESHOLD=70
PPT_MONITORING__MEMORY_THRESHOLD=70
EOF

# 设置权限
sudo chmod 600 /etc/pythonapp/production.env
```

## 📦 Docker部署

### Dockerfile

```dockerfile
FROM python:3.12-slim

# 创建应用用户
RUN groupadd -r appuser && useradd -r -g appuser appuser

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc g++ \
    && rm -rf /var/lib/apt/lists/*

# 复制并安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY --chown=appuser:appuser . .

# 创建必要的目录
RUN mkdir -p logs data && \
    chown -R appuser:appuser logs data

# 设置环境变量
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 切换到应用用户
USER appuser

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# 暴露端口
EXPOSE 8000 9966

# 启动应用
CMD ["python", "main.py"]
```

### Docker Compose配置

```yaml
# docker-compose.production.yml
version: '3.8'

services:
  app:
    build: .
    image: pythonapp:latest
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G
    networks:
      - app-network
    env_file:
      - /etc/pythonapp/production.env
    volumes:
      - /var/log/pythonapp:/app/logs
      - /var/data/pythonapp:/app/data
    depends_on:
      - mysql
      - redis
    ports:
      - "8000-8002:8000"

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USERNAME}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    volumes:
      - mysql-data:/var/lib/mysql
    networks:
      - app-network
    ports:
      - "3306:3306"

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis-data:/data
    networks:
      - app-network
    ports:
      - "6379:6379"

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    networks:
      - app-network
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - app

volumes:
  mysql-data:
  redis-data:

networks:
  app-network:
    driver: bridge
```

### 部署命令

```bash
# 构建并启动服务
docker-compose -f docker-compose.production.yml up -d --build

# 查看服务状态
docker-compose -f docker-compose.production.yml ps

# 查看日志
docker-compose -f docker-compose.production.yml logs -f app

# 扩展服务
docker-compose -f docker-compose.production.yml up -d --scale app=5

# 停止服务
docker-compose -f docker-compose.production.yml down
```

## 🖥️ 传统部署

### 系统服务配置

```ini
# /etc/systemd/system/pythonapp.service
[Unit]
Description=Python Project Template Application
After=network.target mysql.service redis.service

[Service]
Type=forking
User=appuser
Group=appuser
WorkingDirectory=/opt/pythonapp
EnvironmentFile=/etc/pythonapp/production.env
ExecStart=/opt/pythonapp/.venv/bin/python main.py --daemon
ExecReload=/bin/kill -HUP $MAINPID
ExecStop=/bin/kill -TERM $MAINPID
Restart=always
RestartSec=5

# 安全配置
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=/var/log/pythonapp /var/data/pythonapp

# 资源限制
LimitNOFILE=65536
MemoryMax=4G
CPUQuota=200%

[Install]
WantedBy=multi-user.target
```

### 部署脚本

```bash
#!/bin/bash
# deploy.sh - 应用部署脚本

set -e

APP_NAME="pythonapp"
APP_DIR="/opt/$APP_NAME"
REPO_URL="https://github.com/your-username/pythonProjectTemplate.git"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# 1. 停止服务
log "停止应用服务..."
systemctl stop $APP_NAME || true

# 2. 更新代码
log "更新应用代码..."
if [ -d "$APP_DIR/.git" ]; then
    cd "$APP_DIR"
    git pull origin main
else
    git clone "$REPO_URL" "$APP_DIR"
    cd "$APP_DIR"
fi

# 3. 安装依赖
log "安装依赖..."
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 4. 运行测试
log "运行测试..."
python run_module_tests.py all

# 5. 数据库迁移
log "数据库迁移..."
python -m alembic upgrade head

# 6. 设置权限
log "设置权限..."
chown -R appuser:appuser "$APP_DIR"
mkdir -p /var/log/$APP_NAME /var/data/$APP_NAME
chown -R appuser:appuser /var/log/$APP_NAME /var/data/$APP_NAME

# 7. 启动服务
log "启动服务..."
systemctl daemon-reload
systemctl enable $APP_NAME
systemctl start $APP_NAME

# 8. 健康检查
log "健康检查..."
sleep 10
curl -f http://localhost:8000/health || exit 1

log "部署完成！"
```

## ⚙️ 配置管理

### Nginx配置

```nginx
# /etc/nginx/sites-available/pythonapp
upstream pythonapp_backend {
    least_conn;
    server localhost:8000 max_fails=3 fail_timeout=30s;
    server localhost:8001 max_fails=3 fail_timeout=30s;
    server localhost:8002 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    # SSL配置
    ssl_certificate /etc/ssl/certs/yourdomain.com.crt;
    ssl_certificate_key /etc/ssl/private/yourdomain.com.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    
    # 安全头
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    
    # 代理配置
    location / {
        proxy_pass http://pythonapp_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        proxy_connect_timeout 30s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # 健康检查
    location /health {
        proxy_pass http://pythonapp_backend/health;
        access_log off;
    }
    
    # 监控接口（仅内网）
    location /metrics {
        proxy_pass http://localhost:9966/metrics;
        allow 10.0.0.0/8;
        deny all;
    }
}
```

### 生产环境配置

```yaml
# config/production.yaml
database:
  host: ${PPT_DATABASE__HOST}
  port: ${PPT_DATABASE__PORT}
  username: ${PPT_DATABASE__USERNAME}
  password: ${PPT_DATABASE__PASSWORD}
  database: ${PPT_DATABASE__DATABASE}
  pool_size: 20

api:
  host: ${PPT_API__HOST}
  port: ${PPT_API__PORT}
  workers: 4

security:
  token:
    secret_key: ${PPT_SECURITY__TOKEN__SECRET_KEY}
    algorithm: HS256
  revocation:
    backend: ${PPT_SECURITY__REVOCATION__BACKEND:-redis}
    redis:
      host: ${PPT_SECURITY__REVOCATION__REDIS__HOST}
      port: ${PPT_SECURITY__REVOCATION__REDIS__PORT}
      password: ${PPT_SECURITY__REVOCATION__REDIS__PASSWORD}

cache:
  type: redis
  redis:
    host: ${PPT_CACHE__REDIS__HOST}
    port: ${PPT_CACHE__REDIS__PORT}
    db: ${PPT_CACHE__REDIS__DB}

log:
  level: ${PPT_LOGGING__LOG_LEVEL}
  format: structured
  console_output: false
  file_output: true
  log_dir: ${PPT_LOGGING__BASE_LOG_DIRECTORY}

monitoring:
  prometheus_port: ${PPT_MONITORING__PROMETHEUS_PORT}
  cpu_threshold: ${PPT_MONITORING__CPU_THRESHOLD}
  memory_threshold: ${PPT_MONITORING__MEMORY_THRESHOLD}
```

## 📊 监控配置

### Prometheus配置

```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'pythonapp'
    static_configs:
      - targets: ['localhost:9966']
    scrape_interval: 10s
    
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['localhost:9100']
```

### 告警规则

```yaml
# monitoring/alerts.yml
groups:
  - name: app-alerts
    rules:
      - alert: HighResponseTime
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "应用响应时间过高"
      
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "应用错误率过高"
```

## 🔒 安全配置

### SSL证书配置

```bash
# 使用Let's Encrypt获取免费SSL证书
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d yourdomain.com

# 自动续期
sudo crontab -e
# 添加: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 防火墙配置

```bash
# 配置UFW防火墙
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 允许必要端口
sudo ufw allow 22      # SSH
sudo ufw allow 80      # HTTP
sudo ufw allow 443     # HTTPS

# 限制内网访问
sudo ufw allow from 10.0.0.0/8 to any port 3306    # MySQL
sudo ufw allow from 10.0.0.0/8 to any port 6379    # Redis

sudo ufw enable
```

### SSH安全

```bash
# 编辑SSH配置
sudo nano /etc/ssh/sshd_config

# 推荐设置
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3

sudo systemctl restart sshd
```

## 🔧 故障排除

### 常见问题

#### 1. 应用启动失败

```bash
# 检查日志
sudo journalctl -u pythonapp -f

# 检查配置文件
python -c "from config.config import Config; print(Config().get_mysql_config())"

# 检查端口占用
sudo netstat -tulpn | grep :8000
```

#### 2. 数据库连接问题

```bash
# 检查MySQL状态
sudo systemctl status mysql

# 测试连接
mysql -u app_user -p -h localhost production_db

# 检查MySQL配置
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
```

#### 3. Redis连接问题

```bash
# 检查Redis状态
sudo systemctl status redis

# 测试连接
redis-cli -h localhost -p 6379 -a your_password ping

# 检查内存使用
redis-cli info memory
```

#### 4. Nginx配置问题

```bash
# 测试配置
sudo nginx -t

# 重新加载配置
sudo systemctl reload nginx

# 检查访问日志
sudo tail -f /var/log/nginx/access.log
```

### 性能调优

#### 应用优化

```python
# main.py - 生产环境启动优化
import multiprocessing
import uvicorn

def get_workers():
    return min((2 * multiprocessing.cpu_count()) + 1, 8)

if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        workers=get_workers(),
        loop="uvloop",      # 高性能事件循环
        http="httptools"    # 高性能HTTP解析
    )
```

#### 数据库优化

```ini
# /etc/mysql/mysql.conf.d/mysqld.cnf
[mysqld]
max_connections = 1000
innodb_buffer_pool_size = 2G    # 根据内存调整
query_cache_size = 256M
slow_query_log = 1
long_query_time = 2
```

### 备份策略

```bash
#!/bin/bash
# backup.sh - 数据备份脚本

BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# 数据库备份
mysqldump -u root -p production_db > $BACKUP_DIR/db_$DATE.sql

# 应用数据备份
tar -czf $BACKUP_DIR/app_data_$DATE.tar.gz /var/data/pythonapp

# 配置文件备份
cp /etc/pythonapp/production.env $BACKUP_DIR/config_$DATE.env

# 清理旧备份（保留7天）
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

## 📚 参考资源

### 相关文档
- [API指南](api-guide.md) - API接口说明
- [监控系统](../modules/monitoring.md) - 监控配置详情
- [安全配置](../modules/auth.md) - 认证和授权

### 外部资源
- [Docker最佳实践](https://docs.docker.com/develop/best-practices/)
- [Nginx配置指南](https://nginx.org/en/docs/)
- [Let's Encrypt文档](https://letsencrypt.org/docs/)

---

**最后更新**: 2025-09-01  
**文档版本**: v3.0.0  

> 💡 **提示**: 建议在生产环境部署前，先在测试环境完整验证所有配置和流程。
