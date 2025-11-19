import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from rsa_encrypt import RSACipher

def generate_rsa_keys(key_size=2048, public_exponent=65537):
    """
    生成RSA密钥对。
    
    :param key_size: 密钥大小（比特），默认为2048
    :param public_exponent: 公共指数，默认为65537
    :return: 包含私钥和公钥PEM格式字符串的元组
    """
    # 生成私钥
    private_key = rsa.generate_private_key(
        public_exponent=public_exponent,
        key_size=key_size
    )

    # 生成公钥
    public_key = private_key.public_key()

    # 将私钥序列化为PEM格式
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # 将公钥序列化为PEM格式
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem, public_pem

if __name__ == "__main__":
    # 生成密钥对
    private_pem, public_pem = generate_rsa_keys()

    print("生成的私钥:")
    print(private_pem.decode())

    print("\n生成的公钥:")
    print(public_pem.decode())

    # 使用生成的密钥对进行加密和解密验证
    cipher = RSACipher.load_keys(private_pem, public_pem)

    plaintext = "Hello, World!"
    print("\n原始明文:", plaintext)

    ciphertext = cipher.encrypt(plaintext)
    print("加密后的密文:", ciphertext)

    decrypted_text = cipher.decrypt(ciphertext)
    print("解密后的明文:", decrypted_text)

    assert decrypted_text == plaintext, "解密失败"
    print("\n加密和解密验证通过！")