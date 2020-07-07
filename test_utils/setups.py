import re
from os import path

from pymysql import OperationalError, ProgrammingError

from database import get_db_connection
from services import StoreService, EmployeeService, BrandService, ReservationService
from .data import store_data, employee_data, brand_data, reservation_data


def setup_reservations():
    connection = get_db_connection()

    reservation_service = ReservationService(connection)

    try:
        for reservation in reservation_data:
            reservation_service.create_reservation(reservation)

        connection.commit()
    except Exception as error:
        print(error)
        connection.rollback()
    finally:
        connection.close()


def setup_brands():
    connection = get_db_connection()

    brand_service = BrandService(connection)

    try:
        for brand in brand_data:
            brand_service.create_brand(brand_name=brand['brand_name'])

        connection.commit()
    except Exception as error:
        print(error)
        connection.rollback()
    finally:
        connection.close()


def setup_stores():
    connection = get_db_connection()

    store_service = StoreService(connection)

    try:
        for store in store_data:
            store_service.create_store(store_data=store)

        connection.commit()
    except Exception as error:
        print(error)
        connection.rollback()

    finally:
        connection.close()


def setup_employees():
    connection = get_db_connection()

    employee_service = EmployeeService(connection)

    try:
        for employee in employee_data:
            employee_service.create_employee(employee_data=employee)

        connection.commit()
    except Exception as error:
        print(error)
        connection.rollback()
    finally:
        connection.close()


def exec_sql_file(cursor, sql_file):
    # print("\n[INFO] Executing SQL script file: '%s'" % sql_file)
    statement = ""

    for line in open(sql_file):
        if re.match(r'--', line):  # ignore sql comment lines
            continue
        if not re.search(r';$', line):  # keep appending lines that don't end in ';'
            statement = statement + line
        else:  # when you get a line ending in ';' then exec statement and reset for next statement
            statement = statement + line
            # print("\n[DEBUG] Executing SQL statement:%s" % statement)
            try:
                cursor.execute(statement)
            except (OperationalError, ProgrammingError) as e:
                print("\n[WARN] MySQLError during execute statement \n\tArgs: '%s'" % (str(e.args)))

            statement = ""


def sql_setup():
    connection = get_db_connection()
    cursor = connection.cursor()

    down = path.abspath('migrate/0.0.1.down.sql')
    up = path.abspath('migrate/0.0.1.up.sql')
    seed = path.abspath('migrate/0.0.1.seed.sql')

    exec_sql_file(cursor, down)
    exec_sql_file(cursor, up)
    exec_sql_file(cursor, seed)

    connection.commit()
    connection.close()


def sql_teardown():
    connection = get_db_connection()
    cursor = connection.cursor()

    down = path.abspath('migrate/0.0.1.down.sql')
    up = path.abspath('migrate/0.0.1.up.sql')

    exec_sql_file(cursor, down)
    exec_sql_file(cursor, up)

    connection.commit()
    connection.close()
