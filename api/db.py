"""
Capa de acceso a BD: PostgreSQL (Supabase) o MariaDB (local/Docker).
Prioridad: DATABASE_URL → Postgres. Si no, DB_HOST → MariaDB.
"""
from __future__ import annotations

import os
import re
from contextlib import contextmanager
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / '.env')

BACKEND: str  # 'postgres' | 'mysql'

if os.environ.get('DATABASE_URL'):
    BACKEND = 'postgres'
    import psycopg2
    import psycopg2.extras
else:
    BACKEND = 'mysql'
    import pymysql
    import pymysql.cursors

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', '127.0.0.1'),
    'port': int(os.environ.get('DB_PORT', 3306)),
    'user': os.environ.get('DB_USER', 'pokeweb_user'),
    'password': os.environ.get('DB_PASS', 'pokeweb_pass'),
    'database': os.environ.get('DB_NAME', 'pokeweb'),
    'charset': 'utf8mb4',
}
DATABASE_URL = os.environ.get('DATABASE_URL', '')


def is_postgres() -> bool:
    return BACKEND == 'postgres'


def group_concat(column: str, order_by: str) -> str:
    """Agregación de tipos por pokémon."""
    if is_postgres():
        return f"STRING_AGG({column}::text, ',' ORDER BY {order_by})"
    return f"GROUP_CONCAT({column} ORDER BY {order_by})"


def connect():
    if is_postgres():
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = False
        return conn
    return pymysql.connect(
        **DB_CONFIG,
        cursorclass=pymysql.cursors.DictCursor,
    )


@contextmanager
def cursor(conn):
    if is_postgres():
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    else:
        cur = conn.cursor()
    try:
        yield cur
    finally:
        cur.close()


def query(sql: str, params=None) -> list[dict]:
    conn = connect()
    try:
        with cursor(conn) as cur:
            cur.execute(sql, params or ())
            return list(cur.fetchall())
    finally:
        conn.close()


def query_one(sql: str, params=None) -> dict | None:
    rows = query(sql, params)
    return rows[0] if rows else None


def execute(sql: str, params=None) -> int:
    conn = connect()
    try:
        with cursor(conn) as cur:
            cur.execute(sql, params or ())
            conn.commit()
            if is_postgres():
                if cur.description:
                    row = cur.fetchone()
                    if row and 'id' in row:
                        return int(row['id'])
                return 0
            return int(cur.lastrowid or 0)
    finally:
        conn.close()


def execute_returning_id(sql: str, params=None) -> int:
    """INSERT ... RETURNING id (Postgres) o lastrowid (MySQL)."""
    if is_postgres() and 'RETURNING' not in sql.upper():
        sql = sql.rstrip().rstrip(';') + ' RETURNING id'
    return execute(sql, params)


def health_label() -> str:
    if is_postgres():
        parsed = urlparse(DATABASE_URL)
        return parsed.hostname or 'supabase'
    return DB_CONFIG['host']


# ── SQL dialect helpers (import_db) ───────────────────────────────────────────

def insert_ignore_types() -> str:
    if is_postgres():
        return 'INSERT INTO types (name_en, name_es) VALUES (%s,%s) ON CONFLICT (name_en) DO NOTHING'
    return 'INSERT IGNORE INTO types (name_en, name_es) VALUES (%s,%s)'


def upsert_type_effectiveness() -> str:
    if is_postgres():
        return '''INSERT INTO type_effectiveness (attack_type_id, defend_type_id, multiplier)
                  VALUES (%s,%s,%s)
                  ON CONFLICT (attack_type_id, defend_type_id) DO UPDATE SET multiplier = EXCLUDED.multiplier'''
    return '''INSERT INTO type_effectiveness (attack_type_id, defend_type_id, multiplier)
              VALUES (%s,%s,%s) ON DUPLICATE KEY UPDATE multiplier=VALUES(multiplier)'''


def insert_ignore_moves() -> str:
    if is_postgres():
        return '''INSERT INTO moves (name, name_es, type_id, category, power, accuracy, pp)
                  VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (name) DO NOTHING'''
    return '''INSERT IGNORE INTO moves (name, name_es, type_id, category, power, accuracy, pp) VALUES (%s,%s,%s,%s,%s,%s,%s)'''


