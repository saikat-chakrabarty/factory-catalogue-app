from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import or_
from sqlalchemy import and_

from libs.catalogue import models, schemas
from libs.catalogue.db import get_db

import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/factories", tags=["Factories Search"])

@router.get("/", response_model=List[schemas.FactoryResponse])
def search_factories(
    location: Optional[str] = None,
    raw_material: Optional[List[str]] = Query(None, alias="raw_material"),
    product: Optional[str] = Query(None, alias="product"),
    db: Session = Depends(get_db),
    ):
    """
    User endpoint: Search factories by location, raw material, or product.
    You can pass multiple `raw_material` and `product` query parameters.
    """
    logging.debug(f"Request body: location={location}, raw_material={raw_material}, product={product}")

    query = db.query(models.Factory)

    if location:
        query = query.filter(models.Factory.location.ilike(f"%{location}%"))

    if raw_material:
        # Filter factories that have at least one matching raw material name.
        query = query.filter(
            and_(
                *[
                    models.Factory.raw_materials.any(
                        models.RawMaterial.name.ilike(f"%{rm}%")
                    )
                    for rm in raw_material
                ]
            )
        )

    if product:
        query = query.filter(and_(models.Factory.product.ilike(f"%{product}%")))

    factories = query.all()
    logging.info(f"Found {len(factories)} factories")

    return factories
