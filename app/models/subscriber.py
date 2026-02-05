import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean
from app.database import Base


class Subscriber(Base):
    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    baby_name = Column(String, nullable=True)
    baby_birth_date = Column(Date, nullable=True)
    baby_due_date = Column(Date, nullable=True)
    neighborhood = Column(String, nullable=True)
    tier = Column(String, default="free")  # free or paid
    is_active = Column(Boolean, default=True)
    unsubscribe_token = Column(
        String, default=lambda: uuid.uuid4().hex, unique=True, nullable=False
    )
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
