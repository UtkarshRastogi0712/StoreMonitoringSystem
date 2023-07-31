from sqlalchemy.orm import Session
import pandas as pd
from datetime import datetime, timedelta
import models, schema, crud
import uuid


def process_timestamp(timestamp):
    Y=int(timestamp[:4])
    M=int(timestamp[5:7])
    D=int(timestamp[8:10])
    h=int(timestamp[11:13])
    m=int(timestamp[14:16])
    s=int(timestamp[17:19])
    ms=int(timestamp[20:25])
    return datetime(Y,M,D,h,m,s,ms)

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
            if i%100==0:
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
        if i%100==0:
            print("Read ", i , " rows from Stores")