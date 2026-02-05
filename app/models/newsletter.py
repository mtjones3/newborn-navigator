from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class NewsletterIssue(Base):
    __tablename__ = "newsletter_issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    subject_line = Column(String, nullable=False)
    week_number = Column(Integer, nullable=False)  # 0-16
    status = Column(String, default="draft")  # draft, scheduled, sent
    sent_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sections = relationship(
        "ContentSection",
        back_populates="newsletter",
        cascade="all, delete-orphan",
        order_by="ContentSection.sort_order",
    )


class ContentSection(Base):
    __tablename__ = "content_sections"

    id = Column(Integer, primary_key=True, index=True)
    newsletter_id = Column(
        Integer, ForeignKey("newsletter_issues.id"), nullable=False
    )
    section_type = Column(
        String, nullable=False
    )  # greeting, milestones, noteworthy, tips, qa, custom
    title = Column(String, nullable=True)
    body = Column(Text, nullable=False, default="")
    sort_order = Column(Integer, default=0)
    is_paid_only = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    newsletter = relationship("NewsletterIssue", back_populates="sections")
