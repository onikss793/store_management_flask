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

    def get_reservation_by_store_id_and_date(self, store_id, start_at, finish_at):
        with self.cursor(cursors.DictCursor) as cursor:
            cursor.execute('''
                SELECT
                    RESERVATION.id AS id,
                    RESERVATION.start_at AS start_at,
                    RESERVATION.finish_at AS finish_at,
                    RESERVATION.status AS status,
                    RESERVATION.memo AS memo,
                    RESERVATION.created_at AS created_at,
                    RESERVATION.updated_at AS updated_at,
                    EMPLOYEE.id AS employee_id,
                    EMPLOYEE.employee_name AS employee_name,
                    EMPLOYEE.phone_number AS employee_phone_number,
                    EMPLOYEE.created_at AS employee_created_at,
                    EMPLOYEE.updated_at AS employee_updated_at
                FROM reservations AS RESERVATION
                    LEFT JOIN
                        employees AS EMPLOYEE ON RESERVATION.employee_id = EMPLOYEE.id
                WHERE RESERVATION.store_id = %(store_id)s
                    AND RESERVATION.deleted_at IS NULL
                    AND RESERVATION.start_at >= %(start_at)s
                    AND RESERVATION.finish_at <= %(finish_at)s 
                ORDER BY RESERVATION.start_at
            ''', {
                'store_id': store_id,
                'start_at': start_at,
                'finish_at': finish_at
            })

            return cursor.fetchall()
