from fastapi import APIRouter

from barista_api.api.v1.endpoints import (
    business_processes,
    clients,
    coffee_product_types,
    departments,
    employees,
    equipment_service_statuses,
    projects,
    purchases,
    service_requests,
    workplaces,
    etl
)

api_router = APIRouter()

api_router.include_router(business_processes.router)
api_router.include_router(clients.router)
api_router.include_router(coffee_product_types.router)
api_router.include_router(departments.router)
api_router.include_router(employees.router)
api_router.include_router(equipment_service_statuses.router)
api_router.include_router(projects.router)
api_router.include_router(purchases.router)
api_router.include_router(service_requests.router)
api_router.include_router(workplaces.router)
api_router.include_router(etl.router)
