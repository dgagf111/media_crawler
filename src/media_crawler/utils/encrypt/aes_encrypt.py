import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

class AESCipher:
    """AES加密工具类

    使用说明：
    1. 必须通过环境变量或配置提供32字节（256位）的密钥
    2. 密钥示例：os.urandom(32).hex() 获取十六进制密钥
    3. 或使用：PPT_ENCRYPTION__AES_KEY 环境变量
    """

    def __init__(self, key: bytes):
        """
        初始化AES加密器

        :param key: 32字节的加密密钥（256位）
        :raises ValueError: 密钥无效或长度不正确
        """
        if not key:
            raise ValueError("密钥不能为空，必须提供32字节的密钥")
        if len(key) != 32:
            raise ValueError(f"密钥长度必须为32字节（256位），当前长度：{len(key)}")
        self.key = key

    def encrypt(self, plaintext: str, key: bytes = None) -> bytes:
        """
        加密明文

        :param plaintext: 待加密的明文字符串
        :param key: 可选的加密密钥，默认使用实例密钥
        :return: 加密后的密文（包含IV前缀）
        """
        key = key or self.key
        iv = os.urandom(16)  # 128-bit IV
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return iv + ciphertext

    def decrypt(self, ciphertext: bytes, key: bytes = None) -> str:
        """
        解密密文

        :param ciphertext: 待解密的密文（包含IV前缀）
        :param key: 可选的解密密钥，默认使用实例密钥
        :return: 解密后的明文字符串
        :raises ValueError: 密文格式不正确或解密失败
        """
        key = key or self.key
        iv = ciphertext[:16]
        actual_ciphertext = ciphertext[16:]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        return plaintext.decode()

# 测试代码
if __name__ == "__main__":
    # 生成安全的256位随机密钥
    test_key = os.urandom(32)
    print(f"🔑 测试密钥（十六进制）: {test_key.hex()}")
    print(f"🔑 测试密钥长度: {len(test_key)} 字节\n")

    cipher = AESCipher(test_key)

    plaintext = "Hello, World!"
    print("原始明文:", plaintext)

    # 使用密钥加密
    ciphertext = cipher.encrypt(plaintext)
    print("密文（十六进制）:", ciphertext.hex())

    # 解密验证
    decrypted_text = cipher.decrypt(ciphertext)
    print("解密后的明文:", decrypted_text)

    # 断言验证
    assert decrypted_text == plaintext, "解密失败，数据不匹配"
    print("✅ 解密验证成功")

    # 使用不同密钥进行测试
    custom_key = os.urandom(32)  # 256-bit key
    print("\n使用不同密钥加密测试...")
    ciphertext_custom = cipher.encrypt(plaintext, key=custom_key)
    decrypted_text_custom = cipher.decrypt(ciphertext_custom, key=custom_key)
    assert decrypted_text_custom == plaintext, "自定义密钥解密失败"
    print("✅ 自定义密钥测试通过")

    print("\n🎉 所有测试通过！")
    print("\n📢 重要提示：")
    print("   请妥善保管您的加密密钥，任何拥有密钥的人都可以解密数据！")
    print("   生产环境请使用环境变量 PPT_ENCRYPTION__AES_KEY 设置密钥")