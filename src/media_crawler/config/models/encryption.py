from __future__ import annotations

from pydantic import BaseModel, Field


class EncryptionSettings(BaseModel):
    """加密配置管理"""

    aes_key_hex: str = Field(
        default="",
        description="AES加密密钥（十六进制格式，64字符=32字节）",
    )

    @property
    def aes_key(self) -> bytes:
        """
        获取AES密钥（字节格式）
        :raises ValueError: 密钥未配置或格式不正确
        """
        if not self.aes_key_hex:
            raise ValueError(
                "未配置AES密钥！请设置PPT_ENCRYPTION__AES_KEY环境变量\n"
                '生成密钥命令：python -c "import os; print(os.urandom(32).hex())"'
            )

        if len(self.aes_key_hex) != 64:
            raise ValueError(
                f"AES密钥长度错误：{len(self.aes_key_hex)}，应为64个十六进制字符"
            )

        try:
            key = bytes.fromhex(self.aes_key_hex)
            if len(key) != 32:
                raise ValueError(f"AES密钥长度错误：{len(key)}字节，应为32字节")
            return key
        except ValueError as exc:
            raise ValueError("AES密钥格式错误：应为64个十六进制字符") from exc

    @property
    def is_configured(self) -> bool:
        """检查是否已配置加密密钥"""
        return bool(self.aes_key_hex)


__all__ = ["EncryptionSettings"]
