from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from sqlalchemy.dialects.postgresql import JSONB # 针对PostgreSQL的JSONB类型
from models.user import User

class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    workflow_definition: Mapped[dict] = mapped_column(JSONB, nullable=False,default=lambda: {})
    owner: Mapped["User"] = relationship("User", back_populates="projects")
