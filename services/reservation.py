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
            start_at=start_at,
            finish_at=finish_at,
            status=status,
            memo=memo
        )

        return True if result else False
