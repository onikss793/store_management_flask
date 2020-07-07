from database import get_db_connection
from services import StoreService, EmployeeService, BrandService
from .data import store_data, employee_data, brand_data


def setup_brands():
    connection = get_db_connection()

    brand_service = BrandService(connection)

    for brand in brand_data:
        result = brand_service.create_brand(brand_name=brand['brand_name'])

        if not result:
            connection.rollback()
            break

    connection.commit()
    connection.close()


def setup_stores():
    connection = get_db_connection()

    store_service = StoreService(connection)

    for store in store_data:
        result = store_service.create_store(store_data=store)

        if not result:
            connection.rollback()
            break

    connection.commit()
    connection.close()


def setup_employees():
    connection = get_db_connection()

    employee_service = EmployeeService(connection)

    for employee in employee_data:
        result = employee_service.create_employee(employee_data=employee)

        if not result:
            connection.rollback()
            break

    connection.commit()
    connection.close()
