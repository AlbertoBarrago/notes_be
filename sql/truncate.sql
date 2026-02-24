-- =============================================================================
-- truncate.sql
-- Clears all rows from every table while keeping the schema intact.
-- Use this to wipe data between test runs or to start a clean seed.
-- Usage:  mysql -u notez_app -p notez_be < sql/truncate.sql
-- =============================================================================

USE notez_be;

SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE audit;
TRUNCATE TABLE notes;
TRUNCATE TABLE rate_limits;
TRUNCATE TABLE revoked_tokens;
TRUNCATE TABLE users;

SET FOREIGN_KEY_CHECKS = 1;
