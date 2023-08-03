from sqlalchemy.orm import Session
import pandas as pd
from datetime import datetime, timedelta, time, date
import models, schema, crud, services

async def generate_report_from_csv():
    Timezone_data = pd.read_csv('Data\Timezones.csv')
    Store_data = pd.read_csv('Data\store status.csv')
    BusinessHours_data = pd.read_csv('Data\Menu hours.csv')
    max_timestamp = services.process_timestamp(Store_data["timestamp_utc"].max())
    print("Getting store uptime")
    store_uptime = get_store_uptime(Store_data)
    print("Got store uptime")
    local_store_uptime = get_local_store_uptime(store_uptime, Timezone_data)
    print("Got local store uptime")
    get_business_hours_overlap(BusinessHours_data, max_timestamp, local_store_uptime)

def get_store_uptime(Store_data):
    store_list = Store_data["store_id"].unique().tolist()
    store_active={}
    store_uptime={}
    c=0
    for i in store_list:
        c=c+1
        if(c==10):
            break
        temp_df=pd.DataFrame(Store_data[Store_data["store_id"]==i])
        temp_df.sort_values(by=["timestamp_utc"])
        active_time=[]
        for j, row in temp_df.iterrows():
            date=services.process_timestamp(row["timestamp_utc"]).date()
            time=services.process_timestamp(row["timestamp_utc"]).time()
            active_time.append([date,time])
        store_active[i]=active_time
        date_uptime={}
        for k in store_active[i]:
            if k[0] not in date_uptime:
                date_uptime[k[0]]=[k[1],k[1]]
            else:
                if k[1]<date_uptime[k[0]][0]:
                    date_uptime[k[0]][0]=k[1]
                if k[1]>date_uptime[k[0]][1]:
                    date_uptime[k[0]][1]=k[1]
        store_uptime[i]=date_uptime
    return store_uptime

def get_local_store_uptime(store_uptime, Timezone_data):
    timezone_fixed={}
    for i in store_uptime:
        timezone_fixed[i]={}
        for j in store_uptime[i]:
            tz = None
            if not Timezone_data[Timezone_data["store_id"]==i]["timezone_str"].empty:
                tz = Timezone_data[Timezone_data["store_id"]==i]["timezone_str"].to_string()
                l_tz = tz.split()
                tz = l_tz[1]
            else:
                tz = ""
            start = services.convert_timezone(datetime.combine(j,store_uptime[i][j][1]), tz)
            end = services.convert_timezone(datetime.combine(j,store_uptime[i][j][0]), tz)
            timezone_fixed[i][j]=[start.time(),end.time()]
    return timezone_fixed

def get_business_hours_overlap(BusinessHours_data, max_timestamp, local_store_uptime):
    last_hour = max_timestamp - timedelta(hours=1)
    last_day = max_timestamp - timedelta(days=1)
    store_list = local_store_uptime.keys()
    report={}
    print(store_list)
    for i in store_list:
        store_report={}
        uptimes = local_store_uptime[i]
        for dates in uptimes:
            if dates == last_hour.date():
                store_start_time, store_end_time = uptimes[dates][0], uptimes[dates][1]
                day_now = max_timestamp.weekday()
                bh_start_time, bh_end_time = None, None
                try:
                    ls_temp = BusinessHours_data[(BusinessHours_data["store_id" == i]) & (BusinessHours_data["day" == day_now])]["start_time_local"].to_string()
                    bh_start_time = datetime.combine(max_timestamp.date(),services.process_time(ls_temp[1]))
                    le_temp = BusinessHours_data[(BusinessHours_data["store_id" == i]) & (BusinessHours_data["day" == day_now])]["end_time_local"].to_string()
                    bh_end_time = datetime.combine(max_timestamp.date(),services.process_time(le_temp[1]))
                except:
                    bh_start_time, bh_end_time = last_hour, max_timestamp
                start_point, end_point = None, None
                if bh_end_time < last_hour or bh_start_time > max_timestamp:
                    store_report["last_hour_uptime"] = 0
                else:
                    if bh_start_time < last_hour:
                        start_point = last_hour
                    else:
                        start_point = bh_start_time
                    if bh_end_time > max_timestamp:
                        end_point = max_timestamp
                    else:
                        end_point = bh_end_time
                store_start_time = datetime.combine(max_timestamp.date(), store_start_time)
                store_end_time = datetime.combine(max_timestamp.date(), store_end_time)
                start = store_start_time if store_start_time > start_point else start_point
                end = store_end_time if store_end_time < end_point else end_point
                store_report["last_hour_uptime"] = end - start
        report[i] = store_report
    print(report)
    
