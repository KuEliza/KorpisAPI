from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import crud
import schemas
from database import SessionLocal

router = APIRouter(prefix="/business_processes", tags=["Бизнес-процессы"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.BusinessProcess, status_code=status.HTTP_201_CREATED)
def create_business_process(business_process: schemas.BusinessProcessCreate, db: Session = Depends(get_db)):
    return crud.create_business_process(db=db, business_process=business_process)

@router.get("/{process_id}", response_model=schemas.BusinessProcess)
def read_business_process(process_id: str, db: Session = Depends(get_db)):
    db_process = crud.get_business_process(db, process_id=process_id)
    if db_process is None:
        raise HTTPException(status_code=404, detail="Бизнес-процесс не найден")
    return db_process

@router.get("/", response_model=List[schemas.BusinessProcess])
def read_business_processes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    processes = crud.get_business_processes(db, skip=skip, limit=limit)
    return processes

@router.put("/{process_id}", response_model=schemas.BusinessProcess)
def update_business_process(process_id: str, business_process: schemas.BusinessProcessCreate, db: Session = Depends(get_db)):
    db_process = crud.get_business_process(db, process_id=process_id)
    if db_process is None:
        raise HTTPException(status_code=404, detail="Бизнес-процесс не найден")
    return crud.update_business_process(db=db, process_id=process_id, business_process=business_process)

@router.delete("/{process_id}", response_model=schemas.BusinessProcess)
def delete_business_process(process_id: str, db: Session = Depends(get_db)):
    db_process = crud.get_business_process(db, process_id=process_id)
    if db_process is None:
        raise HTTPException(status_code=404, detail="Бизнес-процесс не найден")
    return crud.delete_business_process(db=db, process_id=process_id)