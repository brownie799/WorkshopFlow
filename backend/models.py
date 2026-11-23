from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    phone = Column(String(20))
    password = Column(String(255), nullable=False)
    role = Column(String(20), default="customer")


class JobCard(Base):
    __tablename__ = "job_cards"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    vehicle_number = Column(String(30), index=True)
    vehicle_model = Column(String(100))
    complaint = Column(String(500))
    job_code = Column(String(100))
    status = Column(String(50), default="Received")
    estimated_hours = Column(Float, default=1.0)
    estimated_ready_time = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)