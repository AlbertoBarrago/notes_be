-- =============================================================================
-- create_user.sql
-- Creates a dedicated application user with least-privilege permissions.
-- Run this once as root after create.sql.
-- Usage:  mysql -u root -p < sql/create_user.sql
--
-- Replace 'notez_password' with a strong password before running.
-- Update MYSQL_USER and MYSQL_PASSWORD in .env accordingly.
-- =============================================================================

CREATE USER IF NOT EXISTS 'notez_app'@'%' IDENTIFIED BY 'notez_password';

-- Application only needs DML on notez_be; no DDL, no global privileges.
GRANT SELECT, INSERT, UPDATE, DELETE ON notez_be.* TO 'notez_app'@'%';

-- Allow Alembic migrations to run DDL (CREATE/ALTER/DROP TABLE).
-- Remove this grant in a production environment where migrations are run
-- with a separate privileged user via CI/CD.
GRANT CREATE, ALTER, DROP, INDEX, REFERENCES ON notez_be.* TO 'notez_app'@'%';

FLUSH PRIVILEGES;

-- Verify
SELECT user, host FROM mysql.user WHERE user = 'notez_app';
SHOW GRANTS FOR 'notez_app'@'%';
