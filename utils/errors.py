import traceback

from flask import json, abort, current_app
from werkzeug.exceptions import HTTPException, InternalServerError


def throw_error(error: Exception):
    if not current_app.config['TESTING']:
        traceback.print_exc()

    code = error.code if hasattr(error, 'code') else 500

    return abort(code, error.__str__())


def create_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        response = e.get_response()
        response.data = json.dumps({
            'code': e.code,
            'name': e.name,
            'description': e.description,
        })
        response.content_type = 'application/json'

        return response

    @app.errorhandler(InternalServerError)
    def handle_500(e):
        response = e.get_response()
        response.data = json.dumps({
            'code': e.code,
            'name': e.name,
            'description': e.description,
        })

        return response
