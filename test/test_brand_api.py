import json

import pytest

from app import create_app
from config import test_config
from test_utils import setups, session


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


def test_create_brand_200(api):
    brand = {
        'brand_name': '페디'
    }

    resp = api.post(
        '/brand',
        data=json.dumps(brand),
        content_type='application/json'
    )

    assert resp.status_code == 200


def test_get_brand_list_200(api):
    access_token = session.login_get_access_token(api)

    resp = api.get(
        '/brand',
        content_type='application/json',
        headers={'Authorization': access_token}
    )
    resp_json = json.loads(resp.data.decode('utf-8'))
    print(json.dumps(resp_json, indent=2))
    brand_list = resp_json['data']

    brand_name_list = [{'brand_name': brand['brand_name']} for brand in brand_list]

    assert brand_name_list == [{'brand_name': '에끌리'}]
