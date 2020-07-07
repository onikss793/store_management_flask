from functools import wraps

import jwt
from flask import request, current_app, g, abort
from jwt import InvalidTokenError, ExpiredSignatureError

from database import get_db_connection
from services import StoreService
from utils import throw_error


def is_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        connection = get_db_connection()

        try:
            store_id = g.store_id

            store_service = StoreService(connection)
            result = store_service.check_is_admin(store_id)
            connection.commit()

            if result:
                g.is_admin = True
            else:
                g.is_admin = False
        except Exception as error:
            throw_error(error)
        finally:
            connection.close()

        return f(*args, **kwargs)

    return decorated_function


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get('Authorization')

        if access_token is not None:
            payload = None

            try:
                payload = jwt.decode(access_token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])

            except InvalidTokenError or ExpiredSignatureError:
                payload = None

            except Exception as error:
                throw_error(error)

            if payload is None:
                abort(401)

            store_id = payload['store_id']
            g.store_id = store_id
        else:
            abort(401)

        return f(*args, **kwargs)

    return decorated_function
