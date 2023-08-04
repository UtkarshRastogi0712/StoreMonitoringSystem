from pydantic import BaseModel
from datetime import datetime, time

class Store(BaseModel):
    store_id: int
    timestamp_utc: datetime
    status: str
    class Config:
        orm_model = True

class BusinessHour(BaseModel):
    store_id: int
    dayOfWeek: int
    start_time_local: time
    end_time_local: time
    class Config:
        orm_model = True

class Timezone(BaseModel):
    store_id: int
    timezone_str: str
    class Config:
        orm_model = True

class Report(BaseModel):
    store_id: int
    uptime_last_hour: int
    uptime_last_day: int
    downtime_last_hour: int
    downtime_last_day: int
    class Config:
        orm_model = True