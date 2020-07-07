import json

import pytest

from app import create_app
from config import test_config
from database import get_db_connection
from services import StoreService
from test_utils import data


@pytest.fixture
def api():
    app = create_app(test_config)
    app.config['TESTING'] = True
    api = app.test_client()

    return api


def setup_function():
    connection = get_db_connection()

    store_service = StoreService(connection)

    for store in data.store_data:
        result = store_service.create_store(store_data=store)

        if not result:
            connection.rollback()
            break

    connection.commit()


def teardown_function():
    connection = get_db_connection()
    cursor = connection.cursor()

    with cursor:
        cursor.execute('''
            TRUNCATE stores
        ''')

        connection.commit()

    connection.close()


def test_create_note_200(api):
    store = {
        'store_name': '5 호점',
        'password': 'password',
        'brand_id': 1,
        'is_admin': False
    }
    data.store_data.append(store)

    resp = api.post(
        '/store',
        data=json.dumps(store),
        content_type='application/json'
    )

    assert resp.status_code == 200


def test_create_note_400(api):
    store = {
        'store_name': '',
        'password': ''
    }

    resp = api.post(
        '/store',
        data=json.dumps(store),
        content_type='application/json'
    )

    assert resp.status_code == 400


def test_login_200(api):
    credential = {
        'store_name': '1 호점',
        'password': 'password'
    }
    resp = api.post(
        '/store/login',
        data=json.dumps(credential),
        content_type='application/json'
    )

    assert resp.status_code == 200


def test_login_401(api):
    credential = {
        'store_name': '1 호점',
        'password': 'wrong'
    }
    resp = api.post(
        '/store/login',
        data=json.dumps(credential),
        content_type='application/json'
    )

    assert resp.status_code == 401
