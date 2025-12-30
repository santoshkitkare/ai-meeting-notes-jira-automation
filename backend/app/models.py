from sqlalchemy import Column, String, Enum, Text, JSON
from app.db import Base
import enum

class JobStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(String, primary_key=True, index=True)
    source_url = Column(String)
    source_type = Column(String)
    status = Column(Enum(JobStatus), default=JobStatus.PENDING)
    result = Column(Text, nullable=True)
    jira_tickets = Column(JSON, nullable=True)   # ✅ NEW
