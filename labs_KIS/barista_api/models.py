from sqlalchemy import Column, String, Integer, ForeignKey, Date, DECIMAL, Text, func
from sqlalchemy.orm import relationship
from database import Base


# Справочник статусов оборудования
class EquipmentServiceStatus(Base):
    __tablename__ = 'equipment_service_statuses'

    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

    # Связи
    workplaces = relationship("Workplace", back_populates="equipment_status")
    service_requests = relationship("ServiceRequest", back_populates="status")


# Справочник типов кофейной продукции
class CoffeeProductType(Base):
    __tablename__ = 'coffee_product_types'

    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

    # Связи
    clients = relationship("Client", back_populates="favorite_coffee_type")
    purchases = relationship("Purchase", back_populates="coffee_product_type")


# Сотрудники
class Employee(Base):
    __tablename__ = 'employees'

    id = Column(String(50), primary_key=True)
    department_id = Column(String(50), ForeignKey('departments.id'), nullable=False)
    full_name = Column(String(150), nullable=False)
    position = Column(String(100), nullable=False)
    workplace_id = Column(String(50), ForeignKey('workplaces.id'), nullable=False)
    hire_date = Column(Date, nullable=False, default=func.current_date())
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)



# Отделы компании
class Department(Base):
    __tablename__ = 'departments'

    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    manager_id = Column(String(50), ForeignKey('employees.id'), nullable=True)

    # Связи
    employees = relationship("Employee",
                             back_populates="department",
                             foreign_keys="Employee.department_id")

    manager = relationship("Employee",
                           foreign_keys=[manager_id],
                           remote_side="Employee.id",
                           back_populates="managed_department")


# Рабочие места
class Workplace(Base):
    __tablename__ = 'workplaces'

    id = Column(String(50), primary_key=True)
    location = Column(String(200), nullable=False)
    equipment_details = Column(Text, nullable=True)
    equipment_status_id = Column(String(50), ForeignKey('equipment_service_statuses.id'), nullable=False)

    # Связи
    equipment_status = relationship("EquipmentServiceStatus", back_populates="workplaces")
    employees = relationship("Employee", back_populates="workplace")
    service_requests = relationship("ServiceRequest", back_populates="workplace")


# Проекты
class Project(Base):
    __tablename__ = 'projects'

    id = Column(String(50), primary_key=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False, default=func.current_date())
    end_date = Column(Date, nullable=True)

    # Связи
    business_processes = relationship("BusinessProcess", back_populates="project")


# Клиенты
class Client(Base):
    __tablename__ = 'clients'

    id = Column(String(50), primary_key=True)
    favorite_coffee_type_id = Column(String(50), ForeignKey('coffee_product_types.id'), nullable=False)
    full_name = Column(String(150), nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)

    # Связи
    favorite_coffee_type = relationship("CoffeeProductType", back_populates="clients")


# Бизнес-процессы
class BusinessProcess(Base):
    __tablename__ = 'business_processes'

    id = Column(String(50), primary_key=True)
    responsible_employee_id = Column(String(50), ForeignKey('employees.id'), nullable=False)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    project_id = Column(String(50), ForeignKey('projects.id'), nullable=False)

    # Связи
    responsible_employee = relationship("Employee", back_populates="business_processes")
    project = relationship("Project", back_populates="business_processes")


# Закупки
class Purchase(Base):
    __tablename__ = 'purchases'

    id = Column(String(50), primary_key=True)
    employee_id = Column(String(50), ForeignKey('employees.id'), nullable=False)
    date = Column(Date, nullable=False, default=func.current_date())
    supplier = Column(String(150), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    coffee_product_type_id = Column(String(50), ForeignKey('coffee_product_types.id'), nullable=False)

    # Связи
    employee = relationship("Employee", back_populates="purchases")
    coffee_product_type = relationship("CoffeeProductType", back_populates="purchases")


# Заявки на обслуживание
class ServiceRequest(Base):
    __tablename__ = 'service_requests'

    id = Column(String(50), primary_key=True)
    employee_id = Column(String(50), ForeignKey('employees.id'), nullable=False)
    request_date = Column(Date, nullable=False, default=func.current_date())
    description = Column(Text, nullable=False)
    workplace_id = Column(String(50), ForeignKey('workplaces.id'), nullable=False)
    status_id = Column(String(50), ForeignKey('equipment_service_statuses.id'), nullable=False)

    # Связи
    employee = relationship("Employee", back_populates="service_requests")
    workplace = relationship("Workplace", back_populates="service_requests")
    status = relationship("EquipmentServiceStatus", back_populates="service_requests")


#связи для Employee
Employee.department = relationship("Department",
                                   back_populates="employees",
                                   foreign_keys=[Employee.department_id])

Employee.workplace = relationship("Workplace", back_populates="employees")
Employee.managed_department = relationship("Department",
                                           back_populates="manager",
                                           foreign_keys=[Department.manager_id],
                                           uselist=False)
Employee.purchases = relationship("Purchase", back_populates="employee")
Employee.service_requests = relationship("ServiceRequest", back_populates="employee")
Employee.business_processes = relationship("BusinessProcess", back_populates="responsible_employee")