import json

import pytest

from app import create_app
from config import test_config
from test_utils import data, setups, session


@pytest.fixture
def api():
    app = create_app(test_config)
    app.config['TESTING'] = True
    api = app.test_client()

    return api


def setup_function():
    setups.sql_setup()


def teardown_function():
    setups.sql_teardown()


def test_create_store_200(api):
    store = {
        'store_name': '5 호점',
        'password': 'password',
        'brand_id': 1,
        'is_admin': False
    }

    resp = api.post(
        '/store',
        data=json.dumps(store),
        content_type='application/json'
    )

    assert resp.status_code == 200


def test_create_store_400(api):
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
    session.set_store_for_login()
    credential = session.credential

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


def test_get_store_200(api):
    access_token = session.login_get_access_token(api)

    resp = api.get(
        '/store/1',
        content_type='application/json',
        headers={'Authorization': access_token}
    )

    resp_json = json.loads(resp.data.decode('utf-8'))
    store = resp_json['data']
    expected = data.store_data[0]

    assert {
               'brand_id': store['brand']['id'],
               'store_name': store['store_name'],
               'is_admin': store['is_admin']
           } == {
               'brand_id': expected['brand_id'],
               'store_name': expected['store_name'],
               'is_admin': expected['is_admin']
           }


def test_get_store_list_200(api):
    access_token = session.login_get_access_token(api)

    resp = api.get(
        '/store',
        content_type='application/json',
        headers={'Authorization': access_token}
    )

    resp_json = json.loads(resp.data.decode('utf-8'))
    store_list = resp_json['data']
    expected = data.store_data
    expected.append(session.credential)  # login에서 사용한 store 추가

    assert [{
        'brand_id': store['brand']['id'],
        'is_admin': store['is_admin'],
        'store_name': store['store_name']
    } for store in store_list] == [{
        'brand_id': store['brand_id'],
        'is_admin': store['is_admin'],
        'store_name': store['store_name']
    } for store in expected]
