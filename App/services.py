from sqlalchemy.orm import Session
import pandas as pd
from datetime import datetime, timedelta
import models
import schema

def get_data():
    Store_data = pd.read_csv('Data\store status.csv')
    print(Store_data)

