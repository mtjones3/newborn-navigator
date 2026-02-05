from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from app.database import Base


class Milestone(Base):
    __tablename__ = "milestones"

    id = Column(Integer, primary_key=True, index=True)
    week_number = Column(Integer, nullable=False, index=True)  # 0-12
    category = Column(
        String, nullable=False
    )  # motor, sensory, communication, feeding, sleep, social_emotional, cognitive
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    source = Column(String, nullable=True)  # e.g. "AAP", "CDC"
    parent_action = Column(Text, nullable=True)
    is_concern_flag = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
