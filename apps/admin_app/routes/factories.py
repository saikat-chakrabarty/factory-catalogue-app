from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from libs.catalogue import models, schemas
from libs.catalogue.db import get_db

import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/factories", tags=["Factories Admin"])

@router.post("/", response_model=schemas.FactoryResponse)
def create_factory(factory: schemas.FactoryCreate, db: Session = Depends(get_db)):
    """
    Admin endpoint: Add a new factory.
    """
    logging.debug(f"Request body: {factory}")

    # Check for mandatory fields.
    if not factory.name or not factory.location or not factory.product or not factory.raw_materials:
        logging.error("Mandsary fields missing: Name, location, product and raw materials are required")
        raise HTTPException(
            status_code=400, detail="Name, location, product and raw materials are required"
    )

    # Check if a factory with the same name already exists.
    existing = (
        db.query(models.Factory).filter(models.Factory.name == factory.name).first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Factory already exists")

    # Process raw materials: for each raw material name, check if it exists.
    raw_materials_list = []
    for rm_name in factory.raw_materials:
        rm = (
            db.query(models.RawMaterial)
            .filter(models.RawMaterial.name == rm_name)
            .first()
        )
        if not rm:
            rm = models.RawMaterial(name=rm_name)
            db.add(rm)
            # Flush so that the new raw material gets an ID.
            db.flush()
        raw_materials_list.append(rm)

    new_factory = models.Factory(
        name=factory.name,
        location=factory.location,
        product=factory.product,
        raw_materials=raw_materials_list,
    )
    db.add(new_factory)
    db.commit()
    db.refresh(new_factory)
    logging.info(f"Factory created: {new_factory.id}")
    
    return new_factory
