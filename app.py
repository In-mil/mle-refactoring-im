# file: app.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import sessionmaker, declarative_base

app = FastAPI()
DATABASE_URL = "sqlite:///./houses.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- SQLAlchemy model
class House(Base):
    __tablename__ = "houses"
    id = Column(Integer, primary_key=True, index=True)
    bedrooms = Column(Integer)
    bathrooms = Column(Float)
    sqft_living = Column(Integer)
    grade = Column(Integer)
    price = Column(Float)

Base.metadata.create_all(bind=engine)

# --- Pydantic schema
class HouseCreate(BaseModel):
    bedrooms: int
    bathrooms: float
    sqft_living: int
    grade: int
    price: float

class HouseRead(HouseCreate):
    id: int

# --- CRUD Endpoints

@app.post("/houses/", response_model=HouseRead)
def create_house(house: HouseCreate):
    db = SessionLocal()
    db_house = House(**house.dict())
    db.add(db_house)
    db.commit()
    db.refresh(db_house)
    db.close()
    return db_house

@app.get("/houses/", response_model=List[HouseRead])
def read_houses():
    db = SessionLocal()
    houses = db.query(House).all()
    db.close()
    return houses

@app.get("/houses/{house_id}", response_model=HouseRead)
def read_house(house_id: int):
    db = SessionLocal()
    house = db.query(House).filter(House.id == house_id).first()
    db.close()
    if not house:
        raise HTTPException(status_code=404, detail="House not found")
    return house

@app.put("/houses/{house_id}", response_model=HouseRead)
def update_house(house_id: int, new_house: HouseCreate):
    db = SessionLocal()
    house = db.query(House).filter(House.id == house_id).first()
    if not house:
        db.close()
        raise HTTPException(status_code=404, detail="House not found")
    for key, value in new_house.dict().items():
        setattr(house, key, value)
    db.commit()
    db.refresh(house)
    db.close()
    return house

@app.delete("/houses/{house_id}", response_model=HouseRead)
def delete_house(house_id: int):
    db = SessionLocal()
    house = db.query(House).filter(House.id == house_id).first()
    if not house:
        db.close()
        raise HTTPException(status_code=404, detail="House not found")
    db.delete(house)
    db.commit()
    db.close()
    return house
#interactive documentation: http://localhost:8000/docs.