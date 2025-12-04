from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import crud
import schemas
from database import SessionLocal

router = APIRouter(prefix="/employees", tags=["Сотрудники"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Employee, status_code=status.HTTP_201_CREATED)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db=db, employee=employee)


@router.get("/{employee_id}", response_model=schemas.Employee)
def read_employee(employee_id: str, db: Session = Depends(get_db)):
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    return db_employee


@router.get("/", response_model=List[schemas.Employee])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    employees = crud.get_employees(db, skip=skip, limit=limit)
    return employees


@router.put("/{employee_id}", response_model=schemas.Employee)
def update_employee(employee_id: str, employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")

    # Проверка уникальности email (если указан и изменился)
    if employee.email and employee.email != db_employee.email:
        existing_employee = crud.get_employee_by_email(db, email=employee.email)
        if existing_employee and existing_employee.id != employee_id:
            raise HTTPException(status_code=400, detail="Сотрудник с таким email уже существует")

    return crud.update_employee(db=db, employee_id=employee_id, employee=employee)


@router.delete("/{employee_id}", response_model=schemas.Employee)
def delete_employee(employee_id: str, db: Session = Depends(get_db)):
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    return crud.delete_employee(db=db, employee_id=employee_id)