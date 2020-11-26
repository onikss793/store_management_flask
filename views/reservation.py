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

    @reservation_app.route('/<int:store_id>', methods=['GET'], endpoint='get_reservation_list')
    @authorization.login_required
    @authorization.is_admin
    def get_reservation_list(*args, store_id):
        the_day = request.args.get('date')
        store_id = authorization.get_store_id(g, store_id)

        connection = get_db_connection()

        try:
            reservation_service = ReservationService(connection)
            reservation_list = reservation_service.get_reservation_list(store_id=store_id, the_day=the_day)

            return jsonify({
                'data': reservation_list
            })
        except Exception as error:
            connection.rollback()
            throw_error(error)
        finally:
            connection.close()

    @reservation_app.route('/<int:reservation_id>', methods=['POST'], endpoint='update_reservation')
    @authorization.login_required
    @authorization.is_admin
    def update_reservation(*args, reservation_id):
        store_id = authorization.get_store_id(g, request.args.get('store_id') | None)

        reservation_data = request.json
        reservation_data['reservation_id'] = reservation_id
        reservation_data['store_id'] = store_id

        connection = get_db_connection()

        try:
            reservation_service = ReservationService(connection)
            result = reservation_service.update_reservation_by_id(reservation_data)
            connection.commit()

            return mutation_response(result)
        except Exception as error:
            connection.rollback()
            throw_error(error)
        finally:
            connection.close()

    # @reservation_app.route('/<int:reservation_id>', methods=['DELETE'], endpoint='delete_reservation')
    # @authorization.login_required
    # @authorization.is_admin
    # def delete_reservation(*args, reservation_id):
    #     connection = get_db_connection()
    #
    #     try:
    #         reservation_service = ReservationService
