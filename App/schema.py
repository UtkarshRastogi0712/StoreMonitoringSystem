from pydantic import BaseModel
from datetime import datetime

class Store(BaseModel):
    store_id: int
    timestamp_utc: datetime
    status: str
    class Config:
        orm_model = True

class BusinessHour(BaseModel):
    id: int
    store_id: int
    dayOfWeek: int
    start_time_local: datetime
    end_time_local: datetime
    class Config:
        orm_model = True

class Timezone(BaseModel):
    id: int
    store_id: int
    timezone: str
    class Config:
        orm_model = True

class Report(BaseModel):
    id: int
    uptime_last_hour: int
    uptime_last_day: int
    uptime_last_week: int
    downtime_last_hour: int
    downtime_last_day: int
    downtime_last_week: int
    class Config:
        orm_model = True