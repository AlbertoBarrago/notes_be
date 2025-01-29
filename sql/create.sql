CREATE DATABASE notez_be;
USE notez_be;

-- Audit Table
CREATE TABLE audit
(
    id          SERIAL PRIMARY KEY,
    user_id     VARCHAR(36) NOT NULL,
    action      VARCHAR(50) NOT NULL,
    description TEXT,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_audit FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Users Table
CREATE TABLE users
(
    id              VARCHAR(36) PRIMARY KEY,
    username        VARCHAR(50) UNIQUE  NOT NULL,
    email           VARCHAR(100) UNIQUE NOT NULL,
    picture_url     VARCHAR(255),
    hashed_password VARCHAR(255)        NOT NULL,
    created_at      TIMESTAMP                    DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP                    DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    role            VARCHAR(50)         NOT NULL DEFAULT 'GUEST'
);

-- Notes Table
CREATE TABLE notes
(
    id         SERIAL PRIMARY KEY,
    user_id    VARCHAR(36)                                                     NOT NULL,
    title      VARCHAR(100)                                                    NOT NULL,
    content    TEXT                                                            NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP                             NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    is_public  BOOLEAN   DEFAULT false,
    tags       JSON,
    image_url  VARCHAR(255),
    CONSTRAINT fk_user_notes FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Auth Table
CREATE TABLE auth
(
    id         SERIAL PRIMARY KEY,
    identifier VARCHAR(36) UNIQUE NOT NULL,
    requests   INT       DEFAULT 0,
    timestamp  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE rate_limits
(
    id         INT PRIMARY KEY AUTO_INCREMENT,
    identifier VARCHAR(36) UNIQUE NOT NULL,
    requests   INT       DEFAULT 0,
    timestamp  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);