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
    type           VARCHAR(32),
    yom            SMALLINT UNSIGNED,
    millage        MEDIUMINT UNSIGNED,
    color          VARCHAR(16),
    owner          VARCHAR(64),
    absolute_owner VARCHAR(64),
    reg_time       DATETIME          NOT NULL DEFAULT CURRENT_TIMESTAMP,
    mod_time       DATETIME ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE (vehicle_number, user)
);

CREATE TABLE complain
(
    complain_id         SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user                SMALLINT UNSIGNED NOT NULL REFERENCES user (user_id),
    district            VARCHAR(32)       NOT NULL,
    police_station      VARCHAR(32)       NOT NULL,
    type                VARCHAR(32)       NOT NULL,
    subject             VARCHAR(64)       NOT NULL,
    complain            VARCHAR(256),
    proof               VARCHAR(500)      NOT NULL,
    send_time           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (complain_id, user)
);


CREATE TABLE Video_capture (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    userid SMALLINT UNSIGNED NOT NULL REFERENCES user (user_id),
    link VARCHAR(255) NOT NULL,
    date_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    vehicle_id SMALLINT UNSIGNED NOT NULL REFERENCES vehicle(vehicle_id)
);

CREATE TABLE Post (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    userid SMALLINT UNSIGNED NOT NULL REFERENCES user (user_id),
    video_link VARCHAR(255) NOT NULL,
    likes INT UNSIGNED DEFAULT 0,
    views INT UNSIGNED DEFAULT 0,
    description VARCHAR(500),
    date_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title VARCHAR(100) NOT NULL
);

CREATE TABLE Comment (
    commentid INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    postid INT UNSIGNED NOT NULL REFERENCES Post (id),
    userid SMALLINT UNSIGNED NOT NULL REFERENCES user (user_id),
    comment TEXT NOT NULL,
    date_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE Notification (
    userid SMALLINT UNSIGNED NOT NULL REFERENCES user (user_id),
    title VARCHAR(100) NOT NULL,
    description VARCHAR(500) NOT NULL,
    PRIMARY KEY (userid)
);


CREATE TABLE Inquiry (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    userid SMALLINT UNSIGNED NOT NULL REFERENCES user (user_id),
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    attachment VARCHAR(255),
    reply TEXT
);

CREATE TABLE Location_Request (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    userid SMALLINT UNSIGNED NOT NULL REFERENCES user (user_id),
    vehicle_no VARCHAR(20) NOT NULL,
    type VARCHAR(50) NOT NULL,
    color VARCHAR(30),
    brand VARCHAR(50),
    model VARCHAR(50),
    docs VARCHAR(255),
    image VARCHAR(255),
    approval BOOLEAN NOT NULL DEFAULT FALSE
);


CREATE TABLE Search_result (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    LR_id INT UNSIGNED NOT NULL REFERENCES Location_Request (id),
    location VARCHAR(255) NOT NULL,
    date_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    image VARCHAR(255)
);




