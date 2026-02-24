-- =============================================================================
-- create.sql
-- Full schema for the notez_be database.
-- Run once on a fresh MySQL instance (or after drop.sql).
-- Usage:  mysql -u root -p < sql/create.sql
-- =============================================================================

CREATE DATABASE IF NOT EXISTS notez_be
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE notez_be;

-- -----------------------------------------------------------------------------
-- users
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users
(
    id              VARCHAR(36)  PRIMARY KEY,
    username        VARCHAR(50)  UNIQUE NOT NULL,
    email           VARCHAR(100) UNIQUE NOT NULL,
    picture_url     VARCHAR(255)        NULL,
    hashed_password VARCHAR(255)        NOT NULL,
    created_at      DATETIME            NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME            NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    role            VARCHAR(50)         NOT NULL DEFAULT 'GUEST',
    INDEX ix_users_username (username),
    INDEX ix_users_email    (email)
);

-- -----------------------------------------------------------------------------
-- notes
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS notes
(
    id         INT          NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id    VARCHAR(36)  NOT NULL,
    title      VARCHAR(100) NOT NULL,
    content    TEXT         NOT NULL,
    created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME         NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_public  BOOLEAN          NULL DEFAULT FALSE,
    tags       JSON             NULL,
    image_url  VARCHAR(255)     NULL,
    INDEX ix_notes_id (id),
    CONSTRAINT fk_notes_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- -----------------------------------------------------------------------------
-- audit
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS audit
(
    id          INT          NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id     VARCHAR(36)  NOT NULL,
    action      VARCHAR(255) NOT NULL,
    description VARCHAR(255)     NULL,
    timestamp   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_audit_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- -----------------------------------------------------------------------------
-- rate_limits
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS rate_limits
(
    id         INT          NOT NULL AUTO_INCREMENT PRIMARY KEY,
    identifier VARCHAR(255)     NULL,
    requests   INT              NULL DEFAULT 0,
    timestamp  DATETIME         NULL,
    INDEX ix_rate_limits_id         (id),
    INDEX ix_rate_limits_identifier (identifier)
);
