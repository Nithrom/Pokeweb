-- Migración para bases creadas con init.sql antiguo (sin slug / specialty).
-- Ejecutar: mysql -u pokeweb_user -p pokeweb < sql/migrate_002.sql

SET NAMES utf8mb4;

ALTER TABLE games
  ADD COLUMN IF NOT EXISTS slug VARCHAR(40) NULL AFTER id;

ALTER TABLE trainers
  ADD COLUMN IF NOT EXISTS slug VARCHAR(80) NULL AFTER id,
  ADD COLUMN IF NOT EXISTS specialty VARCHAR(40) NULL AFTER badge_name,
  ADD COLUMN IF NOT EXISTS location VARCHAR(60) NULL AFTER specialty;

-- MariaDB 10.5+ soporta IF NOT EXISTS en ADD COLUMN; si falla, añade columnas a mano.

ALTER TABLE trainers
  MODIFY trainer_class VARCHAR(20) NOT NULL;
