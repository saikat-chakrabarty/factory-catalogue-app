from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

# Association table for many-to-many relationship between factories and raw materials.
factory_raw_material_association = Table(
    'factory_raw_material',
    Base.metadata,
    Column('factory_id', Integer, ForeignKey('factories.id'), index=True),
    Column('raw_material_id', Integer, ForeignKey('raw_materials.id'), index=True)
)

class Factory(Base):
    __tablename__ = "factories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    location = Column(String, index=True, nullable=False)
    # Products still stored as an array of strings.
    product = Column(String, index=True, nullable=False)
    # Many-to-many relationship to RawMaterial.
    raw_materials = relationship(
        "RawMaterial",
        secondary=factory_raw_material_association,
        backref="factories"
    )

class RawMaterial(Base):
    __tablename__ = "raw_materials"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
