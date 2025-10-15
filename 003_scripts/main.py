from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Beispiel-Endpunkt zum Abrufen von Daten
@app.get("/houses/", response_model=list[schemas.House])
def get_houses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.House).offset(skip).limit(limit).all()