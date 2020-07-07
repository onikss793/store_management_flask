import json

from database import get_db_connection
from services.store import StoreService

credential = {
    'store_name': '대치 1 호점',
    'password': 'password',
    'brand_id': 1,
    'is_admin': True
}


def set_store_for_login():
    connection = get_db_connection()
    store_service = StoreService(connection)

    try:
        store_service.create_store(credential)

        connection.commit()
    except Exception as error:
        print(error)
        connection.rollback()
    finally:
        connection.close()


def login_get_access_token(api):
    set_store_for_login()

    resp = api.post(
        '/store/login',
        data=json.dumps(credential),
        content_type='application/json'
    )
    resp_json = json.loads(resp.data.decode('utf-8'))

    return resp_json['access_token']
