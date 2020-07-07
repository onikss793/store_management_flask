from pymysql import cursors


class StoreDao:
    def __init__(self, connection):
        self.cursor = connection.cursor

    def create_one(self, store_name: str, password: str, brand_id: int, is_admin: bool):
        with self.cursor(cursors.DictCursor) as cursor:
            return cursor.execute('''
                INSERT INTO stores (
                    store_name, 
                    password, 
                    brand_id, 
                    is_admin
                ) VALUES (
                    %(store_name)s, 
                    %(password)s, 
                    %(brand_id)s, 
                    %(is_admin)s
                )
            ''', {'store_name': store_name, 'password': password, 'brand_id': brand_id, 'is_admin': is_admin})

    def get_store_data_by_name(self, store_name: str):
        with self.cursor(cursors.DictCursor) as cursor:
            cursor.execute('''
                SELECT
                    id,
                    store_name,
                    password,
                    brand_id,
                    is_admin,
                    created_at,
                    updated_at
                FROM stores
                WHERE store_name = %(store_name)s
                AND deleted_at IS NULL
            ''', {'store_name': store_name})

            return cursor.fetchone()

    def get_is_admin(self, store_id: int):
        with self.cursor(cursors.DictCursor) as cursor:
            cursor.execute('''
                SELECT
                    is_admin
                FROM stores
                WHERE id = %(store_id)s
                AND deleted_at IS NULL
            ''', {'store_id': store_id})

            return cursor.fetchone()

    def get_store_list(self):
        with self.cursor(cursors.DictCursor) as cursor:
            cursor.execute('''
                SELECT
                    STORE.id AS id,
                    STORE.store_name AS store_name,
                    STORE.is_admin AS is_admin,
                    STORE.created_at AS created_at,
                    STORE.updated_at AS updated_at,
                    BRAND.id AS brand_id,
                    BRAND.brand_name AS brand_name,
                    BRAND.created_at AS brand_created_at,
                    BRAND.updated_at AS brand_updated_at
                FROM stores AS STORE
                LEFT JOIN brands AS BRAND ON (STORE.brand_id = BRAND.id)
                WHERE STORE.deleted_at IS NULL
                AND BRAND.deleted_at IS NULL
            ''')

            return cursor.fetchall()

    def get_store_by_id(self, store_id):
        with self.cursor(cursors.DictCursor) as cursor:
            cursor.execute('''
                SELECT
                    STORE.id AS id,
                    STORE.store_name AS store_name,
                    STORE.is_admin AS is_admin,
                    STORE.created_at AS created_at,
                    STORE.updated_at AS updated_at,
                    BRAND.id AS brand_id,
                    BRAND.brand_name AS brand_name,
                    BRAND.created_at AS brand_created_at,
                    BRAND.updated_at AS brand_updated_at
                FROM stores AS STORE
                LEFT JOIN brands AS BRAND ON (STORE.brand_id = BRAND.id)
                WHERE STORE.id = %(store_id)s
                AND STORE.deleted_at IS NULL
                AND BRAND.deleted_at IS NULL
            ''', {'store_id': store_id})

            return cursor.fetchone()
