from pydantic import BaseModel

class HouseBase(BaseModel):
    bedrooms: int
    bathrooms: float
    sqft_living: int
    price: float

class HouseCreate(HouseBase):
    pass

class House(HouseBase):
    id: int

    class Config:
        orm_mode = True