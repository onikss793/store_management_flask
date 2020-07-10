CREATE TABLE clients (
    id           INT          NOT NULL PRIMARY KEY AUTO_INCREMENT,
    client_name  VARCHAR(20)  NOT NULL,
    phone_number VARCHAR(20)  NOT NULL UNIQUE,
    memo         VARCHAR(255) NULL,
    store_id     INT          NOT NULL,
    created_at   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP    NULL     DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    deleted_at   TIMESTAMP    NULL     DEFAULT NULL
);