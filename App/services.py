from sqlalchemy.orm import Session
import pandas as pd
from datetime import datetime, timedelta
import models, schema, crud
import uuid

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

