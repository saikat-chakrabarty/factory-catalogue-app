from typing import List
from pydantic import BaseModel

# Schema for a RawMaterial.
class RawMaterialBase(BaseModel):
    name: str

class RawMaterialResponse(RawMaterialBase):
    id: int

    class Config:
        from_attributes = True

# Shared fields for Factory.
class FactoryBase(BaseModel):
    name: str
    location: str
    product: str

# For creating a factory, raw_materials is a list of names.
class FactoryCreate(FactoryBase):
    raw_materials: List[str]

# For responses, include raw_materials details.
class FactoryResponse(FactoryBase):
    id: int
    raw_materials: List[RawMaterialResponse]

    class Config:
        from_attributes = True
