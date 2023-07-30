from fastapi import FastAPI, Depends
import services
import models, schema
from database import SessionLocal, engine
from sqlalchemy.orm import Session

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
    output = await services.get_data(db)
    print(output)
    return {"message": "Hello World"}
