---
name: refactor-assistant
description: 自动化代码重构建议与实现，识别代码异味、复杂度问题和 SOLID 原则违反。当需要优化代码结构、减少重复代码或提升可维护性时使用。
---

# 重构助手

识别并修复代码异味，自动化重构建议与实现的专家级工具。

## 快速开始

```bash
# 分析单个文件
skill: "refactor-assistant" src/models/user.py

# 分析整个目录
skill: "refactor-assistant" src/

# 专注于特定问题
skill: "refactor-assistant" --focus complexity --suggest-only
```

## 使用说明

作为代码重构专家，按以下步骤执行：

### 1. 代码分析阶段
使用以下工具检查目标代码：

```python
# 检查文件结构和复杂度
files = glob.glob("src/**/*.py")
for file in files:
    content = read_file(file)
    analyze_complexity(content)
```

**检查项目：**
- 代码异味（过长函数、重复代码、臃肿类）
- 复杂度问题（高圈复杂度、深层嵌套）
- 命名不一致和语义模糊
- SOLID 原则违反
- 性能瓶颈和安全隐患

### 2. 模式识别阶段
识别以下重构模式的应用机会：

**结构模式：**
- Extract Method/Function（提取方法/函数）
- Extract Class/Module（提取类/模块）
- Extract Interface（提取接口）
- Move Method/Field（移动方法/字段）

**简化模式：**
- Rename Variable/Function/Class（重命名）
- Introduce Parameter Object（引入参数对象）
- Replace Conditional with Polymorphism（多态取代条件）
- Simplify Complex Conditionals（简化复杂条件）

**清理模式：**
- Remove Dead Code（删除无用代码）
- Remove Duplication（去除重复）
- Replace Magic Number with Constant（常量替换魔法数字）

### 3. 建议生成阶段
对每个重构机会提供详细分析：

```
## 重构建议 #1: Extract Method
**位置**: `src/services/user_service.py:45-67`
**问题**: `process_user_data` 函数过长（23行），职责不单一
**影响**: 中等 - 需要更新调用点
**收益**: 提升可读性和可测试性
**风险**: 低 - 纯内部重构
```

### 4. 实施执行阶段
如获批准，按以下顺序执行重构：

1. **准备工作**：确保测试覆盖
2. **逐步重构**：小步快跑，频繁测试
3. **验证结果**：运行完整测试套件
4. **文档更新**：更新相关文档

## 重构优先级

### 🔴 高优先级（立即处理）
- **安全漏洞**：SQL注入、XSS、权限绕过
- **严重性能问题**：O(n²)以上算法、N+1查询
- **明显错误**：空指针异常、资源泄漏

### 🟡 中优先级（计划处理）
- **代码重复**：相同逻辑在多处出现
- **过长函数**：超过50行或圈复杂度>10
- **职责过多**：类承担不相关职责
- **复杂条件**：嵌套层级>3的条件语句

### 🟢 低优先级（优化处理）
- **命名优化**：变量、函数名不够语义化
- **格式不一致**：代码风格不统一
- **类型注解**：缺失的类型提示

## 示例

### 基础用法
```bash
# 分析单个Python文件
skill: "refactor-assistant" src/models/user.py

# 分析整个项目
skill: "refactor-assistant" src/

# 仅建议，不执行
skill: "refactor-assistant" --suggest-only src/
```

### 高级用法
```bash
# 专注特定问题类型
skill: "refactor-assistant" --focus complexity src/
skill: "refactor-assistant" --focus duplication src/
skill: "refactor-assistant" --focus naming src/

# 指定影响级别
skill: "refactor-assistant" --impact high src/
skill: "refactor-assistant" --impact medium src/
```

## 最佳实践

### 重构前准备
- ✅ 确保有完整的测试覆盖
- ✅ 建立代码质量基线
- ✅ 创建功能分支进行重构

### 重构过程
- ✅ 小步快跑，每次只改一个地方
- ✅ 每次修改后立即运行测试
- ✅ 保持对外接口的向后兼容性
- ✅ 记录重构原因和预期效果

