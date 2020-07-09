import json
from datetime import datetime, timedelta

import pytest

from app import create_app
from config import test_config
from test_utils import data, session, setups


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


def test_create_employee_200(api):
    access_token = session.login_get_access_token(api=api)

    employee = {
        'store_id': 1,
        'employee_name': '유병민',
        'phone_number': '01012341234'
    }

    resp = api.post(
        '/employee',
        data=json.dumps(employee),
        content_type='application/json',
        headers={'Authorization': access_token}
    )

    assert resp.status_code == 200


def test_create_vacation_200(api):
    month_later = str(datetime.utcnow() + timedelta(days=30))
    day_after_month_later = str(datetime.utcnow() + timedelta(days=31))
    vacation = {
        'employee_id': 1,
        'start_at': month_later,
        'finish_at': day_after_month_later
    }

    resp = api.post(
        '/employee/vacation',
        data=json.dumps(vacation),
        content_type='application/json'
    )

    assert resp.status_code == 200


def test_create_vacation_409(api):
    # 0.0.1.seed.sql 에서 내일부터 하루동안 휴가이므로 409
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

    assert resp.status_code == 409


def test_get_employee_list_200(api):
    # 0.0.0.1.seed.sql에서 내일부터 하루동안 휴가이므로 내일 날짜의 직원 목록을 받을 경우, vacation은 True
    access_token = session.login_get_access_token(api)
    tomorrow = str(datetime.utcnow() + timedelta(days=1))

    resp_tomorrow = api.get(
        '/employee/1?date=' + tomorrow,
        content_type='application/json',
        headers={'Authorization': access_token}
    )

    resp_json_tomorrow = json.loads(resp_tomorrow.data.decode('utf-8'))
    employee_list_tomorrow = resp_json_tomorrow['data']

    print(json.dumps(resp_json_tomorrow, indent=2))

    expected_data_tomorrow = [{
        'employee_name': employee['employee_name'],
        'phone_number': employee['phone_number'],
        'vacation': True
    } for index, employee in enumerate(data.employee_data)]

    resp_data = [{
        'employee_name': employee['employee_name'],
        'phone_number': employee['phone_number'],
        'vacation': bool(employee['vacation'])
    } for employee in employee_list_tomorrow]

    assert resp_data == expected_data_tomorrow

    # 0.0.0.1.seed.sql에서 내일부터 하루동안 휴가이므로 오늘 날짜의 직원 목록을 받을 경우, vacation은 False
    today = str(datetime.utcnow())

    resp_today = api.get(
        '/employee/1?date=' + today,
        content_type='application/json',
        headers={'Authorization': access_token}
    )

    resp_json_today = json.loads(resp_today.data.decode('utf-8'))
    employee_list_today = resp_json_today['data']

    print(json.dumps(resp_json_today, indent=2))

    expected_data_today = [{
        'employee_name': employee['employee_name'],
        'phone_number': employee['phone_number'],
        'vacation': False
    } for index, employee in enumerate(data.employee_data)]

    resp_data = [{
        'employee_name': employee['employee_name'],
        'phone_number': employee['phone_number'],
        'vacation': bool(employee['vacation'])
    } for employee in employee_list_today]

    assert resp_data == expected_data_today


def test_update_employee_200(api):
    access_token = session.login_get_access_token(api)

    employee = {
        'store_id': 2,
        'employee_name': '업데이트',
        'phone_number': '01012341234'
    }

    resp = api.post(
        '/employee/1',
        data=json.dumps(employee),
        content_type='application/json',
        headers={'Authorization': access_token}
    )

    assert resp.status_code == 200


def test_delete_employee_200(api):
    access_token = session.login_get_access_token(api)

    resp = api.delete(
        '/employee/1',
        content_type='application/json',
        headers={'Authorization': access_token}
    )

    assert resp.status_code == 200
