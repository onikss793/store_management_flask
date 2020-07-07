CREATE TABLE brands (
    id         INT          NOT NULL PRIMARY KEY AUTO_INCREMENT,
    brand_name VARCHAR(20)  NOT NULL UNIQUE,
    created_at TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP    NULL     DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP    NULL     DEFAULT NULL
);

CREATE TABLE employees (
    id            INT          NOT NULL PRIMARY KEY AUTO_INCREMENT,
    store_id      INT          NOT NULL,
    employee_name VARCHAR(20)  NOT NULL,
    phone_number  VARCHAR(30)  NULL,
    enrolled_in   TIMESTAMP    NULL,
    created_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP    NULL     DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    deleted_at    TIMESTAMP    NULL     DEFAULT NULL
);

CREATE TABLE reservations (
    id          INT          NOT NULL PRIMARY KEY AUTO_INCREMENT,
    store_id    INT          NOT NULL,
    employee_id INT          NOT NULL,
    start_at    TIMESTAMP    NOT NULL,
    finish_at   TIMESTAMP    NOT NULL,
    status      ENUM('ready', 'done', 'canceled'),
    memo        VARCHAR(255) NOT NULL,
    created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP    NULL     DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    deleted_at  TIMESTAMP    NULL     DEFAULT NULL
);

CREATE TABLE stores (
    id          INT          NOT NULL PRIMARY KEY AUTO_INCREMENT,
    brand_id    INT          NOT NULL,
    store_name  VARCHAR(30)  NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    is_admin    TINYINT(1)   NOT NULL DEFAULT 0,
    created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP    NULL     DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    deleted_at  TIMESTAMP    NULL     DEFAULT NULL
);

CREATE TABLE vacations (
    id          INT          NOT NULL PRIMARY KEY AUTO_INCREMENT,
    employee_id INT          NOT NULL,
    start_at    TIMESTAMP    NOT NULL,
    finish_at   TIMESTAMP    NOT NULL,
    created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP    NULL     DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    deleted_at  TIMESTAMP    NULL     DEFAULT NULL
);
