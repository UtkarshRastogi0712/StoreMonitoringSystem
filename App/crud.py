from sqlalchemy.orm import Session
import models, schema

def create_store(db: Session, store: schema.Store):
    db_store = models.Store(store_id = store.store_id ,timestamp_utc = store.timestamp_utc ,status = store.status)
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store

def create_timezone(db: Session, timezone: schema.Timezone):
    db_timezone = models.Timezone(store_id = timezone.store_id, timezone_str = timezone.timezone_str)
    db.add(db_timezone)
    db.commit()
    db.refresh(db_timezone)
    return 

def create_businesshour(db: Session, businesshour: schema.BusinessHour):
    db_businesshour = models.BusinessHour(store_id = businesshour.store_id, dayOfWeek = businesshour.dayOfWeek, start_time_local = businesshour.start_time_local, end_time_local = businesshour.end_time_local)
    db.add(db_businesshour)
    db.commit()
    db.refresh(db_businesshour)
    return 

def create_report(db: Session, report: schema.Report):
    db_report = models.Report(store_id = report.store_id, uptime_last_hour = report.uptime_last_hour, downtime_last_hour = report.downtime_last_hour, uptime_last_day = report.uptime_last_day, downtime_last_day = report.downtime_last_day)
    db.add(db_report)
    db.commit()
    db.refresh(db_report)

def get_all(db: Session, table: str):
    return db.query(table).all()