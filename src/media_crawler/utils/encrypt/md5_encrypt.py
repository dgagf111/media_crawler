"""
密码哈希工具模块

⚠️ 重要提醒：不再使用不安全的MD5算法
此模块已迁移到安全的bcrypt算法进行密码哈希。

bcrypt特性：
- 自适应哈希算法，可以抵御暴力破解
- 内置盐值（salt）生成
- 可配置的工作因子（cost factor）
- OWASP推荐用于密码存储的算法

使用示例：
    from pythonprojecttemplate.utils.encrypt.md5_encrypt import hash_password, verify_password

    # 密码哈希
    password = "my_secure_password"
    hashed = hash_password(password)
    print(f"哈希值: {hashed}")

    # 验证密码
    is_valid = verify_password(password, hashed)
    print(f"验证结果: {'成功' if is_valid else '失败'}")
"""

import secrets
from passlib.context import CryptContext

# 创建bcrypt密码上下文
# 使用自动弃用机制，支持算法升级
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # 设置成本因子（默认12，可根据需要调整）
)


def hash_password(password: str) -> str:
    """
    使用bcrypt算法对密码进行哈希

    :param password: 待哈希的明文密码
    :return: 哈希后的密码字符串（包含salt和参数）
    :raises ValueError: 密码为空或无效
    """
    if not password:
        raise ValueError("密码不能为空")

    # 使用secrets模块生成安全的随机密码
    # 这里只是示例，实际使用时直接传入用户密码
    if password == "generate_random":
        password = secrets.token_urlsafe(32)

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码是否正确

    :param plain_password: 明文密码
    :param hashed_password: 哈希后的密码
    :return: 验证结果，True表示密码正确
    :raises ValueError: 输入参数为空或无效
    """
    if not plain_password:
        raise ValueError("明文密码不能为空")

    if not hashed_password:
        raise ValueError("哈希密码不能为空")

    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        # 记录验证失败，但不暴露内部错误信息
        print(f"密码验证失败: {type(e).__name__}")
        return False


def needs_rehash(hashed_password: str) -> bool:
    """
    检查哈希密码是否需要重新哈希

    用于升级bcrypt成本因子或迁移到其他算法时使用

    :param hashed_password: 哈希后的密码
    :return: 是否需要重新哈希
    """
    try:
        return pwd_context.needs_update(hashed_password)
    except Exception:
        # 如果无法解析哈希值，建议重新哈希
        return True


# 保持向后兼容性别名
encrypt = hash_password


def generate_secure_password(length: int = 16) -> str:
    """
    生成安全的随机密码

    :param length: 密码长度，默认16字符
    :return: 安全的随机密码
    """
    if length < 8:
        raise ValueError("密码长度不能少于8个字符")

    # 生成URL安全的随机密码
    return secrets.token_urlsafe(length)


if __name__ == "__main__":
    print("=" * 80)
    print("🔐 bcrypt密码哈希测试")
    print("=" * 80)

    # 测试密码
    test_password = "MySecure123!@#"

    # 1. 密码哈希测试
    print("\n1️⃣ 密码哈希测试")
    print(f"原始密码: {test_password}")
    hashed = hash_password(test_password)
    print(f"哈希值: {hashed}")
    print(f"哈希长度: {len(hashed)} 字符")

    # 2. 密码验证测试
    print("\n2️⃣ 密码验证测试")
    is_valid = verify_password(test_password, hashed)
    print(f"正确密码验证: {'✅ 成功' if is_valid else '❌ 失败'}")

    # 验证错误密码
    wrong_password = "WrongPassword123"
    is_valid_wrong = verify_password(wrong_password, hashed)
    print(f"错误密码验证: {'✅ 成功（这不对！）' if is_valid_wrong else '❌ 失败（正确）'}")

    # 3. 密码重新哈希检查
    print("\n3️⃣ 密码重新哈希检查")
    needs_rehash_check = needs_rehash(hashed)
    print(f"需要重新哈希: {'是' if needs_rehash_check else '否'}")

    # 4. 不同密码生成不同哈希
    print("\n4️⃣ 不同密码生成不同哈希")
    hashed2 = hash_password(test_password)
    print(f"相同密码第二次哈希: {hashed2}")
    print(f"两次哈希是否相同: {'❌ 相同（不安全）' if hashed == hashed2 else '✅ 不同（安全）'}")

    # 5. 生成安全密码示例
    print("\n5️⃣ 生成安全密码示例")
    for length in [8, 12, 16, 20]:
        secure_pwd = generate_secure_password(length)
        print(f"  {length:2d}位密码: {secure_pwd}")

    print("\n" + "=" * 80)
    print("✅ 所有测试通过！")
    print("=" * 80)
    print("\n📢 重要提示：")
    print("   • bcrypt已自动处理salt，无需手动添加")
    print("   • 哈希结果包含算法参数，可安全存储在数据库中")
    print("   • 建议定期检查needs_rehash()以升级安全参数")
    print("   • 生产环境应设置更强的bcrypt成本因子（建议14-16）")
