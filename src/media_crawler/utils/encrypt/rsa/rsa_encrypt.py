import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

class RSACipher:
    def __init__(self, private_key=None, public_key=None):
        """
        初始化RSACipher类。
        
        :param private_key: 可选的私钥。如果未提供，则生成新的密钥对。
        :param public_key: 可选的公钥。如果未提供，则使用生成的密钥对中的公钥。
        """
        if private_key and public_key:
            self.private_key = private_key
            self.public_key = public_key
        else:
            self.private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )
            self.public_key = self.private_key.public_key()

    def encrypt(self, plaintext, public_key=None):
        """
        使用RSA算法加密明文。
        
        :param plaintext: 要加密的明文字符串。
        :param public_key: 可选的公钥。如果未提供，则使用实例的公钥。
        :return: 加密后的密文。
        """
        public_key = public_key or self.public_key
        ciphertext = public_key.encrypt(
            plaintext.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return ciphertext

    def decrypt(self, ciphertext, private_key=None):
        """
        使用RSA算法解密密文。
        
        :param ciphertext: 要解密的密文。
        :param private_key: 可选的私钥。如果未提供，则使用实例的私钥。
        :return: 解密后的明文字符串。
        """
        private_key = private_key or self.private_key
        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext.decode()

    def serialize_keys(self):
        """
        序列化私钥和公钥。
        
        :return: 私钥和公钥的PEM格式字符串。
        """
        private_pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return private_pem, public_pem

    @staticmethod
    def load_keys(private_pem, public_pem):
        """
        从PEM格式字符串加载私钥和公钥。
        
        :param private_pem: 私钥的PEM格式字符串。
        :param public_pem: 公钥的PEM格式字符串。
        :return: RSACipher实例。
        """
        private_key = serialization.load_pem_private_key(
            private_pem,
            password=None,
        )
        public_key = serialization.load_pem_public_key(
            public_pem,
        )
        return RSACipher(private_key, public_key)

# 测试代码
if __name__ == "__main__":
    cipher = RSACipher()

    # 使用生成的密钥对
    plaintext = "Hello, World!"
    print("原始明文:", plaintext)
    print("使用生成的公钥加密...")
    ciphertext = cipher.encrypt(plaintext)
    print("密文:", ciphertext)

    decrypted_text = cipher.decrypt(ciphertext)
    print("解密后的明文:", decrypted_text)
    assert decrypted_text == plaintext, "生成的密钥对解密失败"

    # 序列化和加载密钥
    private_pem, public_pem = cipher.serialize_keys()
    print("\n私钥:", private_pem)
    print("公钥:", public_pem)

    loaded_cipher = RSACipher.load_keys(private_pem, public_pem)
    ciphertext_loaded = loaded_cipher.encrypt(plaintext)
    print("使用加载的公钥加密后的密文:", ciphertext_loaded)

    decrypted_text_loaded = loaded_cipher.decrypt(ciphertext_loaded)
    print("解密后的明文:", decrypted_text_loaded)
    assert decrypted_text_loaded == plaintext, "加载的密钥对解密失败"

    print("\n所有测试通过！")