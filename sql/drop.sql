-- =============================================================================
-- drop.sql
-- Drops all tables and the database itself.
-- Run this to start completely fresh (followed by create.sql).
-- Usage:  mysql -u root -p < sql/drop.sql
--
-- WARNING: all data will be permanently deleted.
-- =============================================================================

USE notez_be;

-- Disable FK checks so tables can be dropped in any order.
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS audit;
DROP TABLE IF EXISTS notes;
DROP TABLE IF EXISTS rate_limits;
DROP TABLE IF EXISTS users;

SET FOREIGN_KEY_CHECKS = 1;

DROP DATABASE IF EXISTS notez_be;
