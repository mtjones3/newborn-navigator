from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from app.database import Base


class LocalResource(Base):
    __tablename__ = "local_resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)  # hospital, pediatrician, daycare
    neighborhood = Column(String, nullable=False, index=True)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    website = Column(String, nullable=True)
    hours = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    rating = Column(Float, nullable=True)
    accepts_insurance = Column(Boolean, default=True)
    age_range = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
