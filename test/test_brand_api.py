import json

import pytest

from app import create_app
from config import test_config
from database import get_db_connection
from test_utils import data, setups


@pytest.fixture
def api():
    app = create_app(test_config)
    app.config['TESTING'] = True
    api = app.test_client()

    return api


def setup_function():
    setups.setup_brands()


def teardown_function():
    connection = get_db_connection()
    cursor = connection.cursor()

    with cursor:
        cursor.execute('''
            TRUNCATE brands
        ''')

        connection.commit()

    connection.close()


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
    resp = api.get(
        '/brand',
        content_type='application/json'
    )
    resp_json = json.loads(resp.data.decode('utf-8'))
    brand_list = resp_json['data']
    print(resp_json)
    print(data.brand_data)

    for brand in brand_list:
        hasattr(brand, 'id')
        hasattr(brand, 'brand_name')
        hasattr(brand, 'created_at')
        hasattr(brand, 'updated_at')

    brand_name_list = [{'brand_name': brand['brand_name']} for brand in brand_list]

    assert brand_name_list == data.brand_data
