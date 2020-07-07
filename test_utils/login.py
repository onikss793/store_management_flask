import json

from .data import store_data


def login_get_access_token(api):
    store = store_data[0]
    data = {
        'store_name': store['store_name'],
        'password': store['password']
    }

    resp = api.post(
        '/store/login',
        data=json.dumps(data),
        content_type='application/json'
    )
    resp_json = json.loads(resp.data.decode('utf-8'))

    return resp_json['access_token']
