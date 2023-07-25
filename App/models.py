from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base

class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True)
    timestamp_utc = Column(DateTime)
    status = Column(String(8))

class BusinessHour(Base):
    __tablename__ = "businesshours"

    id = Column(Integer, primary_key=True)
    store_id = Column(Integer)
    day = Column(Integer)
    open = Column(DateTime)
    close = Column(DateTime)

class Timezone(Base):
    __timezone__ = "timezones"

    id = Column(Integer, primary_key=True)
    store_id = Column(Integer)
    timezone = Column(String(64))
    