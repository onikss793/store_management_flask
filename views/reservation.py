from flask import request, Blueprint, abort

from database import get_db_connection
from services import ReservationService
from utils import mutation_response, throw_error, check_request


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
