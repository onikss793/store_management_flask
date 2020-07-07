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

    def create_vacation(self, vacation_data):
        employee_id = vacation_data['employee_id']
        start_at = vacation_data['start_at']
        finish_at = vacation_data['finish_at']

        result = self.employee_dao.create_vacation(
            employee_id=employee_id,
            start_at=start_at,
            finish_at=finish_at
        )

        return True if result else False

    def get_employee_list_by_store_id(self, store_id):
        employee_list = self.employee_dao.get_employee_list_by_store_id(store_id)

        return [{
            'id': employee['id'],
            'employee_name': employee['employee_name'],
            'phone_number': employee['phone_number'],
            'created_at': employee['created_at'],
            'updated_at': employee['updated_at'],
            'store': {
                'id': employee['store_id'],
                'store_name': employee['store_name'],
                'created_at': employee['store_created_at'],
                'updated_at': employee['store_updated_at']
            }
        } for employee in employee_list] if employee_list else []
