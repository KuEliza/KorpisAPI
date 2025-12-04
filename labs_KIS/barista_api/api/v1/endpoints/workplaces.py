from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import crud
import schemas
from database import SessionLocal

router = APIRouter(prefix="/workplaces", tags=["Рабочие места"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Workplace, status_code=status.HTTP_201_CREATED)
def create_workplace(workplace: schemas.WorkplaceCreate, db: Session = Depends(get_db)):
    return crud.create_workplace(db=db, workplace=workplace)

@router.get("/{workplace_id}", response_model=schemas.Workplace)
def read_workplace(workplace_id: str, db: Session = Depends(get_db)):
    db_workplace = crud.get_workplace(db, workplace_id=workplace_id)
    if db_workplace is None:
        raise HTTPException(status_code=404, detail="Рабочее место не найдено")
    return db_workplace

@router.get("/", response_model=List[schemas.Workplace])
def read_workplaces(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    workplaces = crud.get_workplaces(db, skip=skip, limit=limit)
    return workplaces

@router.put("/{workplace_id}", response_model=schemas.Workplace)
def update_workplace(workplace_id: str, workplace: schemas.WorkplaceCreate, db: Session = Depends(get_db)):
    db_workplace = crud.get_workplace(db, workplace_id=workplace_id)
    if db_workplace is None:
        raise HTTPException(status_code=404, detail="Рабочее место не найдено")
    return crud.update_workplace(db=db, workplace_id=workplace_id, workplace=workplace)

@router.delete("/{workplace_id}", response_model=schemas.Workplace)
def delete_workplace(workplace_id: str, db: Session = Depends(get_db)):
    db_workplace = crud.get_workplace(db, workplace_id=workplace_id)
    if db_workplace is None:
        raise HTTPException(status_code=404, detail="Рабочее место не найдено")
    return crud.delete_workplace(db=db, workplace_id=workplace_id)