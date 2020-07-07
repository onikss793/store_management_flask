from flask import request, Blueprint, abort, jsonify, g

from database import get_db_connection
from services import ReservationService
from utils import mutation_response, throw_error, check_request, authorization


class ReservationView:
    reservation_app = Blueprint('reservation_app', __name__, url_prefix='/reservation')

    @reservation_app.route('', methods=['POST'], endpoint='create_reservation')
    def create_reservation(*args):
        reservation_data = request.json
        check = check_request(reservation_data, ['store_id', 'employee_id', 'start_at', 'finish_at', 'status', 'memo'])

        if not check:
            abort(400)

        connection = get_db_connection()

        try:
            reservation_service = ReservationService(connection)
            result = reservation_service.create_reservation(reservation_data)
            connection.commit()

            return mutation_response(result)
        except Exception as error:
            connection.rollback()
            throw_error(error)
        finally:
            connection.close()

    @reservation_app.route('<int:store_id>', methods=['GET'], endpoint='get_reservation_list')
    @authorization.login_required
    @authorization.is_admin
    def get_reservation_list(*args, store_id):
        the_day = request.args.get('date')
        store_id_ = 0

        if not g.is_admin and g.store_id == store_id:
            store_id_ = store_id
        elif g.is_admin:
            store_id_ = store_id
        else:
            abort(401)

        connection = get_db_connection()

        try:
            reservation_service = ReservationService(connection)
            reservation_list = reservation_service.get_reservation_list(store_id=store_id_, the_day=the_day)

            return jsonify({
                'data': reservation_list
            })
        except Exception as error:
            connection.rollback()
            throw_error(error)
        finally:
            connection.close()
