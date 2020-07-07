import json
from datetime import datetime

import pytest

from app import create_app
from config import test_config
from database import get_db_connection
from test_utils import setups


@pytest.fixture
def api():
    app = create_app(test_config)
    app.config['TESTING'] = True
    api = app.test_client()

    return api


def setup_function():
    setups.setup_stores()
    setups.setup_employees()


def teardown_function():
    connection = get_db_connection()
    cursor = connection.cursor()

    with cursor:
        cursor.execute('''
            TRUNCATE stores
        ''')
        cursor.execute('''
            TRUNCATE employees
        ''')
        cursor.execute('''
            TRUNCATE reservations
        ''')

        connection.commit()

    connection.close()


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
