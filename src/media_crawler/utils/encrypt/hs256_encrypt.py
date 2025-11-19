import hmac
import hashlib
import os

def hs256_hash(text: str, secret_key: bytes = None) -> str:
    """
    使用HS256 (HMAC-SHA256) 算法对输入的文本进行哈希。

    注意：HMAC-SHA256是一种哈希算法，不是加密算法。
    它使用密钥对文本进行哈希，适用于消息完整性验证和消息认证码（MAC）。

    :param text: 需要哈希的文本
    :param secret_key: 可选的密钥，如果不提供则随机生成
    :return: 哈希后的十六进制字符串
    """
    if secret_key is None:
        secret_key = os.urandom(32)  # 生成32字节的随机密钥
    elif isinstance(secret_key, str):
        secret_key = secret_key.encode('utf-8')

    # 使用HMAC-SHA256进行哈希
    hmac_obj = hmac.new(secret_key, text.encode('utf-8'), hashlib.sha256)
    return hmac_obj.hexdigest()


def verify_hs256(text: str, hashed_text: str, secret_key: bytes) -> bool:
    """
    验证文本的HMAC-SHA256哈希值是否匹配。

    :param text: 待验证的文本
    :param hashed_text: 存储的哈希值（十六进制）
    :param secret_key: 使用的密钥
    :return: 布尔值，表示验证是否成功
    """
    new_hash = hs256_hash(text, secret_key)
    return new_hash == hashed_text


# 保持向后兼容性别名（已弃用）
def hs256_encrypt(text: str, secret_key: bytes = None) -> str:
    """
    ⚠️ 已弃用：请使用 hs256_hash()

    使用HS256 (HMAC-SHA256) 算法对输入的文本进行哈希。

    :param text: 需要哈希的文本
    :param secret_key: 可选的密钥
    :return: 哈希后的十六进制字符串
    """
    import warnings
    warnings.warn(
        "hs256_encrypt已弃用，请使用hs256_hash()，"
        "因为HMAC-SHA256是哈希算法而非加密算法",
        DeprecationWarning,
        stacklevel=2
    )
    return hs256_hash(text, secret_key)

if __name__ == "__main__":
    print("=" * 80)
    print("🔐 HS256 (HMAC-SHA256) 哈希测试")
    print("=" * 80)

    sample_text = "Hello, World!"
    secret_key = os.urandom(32)  # 生成密钥

    print(f"\n📝 原始文本: {sample_text}")
    print(f"🔑 密钥（十六进制）: {secret_key.hex()}")

    # 使用新的函数名
    hashed_text = hs256_hash(sample_text, secret_key)
    print(f"🔒 HS256哈希值: {hashed_text}")

    # 验证
    is_valid = verify_hs256(sample_text, hashed_text, secret_key)
    print(f"✅ 验证结果: {'成功' if is_valid else '失败'}")

    # 尝试验证错误的文本
    wrong_text = "Hello, World"
    is_valid_wrong = verify_hs256(wrong_text, hashed_text, secret_key)
    print(f"❌ 错误文本验证: {'成功（这不对！）' if is_valid_wrong else '失败（正确）'}")

    print("\n" + "=" * 80)
    print("✅ 测试完成")
    print("=" * 80)
    print("\n📌 注意：HMAC-SHA256是哈希算法，不是加密算法")
    print("   • 适用于消息完整性验证")
    print("   • 适用于生成消息认证码（MAC）")
    print("   • 不适用于加密数据（无法解密）")
