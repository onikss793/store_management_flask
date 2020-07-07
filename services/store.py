from datetime import datetime, timedelta

import bcrypt
import jwt
from flask import current_app

from daos import StoreDao


class StoreService:
    def __init__(self, connection):
        self.store_dao = StoreDao(connection)

    def create_store(self, store_data):
        store_name = store_data['store_name']
        password = store_data['password']
        brand_id = store_data['brand_id']
        is_admin = store_data['is_admin']
        hashed_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())

        result = self.store_dao.create_one(store_name, hashed_password, brand_id, is_admin)

        return True if result else False

    def login(self, credential):
        store_name = credential['store_name']
        password = credential['password']

        store_data = self.store_dao.get_store_data_by_name(store_name)

        if store_data and self.check_password(password, store_data['password']):
            token = self.generate_access_token(store_data['id'])

            return token.decode('UTF-8')
        else:
            return None

    def get_store_list(self):
        store_data = self.store_dao.get_store_list()

        return [{
            'id': store['id'],
            'store_name': store['store_name'],
            'is_admin': store['is_admin'],
            'brand': {
                'id': store['brand_id'],
                'brand_name': store['brand_name'],
                'created_at': store['brand_created_at'],
                'updated_at': store['brand_updated_at']
            },
            'created_at': store['created_at'],
            'updated_at': store['updated_at']
        } for store in store_data] if store_data else []

    def check_is_admin(self, store_id):
        is_admin = self.store_dao.get_is_admin(store_id)['is_admin']

        return True if is_admin else False

    @staticmethod
    def check_password(password, hashed_password):
        return bcrypt.checkpw(password.encode('UTF-8'), hashed_password.encode('UTF-8'))

    @staticmethod
    def generate_access_token(store_id):
        payload = {
            'store_id': store_id,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24 * 7 * 4)
        }
        token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

        return token
