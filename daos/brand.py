from pymysql import cursors


class BrandDao:
    def __init__(self, connection):
        self.cursor = connection.cursor

    def create_one(self, brand_name):
        with self.cursor(cursors.DictCursor) as cursor:
            return cursor.execute('''
                INSERT INTO brands (
                    brand_name
                ) VALUES (
                    %(brand_name)s 
                )
            ''', {'brand_name': brand_name})

    def select_all(self):
        with self.cursor(cursors.DictCursor) as cursor:
            cursor.execute('''
                SELECT 
                    id,
                    brand_name,
                    created_at,
                    updated_at
                FROM brands
                WHERE deleted_at IS NULL
            ''')

            return cursor.fetchall()
