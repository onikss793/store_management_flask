from flask import request, Blueprint, abort, jsonify, g

from database import get_db_connection
from services import StoreService
from utils import mutation_response, throw_error, check_request, authorization


class StoreView:
    store_app = Blueprint('store_app', __name__, url_prefix='/store')

    @store_app.route('', methods=['POST'], endpoint='create_store')
    def create_store(*args):
        store_data = request.json

        check = check_request(store_data, ['store_name', 'password', 'brand_id', 'is_admin'])

        if not check:
            abort(400)

        connection = get_db_connection()

        try:
            store_service = StoreService(connection)
            result = store_service.create_store(store_data)

            connection.commit()

            return mutation_response(result)
        except Exception as error:
            connection.rollback()
            throw_error(error)
        finally:
            connection.close()

    @store_app.route('/login', methods=['POST'], endpoint='store_login')
    def store_login(*args):
        credential = request.json

        check = check_request(credential, ['store_name', 'password'])

        if not check:
            abort(400)

        connection = get_db_connection()

        try:
            store_service = StoreService(connection)

            data = store_service.login(credential)

            return jsonify(data) if data else abort(401)
        except Exception as error:
            connection.rollback()
            throw_error(error)
        finally:
            connection.close()

    @store_app.route('', methods=['GET'], endpoint='get_store_list')
    @authorization.login_required
    @authorization.is_admin
    def get_store_list(*args):
        if not g.is_admin:
            abort(401)

        connection = get_db_connection()

        try:
            store_service = StoreService(connection)
            store_list = store_service.get_store_list()
            connection.commit()

            return jsonify({
                'data': store_list
            })
        except Exception as error:
            throw_error(error)
        finally:
            connection.close()

    @store_app.route('<int:store_id>', methods=['GET'], endpoint='get_store')
    @authorization.login_required
    @authorization.is_admin
    def get_store(*args, store_id):
        store_id = authorization.get_store_id(g, store_id)

        connection = get_db_connection()

        try:
            store_service = StoreService(connection)
            store = store_service.get_store(store_id=store_id)
            connection.commit()

            return jsonify({
                'data': store
            })
        except Exception as error:
            connection.rollback()
            throw_error(error)
        finally:
            connection.close()
