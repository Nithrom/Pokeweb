-- ══════════════════════════════════════════════
--  POKEWEB — Esquema de base de datos
--  MariaDB / MySQL
-- ══════════════════════════════════════════════

SET NAMES utf8mb4;
SET foreign_key_checks = 0;

-- ── Tipos ─────────────────────────────────────
CREATE TABLE IF NOT EXISTS types (
  id       TINYINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  name_en  VARCHAR(20) NOT NULL UNIQUE,   -- 'fire', 'water'...
  name_es  VARCHAR(20) NOT NULL           -- 'Fuego', 'Agua'...
);

-- ── Pokémon ────────────────────────────────────
CREATE TABLE IF NOT EXISTS pokemon (
  id         SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,  -- número pokédex
  name       VARCHAR(60)  NOT NULL UNIQUE,   -- 'rayquaza'
  name_es    VARCHAR(60)  NOT NULL,          -- 'Rayquaza'
  sprite_url TEXT,
  hp         SMALLINT UNSIGNED DEFAULT 0,
  attack     SMALLINT UNSIGNED DEFAULT 0,
  defense    SMALLINT UNSIGNED DEFAULT 0,
  sp_attack  SMALLINT UNSIGNED DEFAULT 0,
  sp_defense SMALLINT UNSIGNED DEFAULT 0,
  speed      SMALLINT UNSIGNED DEFAULT 0,
  is_legendary BOOLEAN DEFAULT FALSE,
  evo_family_id SMALLINT UNSIGNED NULL     -- ID del representante de la familia
);

-- Tipos de cada pokémon (puede tener 1 o 2)
CREATE TABLE IF NOT EXISTS pokemon_types (
  pokemon_id SMALLINT UNSIGNED NOT NULL,
  type_id    TINYINT UNSIGNED  NOT NULL,
  slot       TINYINT UNSIGNED  NOT NULL DEFAULT 1,  -- 1=principal, 2=secundario
  PRIMARY KEY (pokemon_id, slot),
  FOREIGN KEY (pokemon_id) REFERENCES pokemon(id),
  FOREIGN KEY (type_id)    REFERENCES types(id)
);

-- ── Movimientos ────────────────────────────────
CREATE TABLE IF NOT EXISTS moves (
  id         SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  name       VARCHAR(60) NOT NULL UNIQUE,   -- 'hyper-beam'
  name_es    VARCHAR(60) NOT NULL,          -- 'Hiperrayo'
  type_id    TINYINT UNSIGNED NOT NULL,
  category   ENUM('physical','special','status') NOT NULL,
  power      SMALLINT UNSIGNED NULL,
  accuracy   TINYINT UNSIGNED NULL,
  pp         TINYINT UNSIGNED NULL,
  FOREIGN KEY (type_id) REFERENCES types(id)
);

-- Movimientos que puede aprender cada pokémon
CREATE TABLE IF NOT EXISTS pokemon_moves (
  pokemon_id   SMALLINT UNSIGNED NOT NULL,
  move_id      SMALLINT UNSIGNED NOT NULL,
  learn_method ENUM('level-up','machine','egg','tutor') NOT NULL DEFAULT 'level-up',
  level        TINYINT UNSIGNED NULL,   -- nivel en que lo aprende (si es level-up)
  PRIMARY KEY (pokemon_id, move_id),
  FOREIGN KEY (pokemon_id) REFERENCES pokemon(id),
  FOREIGN KEY (move_id)    REFERENCES moves(id)
);

-- ── Efectividad de tipos ────────────────────────
-- attack_type_id → defend_type_id = multiplier
-- 0=inmune, 25=x0.25, 50=x0.5, 100=x1, 200=x2, 400=x4
CREATE TABLE IF NOT EXISTS type_effectiveness (
  attack_type_id  TINYINT UNSIGNED NOT NULL,
  defend_type_id  TINYINT UNSIGNED NOT NULL,
  multiplier      SMALLINT UNSIGNED NOT NULL DEFAULT 100,
  PRIMARY KEY (attack_type_id, defend_type_id),
  FOREIGN KEY (attack_type_id) REFERENCES types(id),
  FOREIGN KEY (defend_type_id) REFERENCES types(id)
);

