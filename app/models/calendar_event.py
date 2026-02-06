from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Time, ForeignKey
from app.database import Base


class CalendarEvent(Base):
    __tablename__ = "calendar_events"

    id = Column(Integer, primary_key=True, index=True)
    subscriber_id = Column(Integer, ForeignKey("subscribers.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    event_date = Column(Date, nullable=False, index=True)
    event_time = Column(Time, nullable=True)
    category = Column(String, nullable=True)  # dr_appointment, family_visit, milestone, vaccination, other
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
