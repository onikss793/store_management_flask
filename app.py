from flask import Flask
from flask_cors import CORS

from utils import set_config
from views import create_endpoints


def create_app(test_config=None):
    app = Flask(__name__)

    CORS(app)

    set_config(app, test_config)

    create_endpoints(app)

    return app


handler = create_app()
