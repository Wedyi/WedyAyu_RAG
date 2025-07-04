from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
import enum

class KnowledgeBaseStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"

class KnowledgeBase(Base):
    __tablename__ = "knowledge_bases"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    status: Mapped[KnowledgeBaseStatus] = mapped_column(Enum(KnowledgeBaseStatus), default=KnowledgeBaseStatus.PENDING,nullable=False)
    vector_store_path: Mapped[str] = mapped_column(String(255), nullable=False)
    owner: Mapped["User"] = relationship("User", back_populates="knowledge_bases")

    def __repr__(self):
        return f"<KnowledgeBase {self.name},status{self.status}>,owner_id{self.owner_id}>"

from models.user import User

User.knowledge_bases = relationship("KnowledgeBase", back_populates="owner")
User.projects = relationship("Project", back_populates="owner")






