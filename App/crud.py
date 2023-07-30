from sqlalchemy.orm import Session
import models, schema

def create_store(db: Session, store: schema.Store):
    db_store = models.Store(store_id = store.store_id ,timestamp_utc = store.timestamp_utc ,status = store.status)
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store

def create_timezone(db: Session, timezone: schema.Timezone):
    db_timezone = models.Timezone(id = timezone.id, store_id = timezone.store_id, timezone_str = timezone.timezone_str)
    db.add(db_timezone)
    db.commit()
    db.refresh(db_timezone)
    return 