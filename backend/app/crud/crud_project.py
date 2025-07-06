from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate

class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    """
    项目CRUD操作类。
    """
    async def get_multi_by_owner(
        self, db: AsyncSession, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        """
        获取某个用户拥有的多个项目。
        """
        stmt = select(Project).where(Project.owner_id == owner_id).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return list(result.scalars().all())

project = CRUDProject(Project) # 实例化CRUDProject对象 