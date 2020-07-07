from flask import request, Blueprint, abort, g, jsonify

from database import get_db_connection
from services import EmployeeService
from utils import mutation_response, throw_error, check_request, authorization


class EmployeeView:
    employee_app = Blueprint('employee_app', __name__, url_prefix='/employee')

    @employee_app.route('', methods=['POST'], endpoint='create_employee')
    @authorization.login_required
    def create_employee(*args):
        store_data = request.json
        store_data['store_id'] = g.store_id
        check = check_request(store_data, ['store_id', 'employee_name', 'phone_number'])

        if not check:
            abort(400)

        connection = get_db_connection()

        try:
            employee_service = EmployeeService(connection)
            result = employee_service.create_employee(store_data)
            connection.commit()

            return mutation_response(result)
        except Exception as error:
            connection.rollback()
            throw_error(error)
        finally:
            connection.close()

    @employee_app.route('/vacation', methods=['POST'], endpoint='create_vacation')
    def create_vacation(*args):
        vacation_data = request.json

        check = check_request(vacation_data, ['employee_id', 'start_at', 'finish_at'])

        if not check:
            abort(400)

        connection = get_db_connection()

        try:
            employee_service = EmployeeService(connection)
            result = employee_service.create_vacation(vacation_data)
            connection.commit()

            return mutation_response(result)
        except Exception as error:
            connection.rollback()
            throw_error(error)
        finally:
            connection.close()

    @employee_app.route('/<int:store_id>', methods=['GET'], endpoint='get_employee_list')
    @authorization.login_required
    @authorization.is_admin
    def get_employee_list(*args, store_id):
        store_id_: int = 0

        if not g.is_admin and g.store_id == store_id:
            store_id_ = store_id
        elif g.is_admin:
            store_id_ = store_id
        else:
            abort(401)

        connection = get_db_connection()

        try:
            employee_service = EmployeeService(connection)
            employee_list = employee_service.get_employee_list_by_store_id(store_id_)
            connection.commit()

            return jsonify({
                'data': employee_list
            })
        except Exception as error:
            connection.rollback()
            throw_error(error)
        finally:
            connection.close()
