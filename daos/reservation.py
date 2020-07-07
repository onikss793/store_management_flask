from pymysql import cursors


class ReservationDao:
    def __init__(self, connection):
        self.cursor = connection.cursor

    def create_one(self, store_id: int, employee_id: int, start_at: str, finish_at: str, status: str, memo: str):
        with self.cursor(cursors.DictCursor) as cursor:
            return cursor.execute('''
                INSERT INTO reservations (
                    store_id,
                    employee_id,
                    start_at,
                    finish_at,
                    status,
                    memo
                ) VALUES (
                    %(store_id)s,
                    %(employee_id)s,
                    %(start_at)s,
                    %(finish_at)s,
                    %(status)s,
                    %(memo)s
                )
            ''', {
                'store_id': store_id,
                'employee_id': employee_id,
                'start_at': start_at,
                'finish_at': finish_at,
                'status': status,
                'memo': memo
            })
