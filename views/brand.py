from flask import request, Blueprint, abort, jsonify, g

from database import get_db_connection
from services import BrandService
from utils import mutation_response, throw_error, check_request, authorization


class BrandView:
    brand_app = Blueprint('brand_app', __name__, url_prefix='/brand')

    @brand_app.route('', methods=['POST'], endpoint='create_brand')
    def create_brand(*args):
        brand_data = request.json

        check = check_request(brand_data, ['brand_name'])

        if not check:
            abort(400)

        brand_name = brand_data['brand_name']

        connection = get_db_connection()

        try:
            brand_service = BrandService(connection)
            result = brand_service.create_brand(brand_name)

            connection.commit()

            return mutation_response(result)

        except Exception as error:
            throw_error(error)

        finally:
            connection.close()

    @brand_app.route('', methods=['GET'], endpoint='get_brand_list')
    @authorization.login_required
    @authorization.is_admin
    def get_brand_list(*args):
        if not g.is_admin:
            abort(401)

        connection = get_db_connection()

        try:
            brand_service = BrandService(connection)
            brands = brand_service.get_brand_list()
            connection.commit()

            return jsonify({
                'data': brands
            })
        except Exception as error:
            throw_error(error)
        finally:
            connection.close()
