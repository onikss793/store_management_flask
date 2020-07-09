from datetime import datetime

from dateutil import parser

from daos import ReservationDao


class ReservationService:
    def __init__(self, connection):
        self.reservation_dao = ReservationDao(connection)

    def create_reservation(self, reservation_data):
        store_id = reservation_data['store_id']
        employee_id = reservation_data['employee_id']
        start_at = reservation_data['start_at']
        finish_at = reservation_data['finish_at']
        status = reservation_data['status']
        memo = reservation_data['memo']

        result = self.reservation_dao.create_one(
            store_id=store_id,
            employee_id=employee_id,
            start_at=parser.isoparse(start_at).astimezone(),
            finish_at=parser.isoparse(finish_at).astimezone(),
            status=status,
            memo=memo
        )

        return True if result else False

    def get_reservation_list(self, store_id, the_day):
        date = datetime.strptime(the_day, '%Y-%m-%dT%H:%M:%S.%fZ')
        start_at = datetime(year=date.year, month=date.month, day=date.day, hour=0, minute=00)
        finish_at = datetime(year=date.year, month=date.month, day=date.day, hour=23, minute=59)

        reservation_list = self.reservation_dao.get_reservation_by_store_id_and_date(
            store_id=store_id,
            start_at=start_at,
            finish_at=finish_at
        )

        return [{
            'id': reservation['id'],
            'employee': {
                'id': reservation['employee_id'],
                'employee_name': reservation['employee_name'],
                'phone_number': reservation['employee_phone_number'],
            },
            'start_at': reservation['start_at'].isoformat(),
            'finish_at': reservation['finish_at'].isoformat(),
            'status': reservation['status'],
            'memo': reservation['memo'],
        } for reservation in reservation_list] if reservation_list else []
