from sqlalchemy.orm import Session
import pandas as pd
from datetime import datetime, timedelta
import models
import schema
import crud

async def get_data(db: Session):
    Timezone_data = pd.read_csv('Data\Timezones.csv')
    i=0
    for ind, row in Timezone_data.iterrows():
        i=i+1
        row_schema = schema.Timezone(id = i, store_id = row["store_id"], timezone_str = row["timezone_str"])
        crud.create_timezone(db, row_schema)
        if i%100==0:
            print("Read ", i , " rows")


