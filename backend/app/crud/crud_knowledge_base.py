from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.knowledge_base import KnowledgeBase
from app.schemas.knowledge_base import KnowledgeBaseCreate, KnowledgeBaseUpdate

class CRUDKnowledgeBase(CRUDBase[KnowledgeBase, KnowledgeBaseCreate, KnowledgeBaseUpdate]):
    """
    知识库CRUD操作类。
    """
    async def get_multi_by_owner(
        self, db: AsyncSession, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[KnowledgeBase]:
        """
        获取某个用户拥有的多个知识库。
        """
        stmt = select(KnowledgeBase).where(KnowledgeBase.owner_id == owner_id).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return list(result.scalars().all())

knowledge_base = CRUDKnowledgeBase(KnowledgeBase) # 实例化CRUDKnowledgeBase对象 