from fastapi import FastAPI, Depends
import models, schema, services, report
from database import SessionLocal, engine
from sqlalchemy.orm import Session

models.Base.metadata.drop_all(bind=engine, checkfirst=True)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root(db: Session = Depends(get_db)):
    #output_timezone = await services.get_timezone_data(db)
    #output_store = await services.get_store_data(db)
    #output_businesshour = await services.get_businesshour_data(db)
    output = await report.generate_report_from_csv()
    print(output)
    return {"message": "Hello World"}
