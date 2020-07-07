import json
from datetime import datetime

import pytest
from dateutil import parser

from app import create_app
from config import test_config
from test_utils import setups, session, data


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


def test_create_reservation_200(api):
    reservation = {
        'store_id': 1,
        'employee_id': 1,
        'start_at': str(datetime(year=2020, month=10, day=1, hour=15, minute=00)),
        'finish_at': str(datetime(year=2020, month=10, day=1, hour=16, minute=00)),
        'status': 'ready',
        'memo': 'VIP Gel Nail'
    }

    resp = api.post(
        '/reservation',
        data=json.dumps(reservation),
        content_type='application/json'
    )

    assert resp.status_code == 200


def test_get_reservation_list_200(api):
    setups.setup_reservations()  # javascript ISOString을 위해 따로 생성한다.
    access_token = session.login_get_access_token(api)

    resp = api.get(
        '/reservation/1?date=' + '2020-05-08T11:30:00.000Z',  # javascript ISOString 형식을 따름
        content_type='application/json',
        headers={'Authorization': access_token}
    )

    resp_json = json.loads(resp.data.decode('utf-8'))
    print(json.dumps(resp_json, indent=4))
    reservation_list = resp_json['data']

    assert [{
        'employee_id': reservation['employee']['id'],
        'start_at': parser.isoparse(reservation['start_at']).timestamp(),
        'finish_at': parser.isoparse(reservation['finish_at']).timestamp(),
        'status': reservation['status'],
        'memo': reservation['memo']
    } for reservation in reservation_list] == [{
        'employee_id': reservation['employee_id'],
        'start_at': parser.isoparse(reservation['start_at']).astimezone().timestamp(),
        'finish_at': parser.isoparse(reservation['finish_at']).astimezone().timestamp(),
        'status': reservation['status'],
        'memo': reservation['memo']
    } for reservation in data.reservation_data]
