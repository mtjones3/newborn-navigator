from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
from app.database import Base


class MilestoneTracking(Base):
    __tablename__ = "milestone_tracking"
    __table_args__ = (
        UniqueConstraint("subscriber_id", "milestone_id", name="uq_subscriber_milestone"),
    )

    id = Column(Integer, primary_key=True, index=True)
    subscriber_id = Column(Integer, ForeignKey("subscribers.id"), nullable=False, index=True)
    milestone_id = Column(Integer, ForeignKey("milestones.id"), nullable=False, index=True)
    status = Column(String, nullable=True)  # "achieved" or "concern"; NULL = not tracked
    notes = Column(Text, nullable=True)
    achieved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
