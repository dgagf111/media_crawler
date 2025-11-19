from sqlalchemy import Column, BigInteger, String, DateTime, Integer
from sqlalchemy.sql import func
from zoneinfo import ZoneInfo

from pythonprojecttemplate.config.settings import settings
from pythonprojecttemplate.db.mysql.mysql import MySQL_Base

TIME_ZONE = ZoneInfo(settings.common.time_zone)

# state的设计是大于等于0的都是可以访问的，小于0的都是不可访问的
class User(MySQL_Base):
    __tablename__ = 'users'

    # 用户ID
    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    # 用户名
    username = Column(String(255), unique=True, nullable=False)
    # 密码哈希
    password_hash = Column(String(255), nullable=False)
    # 邮箱
    email = Column(String(255), unique=True, nullable=False)
    # 电话号码
    phone_number = Column(String(20), unique=True)
    # 身份证号码
    id_card_number = Column(String(50), unique=True)
    # 上一次登录时间
    last_login_at = Column(DateTime)
    # 状态，-1: 已删除, -2: 已禁用, 0正常，1: 高风险
    state = Column(Integer, default=0)
    # 创建时间
    created_at = Column(DateTime, server_default=func.now())
    # 更新时间
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Token(MySQL_Base):
    __tablename__ = 'tokens'

    # 令牌ID
    token_id = Column(BigInteger, primary_key=True, autoincrement=True)
    # 用户ID
    user_id = Column(BigInteger, nullable=False)
    # 令牌
    token = Column(String(255), unique=True, nullable=False)
    # 令牌类型，0用户登录持久化数据，1用户API调用的token
    token_type = Column(Integer, nullable=False)
    # 过期时间
    expires_at = Column(DateTime(timezone=True), nullable=False)
    # 状态，-1: 已删除, -2: 已禁用, 0正常，1: 高风险
    state = Column(Integer, default=0)
    # 创建时间
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # 更新时间
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.expires_at and self.expires_at.tzinfo is None:
            self.expires_at = self.expires_at.replace(tzinfo=TIME_ZONE)

class ThirdPartyToken(MySQL_Base):
    __tablename__ = 'third_party_tokens'

    # 第三方令牌ID  
    token_id = Column(BigInteger, primary_key=True, autoincrement=True)
    # 用户ID
    user_id = Column(BigInteger, nullable=False)
    # 提供商
    provider = Column(String(50), nullable=False)
    # 第三方令牌
    third_party_token = Column(String(255), unique=True, nullable=False)
    # 过期时间
    expires_at = Column(DateTime, nullable=False)
    # 状态，-1: 已删除, -2: 已禁用, 0正常，1: 高风险
    state = Column(Integer, default=0)
    # 创建时间
    created_at = Column(DateTime, server_default=func.now())
    # 更新时间
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
