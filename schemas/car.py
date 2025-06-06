from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime




class SCarBase(BaseModel):
    brand: str
    model: str
    year: int


class SCarCreate(SCarBase):
    images: List[str]


class SCarImage(BaseModel):
    image_url: str


class SDamageReport(BaseModel):
    damage_description: str
    current_damage_coef: float
    historical_damage_coef: float

    model_config = ConfigDict(from_attributes=True)