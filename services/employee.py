from datetime import datetime

from dateutil import parser

from daos import EmployeeDao


class EmployeeService:
    def __init__(self, connection):
        self.connection = connection
        self.employee_dao = EmployeeDao(connection)

    def create_employee(self, employee_data):
        store_id = employee_data['store_id']
        employee_name = employee_data['employee_name']
        phone_number = employee_data['phone_number']

        result = self.employee_dao.create_one(
            store_id=store_id,
            employee_name=employee_name,
            phone_number=phone_number
        )

        return True if result else False

    def get_employee_list_by_store_id(self, store_id, date):
        date = parser.isoparse(date).astimezone() if date else datetime.utcnow().isoformat()
        employee_list = self.employee_dao.get_employee_list_by_store_id(store_id, date)
        print(date)

        return [{
            'id': employee['id'],
            'employee_name': employee['employee_name'],
            'phone_number': employee['phone_number'],
            'vacation': bool(employee['vacation'])
        } for employee in employee_list] if employee_list else []

    def create_vacation(self, vacation_data):
        employee_id = vacation_data['employee_id']
        start_at = vacation_data['start_at']
        finish_at = vacation_data['finish_at']

        result = self.employee_dao.create_vacation(
            employee_id=employee_id,
            start_at=parser.isoparse(start_at).astimezone(),
            finish_at=parser.isoparse(finish_at).astimezone(),
        )

        return True if result else False

    def update_employee(self, employee_data: dict):
        store_id = employee_data['store_id']
        employee_id = employee_data['employee_id']
        employee_name = employee_data['employee_name']
        phone_number = employee_data['phone_number']

        result = self.employee_dao.update_employee(employee_id, store_id, employee_name, phone_number)

        return True if result else False

    def delete_employee_by_id_and_store_id(self, employee_id: int, store_id: int):
        result = self.employee_dao.delete_employee(employee_id, store_id)

        return True if result else False

    def check_duplicated_vacation(self, vacation_data):
        employee_id = vacation_data['employee_id']
        start_at = vacation_data['start_at']
        finish_at = vacation_data['finish_at']

        return self.employee_dao.get_duplicated_vacation(employee_id, start_at, finish_at)
