import json
from datetime import datetime, timedelta

import pytest

from app import create_app
from config import test_config
from database import get_db_connection
from test_utils import data, login, setups


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
            TRUNCATE employees
        ''')
        cursor.execute('''
            TRUNCATE stores
        ''')

        connection.commit()

    connection.close()


def test_create_employee_200(api):
    access_token = login.login_get_access_token(api=api)

    employee = {
        'store_id': 1,
        'employee_name': '유병민',
        'phone_number': '01012341234'
    }
    data.employee_data.append(employee)

    resp = api.post(
        '/employee',
        data=json.dumps(employee),
        content_type='application/json',
        headers={'Authorization': access_token}
    )

    assert resp.status_code == 200


def test_create_vacation_200(api):
    one_day_after = str(datetime.utcnow() + timedelta(days=1))
    three_days_after = str(datetime.utcnow() + timedelta(days=3))
    vacation = {
        'employee_id': 1,
        'start_at': one_day_after,
        'finish_at': three_days_after
    }

    resp = api.post(
        '/employee/vacation',
        data=json.dumps(vacation),
        content_type='application/json'
    )

    assert resp.status_code == 200
