from sqlalchemy import Column, String, BigInteger, Boolean, DateTime, Float, CHAR, UniqueConstraint, Text,JSON
from datetime import datetime
from sqlalchemy.orm import relationship

from .connection import Base


class Subject(Base):
    __tablename__ = "subject"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    subject_name = Column(String(100), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now())
    random_rate = Column(Float, nullable=False, default=0.0)
    overlap_rate = Column(Float, nullable=False, default=0.0)
    status = Column(String(20), nullable=False, default="ready")
    task = Column(String(40), nullable=False)


class Label(Base):
    __tablename__ = "label"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    subject_id = Column(BigInteger, nullable=False)
    value = Column(String(1000), nullable=False, unique=True)
    shortcut = Column(CHAR(1), nullable=False, unique=True)


class Agent(Base):
    __tablename__ = "agent"

    id = Column(String(20), primary_key=True, index=True)
    privilege = Column(String(20), nullable=False)


class SubjectAgentMapping(Base):
    __tablename__ = "subject_agent_mapping"

    __table_args__ = (
        UniqueConstraint('subject_id', 'agent_id', name='unique_combination'),
    )

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    subject_id = Column(BigInteger, nullable=False)
    agent_id = Column(String(20), nullable=False)


class TextClassification(Base):
    __tablename__ = "textclassification"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    content = Column(Text, nullable=False)
    subject_id = Column(BigInteger, nullable=False)
    label_id = Column(BigInteger)
    priority = Column(Float, nullable=False, index=True)
    meta = Column(JSON)
    status = Column(String, nullable=False, default="ready")
    updated_by = Column(String(20))


class ImageClassification(Base):
    __tablename__ = "imageclassification"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    content_url = Column(String(200), nullable=False)
    subject_id = Column(BigInteger, nullable=False)
    label_id = Column(BigInteger)
    priority = Column(Float, nullable=False, index=True)
    meta = Column(JSON)
    status = Column(String, nullable=False, default="ready")
    updated_by = Column(String(20))


class LabelLog(Base):
    __tablename__ = "labellog"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now())
    agent_id = Column(String(20), nullable=False)
    subject_id = Column(BigInteger, nullable=False)
    content_id = Column(BigInteger, nullable=False)
    label_id = Column(BigInteger, nullable=False)




