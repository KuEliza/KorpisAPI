from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional
from decimal import Decimal


# Equipment Service Status schemas
class EquipmentServiceStatusBase(BaseModel):
    id: str
    name: str

class EquipmentServiceStatusCreate(EquipmentServiceStatusBase):
    pass

class EquipmentServiceStatus(EquipmentServiceStatusBase):
    class Config:
        from_attributes = True


# Coffee Product Type schemas
class CoffeeProductTypeBase(BaseModel):
    name: str


class CoffeeProductTypeCreate(CoffeeProductTypeBase):
    pass


class CoffeeProductType(CoffeeProductTypeBase):
    id: str

    class Config:
        from_attributes = True


# Department schemas
class DepartmentBase(BaseModel):
    name: str
    manager_id: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    id: str


class Department(DepartmentBase):
    id: str

    class Config:
        from_attributes = True


# Workplace schemas
class WorkplaceBase(BaseModel):
    location: str
    equipment_details: Optional[str] = None
    equipment_status_id: str


class WorkplaceCreate(WorkplaceBase):
    id: str


class Workplace(WorkplaceBase):
    id: str

    class Config:
        from_attributes = True

# Employee schemas
class EmployeeBase(BaseModel):
    department_id: str
    full_name: str
    position: str
    workplace_id: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class EmployeeCreate(EmployeeBase):
    id: str
    hire_date: date


class Employee(EmployeeBase):
    id: str
    hire_date: date

    class Config:
        from_attributes = True


# Project schemas
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None


class ProjectCreate(ProjectBase):
    id: str


class Project(ProjectBase):
    id: str

    class Config:
        from_attributes = True


# Client schemas
class ClientBase(BaseModel):
    favorite_coffee_type_id: str
    full_name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class ClientCreate(ClientBase):
    id: str


class Client(ClientBase):
    id: str

    class Config:
        from_attributes = True


# Business Process schemas
class BusinessProcessBase(BaseModel):
    responsible_employee_id: str
    name: str
    description: Optional[str] = None
    project_id: str

class BusinessProcessCreate(BusinessProcessBase):
    id: str

class BusinessProcess(BusinessProcessBase):
    id: str

    class Config:
        from_attributes = True


# Purchase schemas
class PurchaseBase(BaseModel):
    employee_id: str
    date: date
    supplier: str
    amount: Decimal
    coffee_product_type_id: str


class PurchaseCreate(PurchaseBase):
    id: str


class Purchase(PurchaseBase):
    id: str

    class Config:
        from_attributes = True


# Service Request schemas
class ServiceRequestBase(BaseModel):
    employee_id: str
    request_date: date
    description: str
    workplace_id: str
    status_id: str


class ServiceRequestCreate(ServiceRequestBase):
    id: str


class ServiceRequest(ServiceRequestBase):
    id: str

    class Config:
        from_attributes = True


class DepartmentWithManager(Department):
    manager: Optional['Employee'] = None

    class Config:
        from_attributes = True


class EmployeeWithDetails(Employee):
    department: Optional['Department'] = None
    workplace: Optional['Workplace'] = None

    class Config:
        from_attributes = True


class WorkplaceWithStatus(Workplace):
    equipment_status: Optional['EquipmentServiceStatus'] = None

    class Config:
        from_attributes = True


class ClientWithCoffeeType(Client):
    favorite_coffee_type: Optional['CoffeeProductType'] = None

    class Config:
        from_attributes = True


class PurchaseWithDetails(Purchase):
    employee: Optional['Employee'] = None
    coffee_product_type: Optional['CoffeeProductType'] = None

    class Config:
        from_attributes = True


class BusinessProcessWithDetails(BusinessProcess):
    responsible_employee: Optional['Employee'] = None
    project: Optional['Project'] = None

    class Config:
        from_attributes = True


class ServiceRequestWithDetails(ServiceRequest):
    employee: Optional['Employee'] = None
    workplace: Optional['Workplace'] = None
    status: Optional['EquipmentServiceStatus'] = None

    class Config:
        from_attributes = True


class ProjectWithBusinessProcesses(Project):
    business_processes: list['BusinessProcess'] = []

    class Config:
        from_attributes = True