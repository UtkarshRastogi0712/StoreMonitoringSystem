from sqlalchemy.orm import Session
import pandas as pd
from datetime import datetime, timedelta
import models, schema, crud
import uuid


def process_timestamp(timestamp):
    timestamp_l=timestamp.split()
    date_l=timestamp_l[0].split('-')
    time_l=timestamp_l[1].replace('.',':').split(':')
    return datetime(int(date_l[0]),int(date_l[1]),int(date_l[2]),int(time_l[0]),int(time_l[1]),int(time_l[2]),int(time_l[3]))

def process_uuid():
    return str(uuid.uuid4())

async def get_timezone_data(db: Session):
    Timezone_data = pd.read_csv('Data\Timezones.csv')
    i=0
    existing_timezones =[]
    existing_data=crud.get_all(db, models.Timezone)
    for instance in existing_data:
        existing_timezones.append(int(instance.store_id))
    print(existing_timezones)
    for ind, row in Timezone_data.iterrows():
        if not row["timezone_str"] :
            row["timezone_str"] = "America/Chicago"
        if row["store_id"] not in existing_timezones:
            i=i+1
            row_schema = schema.Timezone(store_id = row["store_id"], timezone_str = row["timezone_str"])
            crud.create_timezone(db, row_schema)
            if i%1000==0:
                print("Read ", i , " rows from Timezones")
        else:
            print("Already exists")

async def get_store_data(db: Session):
    Store_data = pd.read_csv('Data\store status.csv')
    i=0
    for ind, row in Store_data.iterrows():
        i=i+1
        row_schema = schema.Store(store_id = row["store_id"], timestamp_utc = process_timestamp(row["timestamp_utc"]), status = row["status"])
        crud.create_store(db, row_schema)
        if i%1000==0:
            print("Read ", i , " rows from Stores")