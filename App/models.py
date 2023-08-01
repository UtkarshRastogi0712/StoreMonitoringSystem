from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, BigInteger
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Timezone(Base):
    __tablename__ = "timezones"

    store_id = Column(BigInteger, primary_key=True)
    timezone_str = Column(String(64))

class Store(Base):
    __tablename__ = "stores"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(BigInteger)
    timestamp_utc = Column(DateTime)
    status = Column(String(8))

class BusinessHour(Base):
    __tablename__ = "businesshours"

    id = Column(String(32), primary_key=True)
    store_id = Column(BigInteger)
    dayOfWeek = Column(Integer)
    start_time_local = Column(DateTime)
    end_time_local = Column(DateTime)

class Report(Base):
    __tablename__ = "report"
    id = Column(Integer, primary_key=True)
    uptime_last_hour = Column(Integer)
    uptime_last_day = Column(Integer)
    uptime_last_week = Column(Integer)
    downtime_last_hour = Column(Integer)
    downtime_last_day = Column(Integer)
    downtime_last_week = Column(Integer)

    