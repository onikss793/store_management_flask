from datetime import datetime

now = datetime.now()
iso_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")

store_data = [
    {
        'store_name': '선릉 1 호점',
        'password': 'password',
        'brand_id': 1,
        'is_admin': True
    }
]
brand_data = [
    {
        'brand_name': '에끌리'
    }
]
employee_data = [
    {
        'store_id': 1,
        'employee_name': '김관희',
        'phone_number': '01012345678'
    }
]
reservation_data = [
    {
        'store_id': 1,
        'employee_id': 1,
        'start_at': '2020-05-08T10:30:00.000Z',
        'finish_at': '2020-05-08T11:30:00.000Z',
        'status': 'ready',
        'memo': 'VIP 유웅조 젤네일'
    }
]