def upsert_pokemon() -> str:
    if is_postgres():
        return '''INSERT INTO pokemon
               (id, name, name_es, sprite_url, hp, attack, defense,
                sp_attack, sp_defense, speed, is_legendary, evo_family_id)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
               ON CONFLICT (id) DO UPDATE SET
                 name_es=EXCLUDED.name_es, sprite_url=EXCLUDED.sprite_url,
                 hp=EXCLUDED.hp, attack=EXCLUDED.attack, defense=EXCLUDED.defense,
                 sp_attack=EXCLUDED.sp_attack, sp_defense=EXCLUDED.sp_defense,
                 speed=EXCLUDED.speed, is_legendary=EXCLUDED.is_legendary,
                 evo_family_id=EXCLUDED.evo_family_id'''
    return '''INSERT INTO pokemon
               (id, name, name_es, sprite_url, hp, attack, defense,
                sp_attack, sp_defense, speed, is_legendary, evo_family_id)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
               ON DUPLICATE KEY UPDATE
                 name_es=VALUES(name_es), sprite_url=VALUES(sprite_url),
                 hp=VALUES(hp), attack=VALUES(attack), defense=VALUES(defense),
                 sp_attack=VALUES(sp_attack), sp_defense=VALUES(sp_defense),
                 speed=VALUES(speed), is_legendary=VALUES(is_legendary),
                 evo_family_id=VALUES(evo_family_id)'''


def insert_ignore_pokemon_types() -> str:
    if is_postgres():
        return 'INSERT INTO pokemon_types (pokemon_id,type_id,slot) VALUES(%s,%s,%s) ON CONFLICT DO NOTHING'
    return 'INSERT IGNORE INTO pokemon_types (pokemon_id,type_id,slot) VALUES(%s,%s,%s)'


def insert_ignore_pokemon_moves() -> str:
    if is_postgres():
        return '''INSERT INTO pokemon_moves (pokemon_id,move_id,learn_method,level)
                  VALUES(%s,%s,%s,%s) ON CONFLICT DO NOTHING'''
    return '''INSERT IGNORE INTO pokemon_moves (pokemon_id,move_id,learn_method,level) VALUES(%s,%s,%s,%s)'''


def upsert_game() -> str:
    if is_postgres():
        return '''INSERT INTO games (slug, name, region, gen)
                  VALUES (%s,%s,%s,%s)
                  ON CONFLICT (slug) DO UPDATE SET
                    name=EXCLUDED.name, region=EXCLUDED.region, gen=EXCLUDED.gen'''
    return '''INSERT INTO games (slug, name, region, gen)
               VALUES (%s,%s,%s,%s)
               ON DUPLICATE KEY UPDATE name=VALUES(name), region=VALUES(region), gen=VALUES(gen)'''


def upsert_trainer() -> str:
    if is_postgres():
        return '''INSERT INTO trainers
                   (slug, name, name_es, trainer_class, game_id, gym_order,
                    badge_name, specialty, location, sprite_url, team_by_starter)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                   ON CONFLICT (game_id, slug) DO UPDATE SET
                     name=EXCLUDED.name, name_es=EXCLUDED.name_es,
                     trainer_class=EXCLUDED.trainer_class, gym_order=EXCLUDED.gym_order,
                     badge_name=EXCLUDED.badge_name, specialty=EXCLUDED.specialty,
                     location=EXCLUDED.location, sprite_url=EXCLUDED.sprite_url,
                     team_by_starter=EXCLUDED.team_by_starter'''
    return '''INSERT INTO trainers
               (slug, name, name_es, trainer_class, game_id, gym_order,
                badge_name, specialty, location, sprite_url, team_by_starter)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
               ON DUPLICATE KEY UPDATE
                 name=VALUES(name), name_es=VALUES(name_es),
                 trainer_class=VALUES(trainer_class), gym_order=VALUES(gym_order),
                 badge_name=VALUES(badge_name), specialty=VALUES(specialty),
                 location=VALUES(location), sprite_url=VALUES(sprite_url),
                 team_by_starter=VALUES(team_by_starter)'''


def upsert_trainer_pokemon_move() -> str:
    if is_postgres():
        return '''INSERT INTO trainer_pokemon_moves (trainer_pokemon_id, move_id, slot)
                  VALUES (%s,%s,%s)
                  ON CONFLICT (trainer_pokemon_id, slot) DO UPDATE SET move_id=EXCLUDED.move_id'''
    return '''INSERT INTO trainer_pokemon_moves (trainer_pokemon_id, move_id, slot)
               VALUES (%s,%s,%s) ON DUPLICATE KEY UPDATE move_id=VALUES(move_id)'''


def truncate_tables(tables: list[str]) -> None:
    """Vacía tablas respetando FK."""
    valid = [t for t in tables if re.match(r'^[a-zA-Z0-9_]+$', t)]
    if not valid:
        return
    conn = connect()
    try:
        with cursor(conn) as cur:
            if is_postgres():
                cur.execute(
                    f"TRUNCATE {', '.join(valid)} RESTART IDENTITY CASCADE"
                )
            else:
                cur.execute('SET FOREIGN_KEY_CHECKS=0')
                for t in valid:
                    cur.execute(f'DELETE FROM {t}')
                cur.execute('SET FOREIGN_KEY_CHECKS=1')
            conn.commit()
    finally:
        conn.close()

