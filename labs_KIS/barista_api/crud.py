from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas
import logging


logger = logging.getLogger("coffee_business_api")


# Equipment Service Status CRUD
def get_equipment_service_statuses(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Получение списка статусов оборудования, пропуск={skip}, лимит={limit}")
    return db.query(models.EquipmentServiceStatus).order_by(models.EquipmentServiceStatus.name).offset(skip).limit(limit).all()

def get_equipment_service_status(db: Session, status_id: str):
    logger.info(f"Получение статуса оборудования по ID: {status_id}")
    return db.query(models.EquipmentServiceStatus).filter(models.EquipmentServiceStatus.id == status_id).first()


# Coffee Product Type CRUD (только чтение)
def get_coffee_product_types(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Получение списка типов кофейной продукции, пропуск={skip}, лимит={limit}")
    return db.query(models.CoffeeProductType).order_by(models.CoffeeProductType.name).offset(skip).limit(limit).all()

def get_coffee_product_type(db: Session, coffee_type_id: str):
    logger.info(f"Получение типа кофейной продукции по ID: {coffee_type_id}")
    return db.query(models.CoffeeProductType).filter(models.CoffeeProductType.id == coffee_type_id).first()


# Department CRUD
def get_departments(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Получение списка отделов, пропуск={skip}, лимит={limit}")
    return db.query(models.Department).order_by(models.Department.name).offset(skip).limit(limit).all()


def get_department(db: Session, department_id: str):
    logger.info(f"Получение отдела по ID: {department_id}")
    return db.query(models.Department).filter(models.Department.id == department_id).first()


def create_department(db: Session, department: schemas.DepartmentCreate):
    logger.info(f"Создание отдела: {department.name}")
    db_department = models.Department(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    logger.info(f"Создан отдел с ID: {db_department.id}")
    return db_department


def update_department(db: Session, department_id: str, department: schemas.DepartmentCreate):
    logger.info(f"Обновление отдела с ID: {department_id}")
    db_department = db.query(models.Department).filter(models.Department.id == department_id).first()
    if db_department:
        for key, value in department.dict().items():
            setattr(db_department, key, value)
        db.commit()
        db.refresh(db_department)
        logger.info(f"Обновлен отдел с ID: {department_id}")
    else:
        logger.warning(f"Отдел с ID: {department_id} не найден")
    return db_department


def delete_department(db: Session, department_id: str):
    logger.info(f"Удаление отдела с ID: {department_id}")
    db_department = db.query(models.Department).filter(models.Department.id == department_id).first()
    if db_department:
        db.delete(db_department)
        db.commit()
        logger.info(f"Удален отдел с ID: {department_id}")
    else:
        logger.warning(f"Отдел с ID: {department_id} не найден")
    return db_department


# Workplace CRUD
def get_workplaces(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Получение списка рабочих мест, пропуск={skip}, лимит={limit}")
    return db.query(models.Workplace).order_by(models.Workplace.location).offset(skip).limit(limit).all()


def get_workplace(db: Session, workplace_id: str):
    logger.info(f"Получение рабочего места по ID: {workplace_id}")
    return db.query(models.Workplace).filter(models.Workplace.id == workplace_id).first()


def create_workplace(db: Session, workplace: schemas.WorkplaceCreate):
    logger.info(f"Создание рабочего места в локации: {workplace.location}")
    db_workplace = models.Workplace(**workplace.dict())
    db.add(db_workplace)
    db.commit()
    db.refresh(db_workplace)
    logger.info(f"Создано рабочее место с ID: {db_workplace.id}")
    return db_workplace


def update_workplace(db: Session, workplace_id: str, workplace: schemas.WorkplaceCreate):
    logger.info(f"Обновление рабочего места с ID: {workplace_id}")
    db_workplace = db.query(models.Workplace).filter(models.Workplace.id == workplace_id).first()
    if db_workplace:
        for key, value in workplace.dict().items():
            setattr(db_workplace, key, value)
        db.commit()
        db.refresh(db_workplace)
        logger.info(f"Обновлено рабочее место с ID: {workplace_id}")
    else:
        logger.warning(f"Рабочее место с ID: {workplace_id} не найдено")
    return db_workplace


def delete_workplace(db: Session, workplace_id: str):
    logger.info(f"Удаление рабочего места с ID: {workplace_id}")
    db_workplace = db.query(models.Workplace).filter(models.Workplace.id == workplace_id).first()
    if db_workplace:
        db.delete(db_workplace)
        db.commit()
        logger.info(f"Удалено рабочее место с ID: {workplace_id}")
    else:
        logger.warning(f"Рабочее место с ID: {workplace_id} не найдено")
    return db_workplace


# Employee CRUD
def get_employees(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Получение списка сотрудников, пропуск={skip}, лимит={limit}")
    return db.query(models.Employee).order_by(models.Employee.full_name).offset(skip).limit(limit).all()


def get_employee(db: Session, employee_id: str):
    logger.info(f"Получение сотрудника по ID: {employee_id}")
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()


def create_employee(db: Session, employee: schemas.EmployeeCreate):
    logger.info(f"Создание сотрудника: {employee.full_name}")
    db_employee = models.Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    logger.info(f"Создан сотрудник с ID: {db_employee.id}")
    return db_employee


def update_employee(db: Session, employee_id: str, employee: schemas.EmployeeCreate):
    logger.info(f"Обновление сотрудника с ID: {employee_id}")
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if db_employee:
        for key, value in employee.dict().items():
            setattr(db_employee, key, value)
        db.commit()
        db.refresh(db_employee)
        logger.info(f"Обновлен сотрудник с ID: {employee_id}")
    else:
        logger.warning(f"Сотрудник с ID: {employee_id} не найден")
    return db_employee


def delete_employee(db: Session, employee_id: str):
    logger.info(f"Удаление сотрудника с ID: {employee_id}")
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if db_employee:
        db.delete(db_employee)
        db.commit()
        logger.info(f"Удален сотрудник с ID: {employee_id}")
    else:
        logger.warning(f"Сотрудник с ID: {employee_id} не найден")
    return db_employee


# Project CRUD
def get_projects(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Получение списка проектов, пропуск={skip}, лимит={limit}")
    return db.query(models.Project).order_by(models.Project.start_date.desc()).offset(skip).limit(limit).all()


def get_project(db: Session, project_id: str):
    logger.info(f"Получение проекта по ID: {project_id}")
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def create_project(db: Session, project: schemas.ProjectCreate):
    logger.info(f"Создание проекта: {project.name}")
    db_project = models.Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    logger.info(f"Создан проект с ID: {db_project.id}")
    return db_project


def update_project(db: Session, project_id: str, project: schemas.ProjectCreate):
    logger.info(f"Обновление проекта с ID: {project_id}")
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project:
        for key, value in project.dict().items():
            setattr(db_project, key, value)
        db.commit()
        db.refresh(db_project)
        logger.info(f"Обновлен проект с ID: {project_id}")
    else:
        logger.warning(f"Проект с ID: {project_id} не найден")
    return db_project


def delete_project(db: Session, project_id: str):
    logger.info(f"Удаление проекта с ID: {project_id}")
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project:
        db.delete(db_project)
        db.commit()
        logger.info(f"Удален проект с ID: {project_id}")
    else:
        logger.warning(f"Проект с ID: {project_id} не найден")
    return db_project


# Client CRUD
def get_clients(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Получение списка клиентов, пропуск={skip}, лимит={limit}")
    return db.query(models.Client).order_by(models.Client.full_name).offset(skip).limit(limit).all()


def get_client(db: Session, client_id: str):
    logger.info(f"Получение клиента по ID: {client_id}")
    return db.query(models.Client).filter(models.Client.id == client_id).first()


def create_client(db: Session, client: schemas.ClientCreate):
    logger.info(f"Создание клиента: {client.full_name}")
    db_client = models.Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    logger.info(f"Создан клиент с ID: {db_client.id}")
    return db_client


def update_client(db: Session, client_id: str, client: schemas.ClientCreate):
    logger.info(f"Обновление клиента с ID: {client_id}")
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if db_client:
        for key, value in client.dict().items():
            setattr(db_client, key, value)
        db.commit()
        db.refresh(db_client)
        logger.info(f"Обновлен клиент с ID: {client_id}")
    else:
        logger.warning(f"Клиент с ID: {client_id} не найден")
    return db_client


def delete_client(db: Session, client_id: str):
    logger.info(f"Удаление клиента с ID: {client_id}")
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if db_client:
        db.delete(db_client)
        db.commit()
        logger.info(f"Удален клиент с ID: {client_id}")
    else:
        logger.warning(f"Клиент с ID: {client_id} не найден")
    return db_client


# Business Process CRUD
def get_business_processes(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Получение списка бизнес-процессов, пропуск={skip}, лимит={limit}")
    return db.query(models.BusinessProcess).order_by(models.BusinessProcess.name).offset(skip).limit(limit).all()


def get_business_process(db: Session, process_id: str):
    logger.info(f"Получение бизнес-процесса по ID: {process_id}")
    return db.query(models.BusinessProcess).filter(models.BusinessProcess.id == process_id).first()


def create_business_process(db: Session, business_process: schemas.BusinessProcessCreate):
    logger.info(f"Создание бизнес-процесса: {business_process.name}")
    db_process = models.BusinessProcess(**business_process.dict())
    db.add(db_process)
    db.commit()
    db.refresh(db_process)
    logger.info(f"Создан бизнес-процесс с ID: {db_process.id}")
    return db_process


def update_business_process(db: Session, process_id: str, business_process: schemas.BusinessProcessCreate):
    logger.info(f"Обновление бизнес-процесса с ID: {process_id}")
    db_process = db.query(models.BusinessProcess).filter(models.BusinessProcess.id == process_id).first()
    if db_process:
        for key, value in business_process.dict().items():
            setattr(db_process, key, value)
        db.commit()
        db.refresh(db_process)
        logger.info(f"Обновлен бизнес-процесс с ID: {process_id}")
    else:
        logger.warning(f"Бизнес-процесс с ID: {process_id} не найден")
    return db_process


def delete_business_process(db: Session, process_id: str):
    logger.info(f"Удаление бизнес-процесса с ID: {process_id}")
    db_process = db.query(models.BusinessProcess).filter(models.BusinessProcess.id == process_id).first()
    if db_process:
        db.delete(db_process)
        db.commit()
        logger.info(f"Удален бизнес-процесс с ID: {process_id}")
    else:
        logger.warning(f"Бизнес-процесс с ID: {process_id} не найден")
    return db_process


# Purchase CRUD
def get_purchases(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Получение списка закупок, пропуск={skip}, лимит={limit}")
    return db.query(models.Purchase).order_by(models.Purchase.date.desc()).offset(skip).limit(limit).all()


def get_purchase(db: Session, purchase_id: str):
    logger.info(f"Получение закупки по ID: {purchase_id}")
    return db.query(models.Purchase).filter(models.Purchase.id == purchase_id).first()


def create_purchase(db: Session, purchase: schemas.PurchaseCreate):
    logger.info(f"Создание закупки от поставщика: {purchase.supplier}")
    db_purchase = models.Purchase(**purchase.dict())
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    logger.info(f"Создана закупка с ID: {db_purchase.id}")
    return db_purchase


def update_purchase(db: Session, purchase_id: str, purchase: schemas.PurchaseCreate):
    logger.info(f"Обновление закупки с ID: {purchase_id}")
    db_purchase = db.query(models.Purchase).filter(models.Purchase.id == purchase_id).first()
    if db_purchase:
        for key, value in purchase.dict().items():
            setattr(db_purchase, key, value)
        db.commit()
        db.refresh(db_purchase)
        logger.info(f"Обновлена закупка с ID: {purchase_id}")
    else:
        logger.warning(f"Закупка с ID: {purchase_id} не найдена")
    return db_purchase


def delete_purchase(db: Session, purchase_id: str):
    logger.info(f"Удаление закупки с ID: {purchase_id}")
    db_purchase = db.query(models.Purchase).filter(models.Purchase.id == purchase_id).first()
    if db_purchase:
        db.delete(db_purchase)
        db.commit()
        logger.info(f"Удалена закупка с ID: {purchase_id}")
    else:
        logger.warning(f"Закупка с ID: {purchase_id} не найдена")
    return db_purchase


# Service Request CRUD
def get_service_requests(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Получение списка заявок на обслуживание, пропуск={skip}, лимит={limit}")
    return db.query(models.ServiceRequest).order_by(models.ServiceRequest.request_date.desc()).offset(skip).limit(limit).all()


def get_service_request(db: Session, request_id: str):
    logger.info(f"Получение заявки на обслуживание по ID: {request_id}")
    return db.query(models.ServiceRequest).filter(models.ServiceRequest.id == request_id).first()


def create_service_request(db: Session, service_request: schemas.ServiceRequestCreate):
    logger.info(f"Создание заявки на обслуживание")
    db_request = models.ServiceRequest(**service_request.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    logger.info(f"Создана заявка на обслуживание с ID: {db_request.id}")
    return db_request


def update_service_request(db: Session, request_id: str, service_request: schemas.ServiceRequestCreate):
    logger.info(f"Обновление заявки на обслуживание с ID: {request_id}")
    db_request = db.query(models.ServiceRequest).filter(models.ServiceRequest.id == request_id).first()
    if db_request:
        for key, value in service_request.dict().items():
            setattr(db_request, key, value)
        db.commit()
        db.refresh(db_request)
        logger.info(f"Обновлена заявка на обслуживание с ID: {request_id}")
    else:
        logger.warning(f"Заявка на обслуживание с ID: {request_id} не найдена")
    return db_request


def delete_service_request(db: Session, request_id: str):
    logger.info(f"Удаление заявки на обслуживание с ID: {request_id}")
    db_request = db.query(models.ServiceRequest).filter(models.ServiceRequest.id == request_id).first()
    if db_request:
        db.delete(db_request)
        db.commit()
        logger.info(f"Удалена заявка на обслуживание с ID: {request_id}")
    else:
        logger.warning(f"Заявка на обслуживание с ID: {request_id} не найдена")
    return db_request