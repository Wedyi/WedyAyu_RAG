from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,M
from sqlalchemy import DateTime,func
from datetime import datetime

class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