-- ── Juegos / Versiones ─────────────────────────
CREATE TABLE IF NOT EXISTS games (
  id        SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  slug      VARCHAR(40) NOT NULL UNIQUE,  -- 'heartgold-soulsilver'
  name      VARCHAR(60) NOT NULL,         -- 'HeartGold / SoulSilver'
  region    VARCHAR(30) NOT NULL,         -- 'Johto'
  gen       TINYINT UNSIGNED NOT NULL
);

-- ── Entrenadores (líderes, altos mandos...) ────
CREATE TABLE IF NOT EXISTS trainers (
  id            SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  slug          VARCHAR(80) NOT NULL,   -- único por juego: 'brock-badgerock'
  name          VARCHAR(60) NOT NULL,
  name_es       VARCHAR(60) NOT NULL,
  trainer_class VARCHAR(20) NOT NULL,     -- gym, elite4, champion, kahuna, captain, other
  game_id       SMALLINT UNSIGNED NOT NULL,
  gym_order     TINYINT UNSIGNED NULL,
  badge_name    VARCHAR(40) NULL,
  specialty     VARCHAR(40) NULL,         -- badgerock, rematchice, halafighting...
  location      VARCHAR(60) NULL,
  sprite_url    TEXT NULL,
  team_by_starter JSON NULL,  -- equipos alternativos { "bulbasaur": [...], ... }
  UNIQUE KEY uq_trainer_game_slug (game_id, slug),
  FOREIGN KEY (game_id) REFERENCES games(id)
);

-- Equipo de cada entrenador
CREATE TABLE IF NOT EXISTS trainer_pokemon (
  id          SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  trainer_id  SMALLINT UNSIGNED NOT NULL,
  pokemon_id  SMALLINT UNSIGNED NOT NULL,
  level       TINYINT UNSIGNED NOT NULL DEFAULT 50,
  slot        TINYINT UNSIGNED NOT NULL DEFAULT 1,  -- posición en equipo (1-6)
  FOREIGN KEY (trainer_id) REFERENCES trainers(id),
  FOREIGN KEY (pokemon_id) REFERENCES pokemon(id)
);

-- Movimientos del equipo de cada entrenador
CREATE TABLE IF NOT EXISTS trainer_pokemon_moves (
  trainer_pokemon_id SMALLINT UNSIGNED NOT NULL,
  move_id            SMALLINT UNSIGNED NOT NULL,
  slot               TINYINT UNSIGNED NOT NULL DEFAULT 1,  -- 1-4
  PRIMARY KEY (trainer_pokemon_id, slot),
  FOREIGN KEY (trainer_pokemon_id) REFERENCES trainer_pokemon(id),
  FOREIGN KEY (move_id)            REFERENCES moves(id)
);

-- ── Equipos de usuario (para la página de batalla) ─
CREATE TABLE IF NOT EXISTS user_teams (
  id         INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  name       VARCHAR(60) NOT NULL DEFAULT 'Mi equipo',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_team_pokemon (
  id         INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  team_id    INT UNSIGNED NOT NULL,
  pokemon_id SMALLINT UNSIGNED NOT NULL,
  slot       TINYINT UNSIGNED NOT NULL DEFAULT 1,
  FOREIGN KEY (team_id)    REFERENCES user_teams(id) ON DELETE CASCADE,
  FOREIGN KEY (pokemon_id) REFERENCES pokemon(id)
);

CREATE TABLE IF NOT EXISTS user_team_pokemon_moves (
  team_pokemon_id INT UNSIGNED NOT NULL,
  move_id         SMALLINT UNSIGNED NOT NULL,
  slot            TINYINT UNSIGNED NOT NULL DEFAULT 1,
  PRIMARY KEY (team_pokemon_id, slot),
  FOREIGN KEY (team_pokemon_id) REFERENCES user_team_pokemon(id) ON DELETE CASCADE,
  FOREIGN KEY (move_id)         REFERENCES moves(id)
);

SET foreign_key_checks = 1;
