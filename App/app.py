from fastapi import FastAPI, Depends, BackgroundTasks
import models, schema, services, report
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import uuid
import redis

models.Base.metadata.drop_all(bind=engine, checkfirst=True)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def redis_connect() -> redis.client.Redis:
    try:
        client = redis.Redis(
            host="localhost",
            port=6379,
            db=0,
        )
        ping = client.ping()
        if ping is True:
            return client
    except redis.ConnectionError:
        print("Connection Error!")

client = redis_connect()

@app.get("/")
async def root(db: Session = Depends(get_db)):
    #output_timezone = await services.get_timezone_data(db)
    #output_store = await services.get_store_data(db)
    #output_businesshour = await services.get_businesshour_data(db)
    return {"message": "Hello World! Everything works"}

@app.get("/trigger_report")
async def trigger_report(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    report_uuid = str(uuid.uuid4())
    background_tasks.add_task(report.generate_report_from_csv, db, report_uuid, client)
    return {"message": "Report will be generated and uploaded to DB", "report_id": report_uuid}

@app.get("/get_report/{report_id}")
async def get_report(report_id: str):
    report = client.get(report_id)
    print(report)
    if report:
        return {"message": "Report found", "report": report}
    else:
        return {"message": "Running"}
