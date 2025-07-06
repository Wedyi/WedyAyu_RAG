# backend/app/core/security.py
from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Union

from passlib.context import CryptContext
from jose import jwt, JWTError

from app.core.config import settings
from app.schemas.token import TokenPayload

# 用于密码哈希的上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证明文密码是否与哈希密码匹配。
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    对密码进行哈希。
    """
    return pwd_context.hash(password)

def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    创建JWT访问令牌。
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)  # 默认30分钟过期

    to_encode = {"exp": expire, "sub": str(subject)}
    # 确保Secret_Key不为None，如果为None则使用默认值
    secret_key = settings.Secret_Key or "default-secret-key"
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")
    return encoded_jwt

def decode_token(token: str) -> Optional[TokenPayload]:
    """
    解码JWT令牌并返回负载。
    """
    try:
        payload = jwt.decode(
            token, "your-secret-key", algorithms=["HS256"]
        )
        # 使用Pydantic进行负载校验
        token_data = TokenPayload(**payload)
        return token_data
    except JWTError:
        # JWT解码失败（如签名无效、过期等）
        return None
    except Exception as e:
        # 其他异常
        print(f"Error decoding token: {e}")
        return None