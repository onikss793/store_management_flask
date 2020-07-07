from pymysql import cursors


class EmployeeDao:
    def __init__(self, connection):
        self.cursor = connection.cursor

    def create_one(self, store_id: int, employee_name: str, phone_number: str):
        with self.cursor(cursors.DictCursor) as cursor:
            return cursor.execute('''
                INSERT INTO employees (
                    store_id,
                    employee_name,
                    phone_number
                ) VALUES (
                    %(store_id)s,
                    %(employee_name)s,
                    %(phone_number)s
                )
            ''', {
                'store_id': store_id,
                'employee_name': employee_name,
                'phone_number': phone_number
            })

    def create_vacation(self, employee_id: int, start_at: str, finish_at: str):
        with self.cursor() as cursor:
            return cursor.execute('''
                INSERT INTO vacations (
                    employee_id,
                    start_at,
                    finish_at
                ) VALUES (
                    %(employee_id)s,
                    %(start_at)s,
                    %(finish_at)s
                )
            ''', {
                'employee_id': employee_id,
                'start_at': start_at,
                'finish_at': finish_at
            })

    def get_employee_list_by_store_id(self, store_id: int):
        with self.cursor(cursors.DictCursor) as cursor:
            cursor.execute('''
                SELECT
                    EMPLOYEE.id AS id,
                    EMPLOYEE.employee_name AS employee_name,
                    EMPLOYEE.phone_number AS phone_number,
                    EMPLOYEE.created_at AS created_at,
                    EMPLOYEE.updated_at AS updated_at,
                    STORE.id AS store_id,
                    STORE.store_name AS store_name,
                    STORE.created_at AS store_created_at,
                    STORE.updated_at AS store_updated_at
                FROM employees AS EMPLOYEE
                LEFT JOIN stores AS STORE ON (EMPLOYEE.store_id = STORE.id)
                WHERE EMPLOYEE.store_id = %(store_id)s 
                AND EMPLOYEE.deleted_at IS NULL
                AND STORE.deleted_at IS NULL
            ''', {'store_id': store_id})

            return cursor.fetchall()
