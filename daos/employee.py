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

    def get_duplicated_vacation(self, employee_id: int, start_at: str, finish_at: str):
        with self.cursor() as cursor:
            cursor.execute('''
                SELECT
                    id
                FROM vacations
                WHERE employee_id = %(employee_id)s
                AND start_at BETWEEN %(start_at)s AND %(finish_at)s
                OR finish_at BETWEEN %(start_at)s AND %(finish_at)s
                AND deleted_at IS NULL
            ''', {'employee_id': employee_id, 'start_at': start_at, 'finish_at': finish_at})

            return cursor.fetchone()

    def get_employee_list_by_store_id(self, store_id: int, date: str):
        with self.cursor(cursors.DictCursor) as cursor:
            cursor.execute('''
                SELECT
                    EMPLOYEE.id AS id,
                    EMPLOYEE.employee_name AS employee_name,
                    EMPLOYEE.phone_number AS phone_number,
                    EMPLOYEE.created_at AS created_at,
                    EMPLOYEE.updated_at AS updated_at,
                    IF(VACATION.id IS NOT NULL, 1, 0) AS vacation
                FROM employees AS EMPLOYEE
                LEFT JOIN vacations AS VACATION 
                    ON (EMPLOYEE.id = VACATION.employee_id 
                    AND %(date)s BETWEEN start_at AND finish_at)
                WHERE EMPLOYEE.store_id = %(store_id)s 
                AND EMPLOYEE.deleted_at IS NULL
                AND VACATION.deleted_at IS NULL
            ''', {'store_id': store_id, 'date': date})

            return cursor.fetchall()

    def update_employee(self, employee_id, store_id, employee_name, phone_number):
        with self.cursor() as cursor:
            return cursor.execute('''
                UPDATE employees
                SET employee_name = %(employee_name)s,
                    phone_number = %(phone_number)s,
                    store_id = %(store_id)s
                WHERE id = %(employee_id)s
                AND deleted_at IS NULL
            ''', {
                'employee_id': employee_id,
                'store_id': store_id,
                'employee_name': employee_name,
                'phone_number': phone_number
            })

    def delete_employee(self, employee_id, store_id):
        with self.cursor() as cursor:
            return cursor.execute('''
                UPDATE employees
                SET deleted_at = CURRENT_TIMESTAMP
                WHERE id = %(employee_id)s
                AND store_id = %(store_id)s
            ''', {'employee_id': employee_id, 'store_id': store_id})
