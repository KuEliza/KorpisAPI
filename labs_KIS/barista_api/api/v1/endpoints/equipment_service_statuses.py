from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud
import schemas
from database import SessionLocal

router = APIRouter(prefix="/equipment_service_statuses", tags=["Статусы оборудования"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.EquipmentServiceStatus])
def read_equipment_service_statuses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    statuses = crud.get_equipment_service_statuses(db, skip=skip, limit=limit)
    return statuses

@router.get("/{status_id}", response_model=schemas.EquipmentServiceStatus)
def read_equipment_service_status(status_id: str, db: Session = Depends(get_db)):
    db_status = crud.get_equipment_service_status(db, status_id=status_id)
    if db_status is None:
        raise HTTPException(status_code=404, detail="Статус оборудования не найден")
    return db_status