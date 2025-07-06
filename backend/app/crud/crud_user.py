from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """
    用户CRUD操作类。
    """
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        """
        根据邮箱获取用户。
        """
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        """
        创建新用户，对密码进行哈希处理。
        """
        hashed_password = get_password_hash(obj_in.password)
        db_obj = User(
            email=obj_in.email,
            hashed_password=hashed_password,
            full_name=obj_in.full_name,
            is_active=True, # 默认激活
            is_superuser=False # 默认非超级用户
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: User, obj_in: UserUpdate) -> User:
        """
        更新用户，如果提供了新密码则进行哈希处理。
        """
        if obj_in.password:
            obj_in.password = get_password_hash(obj_in.password)
        return await super().update(db, db_obj=db_obj, obj_in=obj_in)

user = CRUDUser(User) # 实例化CRUDUser对象，方便在其他地方导入和使用 