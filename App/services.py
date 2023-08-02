from sqlalchemy.orm import Session
import pandas as pd
from datetime import datetime, timedelta, time
import models, schema, crud
import uuid
import pytz


def process_timestamp(timestamp):
    timestamp_l=timestamp.split()
    date_l=timestamp_l[0].split('-')
    time_l=timestamp_l[1].replace('.',':').split(':')
    return datetime(int(date_l[0]),int(date_l[1]),int(date_l[2]),int(time_l[0]),int(time_l[1]),int(time_l[2]),int(time_l[3]))

def process_time(timestamp):
    timestamp_l=timestamp.split(":")
    return time(int(timestamp_l[0]), int(timestamp_l[1]), int(timestamp_l[2]))

def process_uuid():
    return str(uuid.uuid4())

def convert_timezone(timestamp, timezone):
    target_tz = None
    try:
        target_tz = pytz.timezone(timezone)
    except:
        target_tz = pytz.timezone("America/Chicago")
    source_tz = pytz.timezone('UTC')
    target_dt = source_tz.localize(timestamp).astimezone(target_tz)
    return target_dt

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

async def get_businesshour_data(db: Session):
    BusinessHours_data = pd.read_csv('Data\Menu hours.csv')
    i=0
    for ind, row in BusinessHours_data.iterrows():
        i=i+1
        if not row["start_time_local"]:
            row["start_time_local"]="0:0:0"
        if not row["end_time_local"]:
            row["end_time_local"]="23:59:59"
        row_schema = schema.BusinessHour(store_id = row["store_id"], dayOfWeek = row["day"], start_time_local=process_time(row["start_time_local"]), end_time_local=process_time(row["end_time_local"]))
        crud.create_businesshour(db, row_schema)
        if i%1000==0:
            print("Read ", i , " rows from Business Hours")