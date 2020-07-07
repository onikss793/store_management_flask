INSERT INTO brands (brand_name)
VALUES ('에끌리');

INSERT INTO employees (store_id, employee_name, phone_number, enrolled_in)
VALUES (1, '김관희', '01012345678', CURRENT_TIMESTAMP);

INSERT INTO reservations (store_id, employee_id, start_at, finish_at, status, memo)
VALUES (1, 1, CURRENT_TIMESTAMP, DATE_ADD(now(), INTERVAL 2 HOUR), 'ready', 'VIP 유웅조 젤네일');

INSERT INTO stores (store_name, password, brand_id, is_admin)
VALUES ('1 호점', 'password', 1, 1);

INSERT INTO vacations (employee_id, start_at, finish_at)
VALUES (1, DATE_ADD(now(), INTERVAL 24 HOUR), DATE_ADD(now(), INTERVAL 48 HOUR));