### 重构后验证
- ✅ 运行完整测试套件
- ✅ 性能基准测试
- ✅ 代码审查和文档更新

## 常见重构模式

### 提取函数（Extract Function）

```python
# 重构前
def process_order(order):
    # validate order (10 lines)
    if not order.customer_id:
        raise ValueError("Customer ID required")
    if order.total <= 0:
        raise ValueError("Invalid total")

    # calculate total (15 lines)
    subtotal = sum(item.price * item.quantity for item in order.items)
    tax = subtotal * 0.1
    total = subtotal + tax

    # apply discounts (20 lines)
    if order.customer.is_premium:
        discount = total * 0.15
    elif len(order.items) > 5:
        discount = total * 0.1
    else:
        discount = 0

    final_total = total - discount
    # save order (5 lines)
    order.save()
```

```python
# 重构后
def process_order(order):
    validate_order(order)
    total = calculate_total(order)
    discounted = apply_discounts(order, total)
    save_order(order, discounted)

def validate_order(order):
    if not order.customer_id:
        raise ValueError("Customer ID required")
    if order.total <= 0:
        raise ValueError("Invalid total")

def calculate_total(order):
    subtotal = sum(item.price * item.quantity for item in order.items)
    tax = subtotal * 0.1
    return subtotal + tax
```

### 去除重复（Remove Duplication）

```python
# 重构前
def format_user_name(user):
    return f"{user.first_name} {user.last_name}".strip()

def format_admin_name(admin):
    return f"{admin.first_name} {admin.last_name}".strip()

# 重构后
def format_full_name(person):
    return f"{person.first_name} {person.last_name}".strip()
```

### 多态取代条件（Replace Conditional with Polymorphism）

```python
# 重构前
class PaymentProcessor:
    def process(self, payment):
        if payment.type == "credit_card":
            return self.process_credit_card(payment)
        elif payment.type == "paypal":
            return self.process_paypal(payment)
        elif payment.type == "bank_transfer":
            return self.process_bank_transfer(payment)

# 重构后
from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def process(self, payment):
        pass

class CreditCardPayment(PaymentStrategy):
    def process(self, payment):
        # credit card processing logic
        pass

class PayPalPayment(PaymentStrategy):
    def process(self, payment):
        # paypal processing logic
        pass

class PaymentProcessor:
    def __init__(self):
        self.strategies = {
            "credit_card": CreditCardPayment(),
            "paypal": PayPalPayment(),
            # ...
        }

    def process(self, payment):
        strategy = self.strategies[payment.type]
        return strategy.process(payment)
```

## 代码警示信号（Red Flags）

### 函数级别
- 参数超过 4 个的函数
- 嵌套层级超过 3 层的条件语句
- 圈复杂度 > 10
- 函数长度超过 50 行

### 类级别
- 拥有超过 10 个方法的类
- 类承担多个不相关的职责
- 过度继承（继承深度 > 3）

### 文件级别
- 文件长度超过 500 行
- 重复的代码块（3次以上）
- 魔法数字或字符串

### 架构级别
- 循环依赖
- 全局变量或全局状态
- 紧耦合的模块

## 依赖项

此技能可能需要以下工具和包：

```bash
# 代码质量分析工具
pip install bandit          # 安全检查
pip install flake8          # 代码风格
pip install mccabe          # 复杂度分析
pip install radon           # 代码度量

# 重构辅助工具
pip install rope            # Python重构库
pip install black           # 代码格式化
pip install isort           # 导入排序
```

## 注意事项

### 安全第一
- 每次重构后务必运行测试
- 重大结构调整前需获得批准
- 保留 Git 历史（不要压缩重构提交）

### 风险控制
- 清晰记录所有破坏性更改
- 在生产环境应用前进行充分测试
- 准备回滚计划

### 团队协作
- 重构前与团队成员沟通
- 确保所有人都理解重构的原因和效果
- 更新相关文档和注释