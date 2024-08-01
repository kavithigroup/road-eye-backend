CREATE TABLE user
(
    user_id    SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(32)         NOT NULL,
    last_name  VARCHAR(32)         NOT NULL,
    email      VARCHAR(128) UNIQUE NOT NULL,
    otp        VARCHAR(6),
    phone      VARCHAR(15)         NOT NULL,
    nic        VARCHAR(16)         NOT NULL,
    username   VARCHAR(32) UNIQUE  NOT NULL,
    password   VARCHAR(64)         NOT NULL,
    role       TINYINT UNSIGNED             DEFAULT 0,
    reg_time   DATETIME            NOT NULL DEFAULT CURRENT_TIMESTAMP,
    mod_time   DATETIME ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE otp
(
    otp_id   SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email    VARCHAR(128) NOT NULL,
    otp      VARCHAR(6)   NOT NULL,
    reg_time DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    mod_time DATETIME ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE vehicle
(
    vehicle_id     SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user           SMALLINT UNSIGNED NOT NULL REFERENCES user (user_id),
    vehicle_number VARCHAR(16)       NOT NULL,
    brand          VARCHAR(16),
    model          VARCHAR(32),
    type VARCHAR(32),
    yom            SMALLINT UNSIGNED,
    millage        MEDIUMINT UNSIGNED,
    color          VARCHAR(16),
    owner          VARCHAR(64),
    absolute_owner VARCHAR(64),
    reg_time       DATETIME          NOT NULL DEFAULT CURRENT_TIMESTAMP,
    mod_time       DATETIME ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE (vehicle_number, user)
);