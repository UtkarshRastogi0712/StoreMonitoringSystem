from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Store(Base):
    __tablename__ = "stores"

    store_id = Column(Integer, primary_key=True)
    timestamp_utc = Column(DateTime)
    status = Column(String(8))

class BusinessHour(Base):
    __tablename__ = "businesshours"

    id = Column(Integer, primary_key=True)
    store_id = Column(Integer)
    dayOfWeek = Column(Integer)
    start_time_local = Column(DateTime)
    end_time_local = Column(DateTime)

class Timezone(Base):
    __tablename__ = "timezones"

    id = Column(Integer, primary_key=True)
    store_id = Column(Integer)
    timezone = Column(String(64))

class Report(Base):
    __tablename__ = "report"
    id = Column(Integer, primary_key=True)
    uptime_last_hour = Column(Integer)
    uptime_last_day = Column(Integer)
    uptime_last_week = Column(Integer)
    downtime_last_hour = Column(Integer)
    downtime_last_day = Column(Integer)
    downtime_last_week = Column(Integer)

    