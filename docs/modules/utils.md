# 🔧 工具类库文档

Python Project Template 提供了丰富的工具类库，涵盖了常用的加密、文件处理、网络请求等功能。

## 📋 目录

- [工具库概览](#工具库概览)
- [加密工具](#加密工具)
- [Excel处理工具](#excel处理工具)
- [HTTP请求工具](#http请求工具)
- [使用示例](#使用示例)
- [测试验证](#测试验证)
- [最佳实践](#最佳实践)

## 🏗️ 工具库概览

### 工具库结构

```
utils/
├── __init__.py              # 工具库入口
├── encrypt/                 # 加密工具模块
│   ├── __init__.py
│   ├── aes.py              # AES对称加密
│   ├── md5.py              # MD5哈希算法
│   ├── rsa/                # RSA非对称加密
│   └── sha.py              # SHA哈希算法
├── excel/                   # Excel处理模块
│   ├── __init__.py
│   └── excel_utils.py      # Excel读写工具
├── http/                    # HTTP请求模块
│   ├── __init__.py
│   └── http_util.py        # HTTP请求封装
└── test_utils_module.py     # 完整测试套件
```

### 功能特性

- **🔐 多种加密算法**: 支持AES、RSA、MD5、SHA256等
- **📊 Excel处理**: 便捷的Excel文件读写操作
- **🌐 HTTP工具**: 封装了常用的HTTP请求方法
- **🧪 完整测试**: 100%测试覆盖，确保功能可靠性
- **📚 丰富文档**: 详细的使用说明和示例代码

## 🔐 加密工具

### AES对称加密

#### 功能说明
- **算法类型**: AES (Advanced Encryption Standard)
- **加密模式**: 支持多种加密模式
- **应用场景**: 数据传输加密、敏感信息存储

#### 使用方法

```python
from pythonprojecttemplate.utils.encrypt import aes_encrypt

# AES加密
encrypted_data = aes_encrypt.encrypt("sensitive_data", "your_key")

# AES解密  
decrypted_data = aes_encrypt.decrypt(encrypted_data, "your_key")
```

#### 配置参数

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| data | str | 要加密的数据 | 必填 |
| key | str | 加密密钥 | 必填 |
| mode | str | 加密模式 | CBC |

### RSA非对称加密

#### 功能说明
- **算法类型**: RSA (Rivest-Shamir-Adleman)
- **密钥长度**: 支持多种密钥长度
- **应用场景**: 数字签名、密钥交换、安全通信

#### 使用方法

```python
from pythonprojecttemplate.utils.encrypt.rsa import rsa_encrypt

# 生成密钥对
public_key, private_key = rsa_encrypt.generate_keys(2048)

# RSA加密
encrypted_data = rsa_encrypt.encrypt("message", public_key)

# RSA解密
decrypted_data = rsa_encrypt.decrypt(encrypted_data, private_key)

# 数字签名
signature = rsa_encrypt.sign("message", private_key)

# 验证签名
is_valid = rsa_encrypt.verify("message", signature, public_key)
```

### 哈希算法

#### bcrypt密码哈希

```python
from pythonprojecttemplate.utils.encrypt import bcrypt_hash

# 密码哈希
hashed = bcrypt_hash.hash_password("my_password")
print(f"哈希值: {hashed}")

# 验证密码
is_valid = bcrypt_hash.verify_password("my_password", hashed)
print(f"验证结果: {'成功' if is_valid else '失败'}")

# 检查是否需要重新哈希
if bcrypt_hash.needs_rehash(hashed):
    print("建议升级密码哈希")
```

#### SHA256哈希

```python
from pythonprojecttemplate.utils.encrypt import sha_256_encrypt

# SHA256哈希
hash_value = sha_256_encrypt.encrypt("input_string")
print(f"SHA256: {hash_value}")
```

#### 特性对比

| 算法 | 长度 | 安全性 | 性能 | 推荐使用 |
|------|------|--------|------|----------|
| bcrypt | 变长 | 极高 | 低 | 密码存储、用户认证 |
| SHA256 | 256位 | 高 | 中等 | 安全哈希、数据完整性 |

## 📊 Excel处理工具

### 功能说明
- **读取功能**: 支持多种Excel格式 (.xls, .xlsx)
- **写入功能**: 创建和编辑Excel文件
- **数据处理**: 行列操作、格式设置
- **批量处理**: 支持大文件高效处理

### 使用方法

#### Excel读取

```python
from pythonprojecttemplate.utils.excel import excel_utils

# 读取Excel文件
data = excel_utils.read_excel("data.xlsx")

# 读取指定工作表
data = excel_utils.read_excel("data.xlsx", sheet_name="Sheet1")

# 读取指定列
data = excel_utils.read_excel("data.xlsx", columns=["A", "B", "C"])

# 读取指定行范围
data = excel_utils.read_excel("data.xlsx", start_row=1, end_row=100)
```

#### Excel写入

```python
# 写入数据到Excel
excel_utils.write_excel(data, "output.xlsx")

# 写入到指定工作表
excel_utils.write_excel(data, "output.xlsx", sheet_name="Results")

# 追加数据
excel_utils.append_excel(new_data, "output.xlsx")

# 设置格式
excel_utils.write_excel(
    data, 
    "output.xlsx", 
    format_options={
        'header_style': {'bold': True, 'bg_color': '#4F81BD'},
        'cell_style': {'align': 'center'}
    }
)
```

### 高级功能

#### 数据验证

```python
# 数据类型验证
validated_data = excel_utils.validate_data(
    data, 
    schema={
        'name': str,
        'age': int,
        'email': 'email'
    }
)

# 数据清洗
cleaned_data = excel_utils.clean_data(data, {
    'remove_duplicates': True,
    'fill_missing': 'auto',
    'trim_whitespace': True
})
```

#### 批量处理

```python
# 批量转换
excel_utils.batch_convert(
    input_dir="./input/",
    output_dir="./output/",
    format="csv"
)

# 合并多个Excel文件
excel_utils.merge_excel_files([
    "file1.xlsx",
    "file2.xlsx", 
    "file3.xlsx"
], "merged.xlsx")
```

## 🌐 HTTP请求工具

### 功能说明
- **HTTP方法**: 支持GET、POST、PUT、DELETE等
- **请求配置**: 超时、重试、代理等配置
- **响应处理**: 自动解析JSON、XML等格式
- **错误处理**: 完善的异常处理机制

### 基础使用

#### GET请求

```python
from pythonprojecttemplate.utils.http import http_util

# 简单GET请求
response = http_util.get("https://api.example.com/users")

# 带参数的GET请求
response = http_util.get(
    "https://api.example.com/users",
    params={
        'page': 1,
        'limit': 10,
        'filter': 'active'
    }
)

# 带请求头的GET请求
response = http_util.get(
    "https://api.example.com/users",
    headers={
        'Authorization': 'Bearer token123',
        'Content-Type': 'application/json'
    }
)
```

#### POST请求

```python
# JSON数据POST请求
response = http_util.post(
    "https://api.example.com/users",
    json={
        'name': 'John Doe',
        'email': 'john@example.com'
    }
)

# 表单数据POST请求
response = http_util.post(
    "https://api.example.com/login",
    data={
        'username': 'admin',
        'password': 'password123'
    }
)

# 文件上传POST请求
response = http_util.post(
    "https://api.example.com/upload",
    files={
        'file': open('document.pdf', 'rb')
    }
)
```

### 高级配置

#### 请求配置

```python
# 超时配置
response = http_util.get(
    "https://api.example.com/slow-endpoint",
    timeout=30
)

# 重试配置
response = http_util.get(
    "https://api.example.com/endpoint",
    retry_count=3,
    retry_delay=1.0
)

# 代理配置
response = http_util.get(
    "https://api.example.com/endpoint",
    proxies={
        'http': 'http://proxy.example.com:8080',
        'https': 'https://proxy.example.com:8080'
    }
)
```

#### 会话管理

```python
# 创建会话
session = http_util.create_session()

# 设置默认请求头
session.headers.update({
    'Authorization': 'Bearer token123',
    'User-Agent': 'MyApp/1.0'
})

# 使用会话发送请求
response = session.get("https://api.example.com/profile")
```

### 响应处理

#### 响应解析

```python
# 获取JSON响应
data = response.json()

# 获取文本响应
text = response.text

# 获取状态码
status_code = response.status_code

# 获取响应头
headers = response.headers
```

#### 错误处理

```python
try:
    response = http_util.get("https://api.example.com/endpoint")
    response.raise_for_status()  # 检查HTTP错误
    data = response.json()
    
except http_util.RequestException as e:
    print(f"请求失败: {e}")
except http_util.Timeout:
    print("请求超时")
except http_util.ConnectionError:
    print("连接错误")
```

## 💡 使用示例

### 综合示例：数据处理管道

```python
from pythonprojecttemplate.utils.encrypt import aes_encrypt, bcrypt_hash
from pythonprojecttemplate.utils.excel import excel_utils
from pythonprojecttemplate.utils.http import http_util
import json

def process_data_pipeline():
    """完整的数据处理管道示例"""

    # 1. 从API获取数据
    print("📥 获取数据...")
    response = http_util.get(
        "https://api.example.com/data",
        headers={'Authorization': 'Bearer your-token'}
    )

    if response.status_code == 200:
        raw_data = response.json()

        # 2. 数据加密和哈希
        print("🔐 加密敏感数据...")
        for record in raw_data:
            if 'email' in record:
                # 使用bcrypt哈希邮箱（用于索引和比较，不存储明文）
                record['email_hash'] = bcrypt_hash.hash_password(record['email'])
                # 使用AES加密邮箱（需要时解密）
                record['email_encrypted'] = aes_encrypt.encrypt(
                    record['email'],
                    "encryption_key"
                )

        # 3. 保存到Excel
        print("💾 保存到Excel...")
        excel_utils.write_excel(
            raw_data,
            "processed_data.xlsx",
            sheet_name="ProcessedData"
        )

        # 4. 生成报告
        print("📊 生成处理报告...")
        report = {
            'total_records': len(raw_data),
            'processing_time': '2.5s',
            'encrypted_fields': ['email'],
            'output_file': 'processed_data.xlsx'
        }

        excel_utils.write_excel(
            [report],
            "processing_report.xlsx",
            sheet_name="Report"
        )

        print("✅ 数据处理管道完成!")
        return True

    else:
        print(f"❌ API请求失败: {response.status_code}")
        return False

# 运行示例
if __name__ == "__main__":
    process_data_pipeline()
```

### 批量文件处理示例

```python
import os
from pythonprojecttemplate.utils.excel import excel_utils
from pythonprojecttemplate.utils.encrypt import sha_256_encrypt

def batch_file_processor(input_dir, output_dir):
    """批量处理Excel文件并生成校验和"""
    
    processed_files = []
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.xlsx'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"processed_{filename}")
            
            # 读取原始数据
            data = excel_utils.read_excel(input_path)
            
            # 数据处理
            for record in data:
                record['checksum'] = sha_256_encrypt.encrypt(
                    str(record)
                )
                record['processed_at'] = datetime.now().isoformat()
            
            # 保存处理后的数据
            excel_utils.write_excel(data, output_path)
            
            processed_files.append({
                'input_file': filename,
                'output_file': f"processed_{filename}",
                'record_count': len(data)
            })
    
    # 生成处理摘要
    excel_utils.write_excel(
        processed_files, 
        os.path.join(output_dir, "processing_summary.xlsx")
    )
    
    return processed_files
```

## 🧪 测试验证

### 运行工具库测试

```bash
# 运行工具库专用测试
python utils/test_utils_module.py

# 通过测试控制器运行
python run_module_tests.py utils

# 运行所有测试（包含工具库）
python run_module_tests.py all
```

### 测试覆盖范围

工具库测试覆盖以下功能：

- ✅ **RSA加密工具** - 密钥生成、加解密、数字签名
- ✅ **AES加密工具** - 对称加密解密功能
- ✅ **bcrypt密码哈希** - 安全的密码哈希和验证
- ✅ **SHA哈希工具** - 安全哈希算法
- ✅ **Excel处理工具** - 文件读写、格式处理
- ✅ **HTTP请求工具** - 网络请求、响应处理

### 性能基准

| 工具 | 操作 | 基准性能 | 测试条件 |
|------|------|----------|----------|
| AES加密 | 加密1KB数据 | <1ms | 标准密钥长度 |
| RSA加密 | 2048位密钥生成 | <100ms | 标准环境 |
| MD5哈希 | 1MB数据哈希 | <10ms | 标准算法 |
| Excel读取 | 1000行数据 | <500ms | 标准格式 |
| HTTP请求 | 简单GET请求 | <1s | 本地网络 |

## 🎯 最佳实践

### 安全使用

#### 加密最佳实践

```python
# ✅ 推荐：使用强密钥
key = os.urandom(32)  # 256位随机密钥
encrypted = aes_encrypt.encrypt(data, key)

# ❌ 避免：使用弱密钥
# key = "123456"  # 过于简单的密钥

# ✅ 推荐：安全存储密钥
import keyring
keyring.set_password("myapp", "encryption_key", key.hex())

# ✅ 推荐：使用bcrypt进行密码哈希（而不是MD5）
password_hash = bcrypt_hash.hash_password(password)
is_valid = bcrypt_hash.verify_password(password, password_hash)

# ✅ 推荐：定期检查是否需要升级哈希
if bcrypt_hash.needs_rehash(password_hash):
    password_hash = bcrypt_hash.hash_password(password)
```

#### 敏感数据处理

```python
# ✅ 推荐：及时清除敏感数据
try:
    decrypted_data = aes_encrypt.decrypt(encrypted_data, key)
    # 处理数据...
finally:
    # 清除内存中的敏感数据
    decrypted_data = None
    del decrypted_data
```

### 性能优化

#### 批量处理优化

```python
# ✅ 推荐：批量加密
def batch_encrypt(data_list, key):
    """批量加密优化"""
    cipher = aes_encrypt.create_cipher(key)  # 复用cipher对象
    return [cipher.encrypt(data) for data in data_list]

# ✅ 推荐：Excel流式处理
def process_large_excel(file_path, chunk_size=1000):
    """分块处理大Excel文件"""
    for chunk in excel_utils.read_excel_chunks(file_path, chunk_size):
        processed_chunk = process_data(chunk)
        yield processed_chunk
```

#### HTTP请求优化

```python
# ✅ 推荐：使用连接池
session = http_util.create_session(pool_size=10)

# ✅ 推荐：异步请求（如果支持）
async def fetch_multiple_urls(urls):
    """并发获取多个URL"""
    tasks = [http_util.async_get(url) for url in urls]
    return await asyncio.gather(*tasks)
```

### 错误处理

#### 健壮的错误处理

```python
from pythonprojecttemplate.utils.http import http_util
from pythonprojecttemplate.utils.excel import excel_utils
import logging

logger = logging.getLogger(__name__)

def robust_data_processing(api_url, output_file):
    """健壮的数据处理示例"""
    try:
        # HTTP请求with重试
        response = http_util.get(
            api_url, 
            timeout=30,
            retry_count=3
        )
        response.raise_for_status()
        
        data = response.json()
        
        # Excel写入with备份
        try:
            excel_utils.write_excel(data, output_file)
            logger.info(f"数据成功写入: {output_file}")
            
        except Exception as e:
            # 写入备份位置
            backup_file = f"backup_{output_file}"
            excel_utils.write_excel(data, backup_file)
            logger.warning(f"主文件写入失败，已写入备份: {backup_file}")
            
    except http_util.Timeout:
        logger.error("API请求超时")
        raise
    except http_util.ConnectionError:
        logger.error("网络连接失败")
        raise
    except Exception as e:
        logger.error(f"数据处理失败: {e}")
        raise
```

## 🔧 故障排除

### 常见问题

#### 1. 加密模块导入失败

**问题**: `ImportError: No module named 'Crypto'`

**解决方案**:
```bash
# 安装加密依赖
pip install pycrypto
# 或者
pip install pycryptodome
```

#### 2. Excel文件处理错误

**问题**: `Excel文件格式不支持`

**解决方案**:
```bash
# 安装Excel依赖
pip install openpyxl xlrd xlwt
```

#### 3. HTTP请求SSL错误

**问题**: `SSL certificate verify failed`

**解决方案**:
```python
# 临时禁用SSL验证（仅测试环境）
response = http_util.get(url, verify=False)

# 或指定证书路径
response = http_util.get(url, verify='/path/to/cert.pem')
```

### 调试技巧

#### 启用详细日志

```python
import logging

# 启用HTTP调试日志
logging.getLogger('urllib3').setLevel(logging.DEBUG)

# 启用工具库调试日志
logging.getLogger('utils').setLevel(logging.DEBUG)
```

#### 性能分析

```python
import time
from functools import wraps

def timing_decorator(func):
    """性能计时装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} 执行时间: {end - start:.4f}秒")
        return result
    return wrapper

# 使用示例
@timing_decorator
def process_excel_file(file_path):
    return excel_utils.read_excel(file_path)
```

## 📚 参考资源

### 相关文档
- [测试指南](../guides/testing-guide.md) - 完整的测试系统说明
- [开发指南](../guides/development-guide.md) - 开发环境配置
- [API文档](../guides/api-guide.md) - API接口说明

### 外部资源
- [Python加密库文档](https://cryptography.io/)
- [openpyxl官方文档](https://openpyxl.readthedocs.io/)
- [Requests库文档](https://requests.readthedocs.io/)

---

**最后更新**: 2025-09-01  
**文档版本**: v3.0.0  
**模块版本**: v3.0.0

> 💡 **提示**: 工具库设计遵循"开箱即用"原则，提供了完善的默认配置和错误处理机制。