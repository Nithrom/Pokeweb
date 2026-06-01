"""
Capa de acceso a BD: MariaDB (local/Docker) o PostgreSQL (Supabase).

Variables:
  Supabase: DATABASE_URL=postgresql://user:pass@host:5432/postgres
  MariaDB:  DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME
"""
from __future__ import annotations

import os
import re
from typing import Any

try:
    from dotenv import load_dotenv

    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
except ImportError:
    pass

_BACKEND: str | None = None


def get_backend() -> str:
    global _BACKEND
    if _BACKEND is None:
        url = (os.environ.get('DATABASE_URL') or '').strip()
        if url.startswith(('postgres://', 'postgresql://')):
            _BACKEND = 'postgres'
        elif os.environ.get('DB_BACKEND', '').lower() in (
            'postgres', 'postgresql', 'supabase',
        ):
            _BACKEND = 'postgres'
        else:
            _BACKEND = 'mysql'
    return _BACKEND


def missing_database_config_hint() -> str | None:
    """Mensaje si en cloud no hay DATABASE_URL (evita confusión con 127.0.0.1)."""
    if (os.environ.get('DATABASE_URL') or '').strip():
        return None
    if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('RAILWAY_PROJECT_ID'):
        return (
            'En Railway falta la variable DATABASE_URL (URI de Supabase). '
            'Project Settings → Database → Connection string → URI.'
        )
    return None


def is_postgres() -> bool:
    return get_backend() == 'postgres'


def mysql_config() -> dict:
    import pymysql

    return {
        'host': os.environ.get('DB_HOST', '127.0.0.1'),
        'port': int(os.environ.get('DB_PORT', 3306)),
        'user': os.environ.get('DB_USER', 'pokeweb_user'),
        'password': os.environ.get('DB_PASS', 'pokeweb_pass'),
        'database': os.environ.get('DB_NAME', 'pokeweb'),
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
    }


def db_label() -> str:
    if is_postgres():
        url = os.environ.get('DATABASE_URL', '')
        if '@' in url:
            host = url.split('@', 1)[1].split('/')[0].split(':')[0]
            return f'PostgreSQL ({host})'
        return 'PostgreSQL'
    cfg = mysql_config()
    return f'MariaDB ({cfg["host"]})'


def connect():
    if is_postgres():
        import psycopg2

        return psycopg2.connect(os.environ['DATABASE_URL'])
    import pymysql

    return pymysql.connect(**mysql_config())


def cursor(conn):
    if is_postgres():
        from psycopg2.extras import RealDictCursor

        return conn.cursor(cursor_factory=RealDictCursor)
    return conn.cursor()


def group_concat(column: str, order_by: str) -> str:
    if is_postgres():
        return f"STRING_AGG({column}::text, ',' ORDER BY {order_by})"
    return f'GROUP_CONCAT({column} ORDER BY {order_by})'


def types_agg_join(alias: str = 'pt_agg', pokemon_fk: str = 'p.id') -> str:
    """JOIN que agrega tipos por pokemon (evita GROUP BY en filas de equipo)."""
    gc_en = group_concat('t.name_en', 'pt.slot')
    gc_es = group_concat('t.name_es', 'pt.slot')
    return f"""
        LEFT JOIN (
            SELECT pt.pokemon_id,
                   {gc_en} AS types_en,
                   {gc_es} AS types_es
            FROM pokemon_types pt
            JOIN types t ON t.id = pt.type_id
            GROUP BY pt.pokemon_id
        ) {alias} ON {alias}.pokemon_id = {pokemon_fk}
    """


def schema_name() -> str:
    if is_postgres():
        return 'public'
    return mysql_config()['database']


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
            if is_postgres() and cur.description:
                row = cur.fetchone()
                if row and 'id' in row:
                    return int(row['id'])
            return int(getattr(cur, 'lastrowid', 0) or 0)
    finally:
        conn.close()


def insert_returning_id(cur, sql: str, params: tuple, id_col: str = 'id') -> int:
    if is_postgres():
        cur.execute(f'{sql.rstrip(";")} RETURNING {id_col}', params)
        row = cur.fetchone()
        if not row:
            raise RuntimeError('INSERT sin RETURNING')
        return int(row[id_col])
    cur.execute(sql, params)
    return int(cur.lastrowid)


# ── SQL específico por motor (import_db) ─────────────────────────────────────

def sql_insert_ignore_types() -> str:
    if is_postgres():
        return (
            'INSERT INTO types (name_en, name_es) VALUES (%s,%s) '
            'ON CONFLICT (name_en) DO NOTHING'
        )
    return 'INSERT IGNORE INTO types (name_en, name_es) VALUES (%s,%s)'


def sql_upsert_effectiveness() -> str:
    if is_postgres():
        return (
            'INSERT INTO type_effectiveness (attack_type_id, defend_type_id, multiplier) '
            'VALUES (%s,%s,%s) ON CONFLICT (attack_type_id, defend_type_id) '
            'DO UPDATE SET multiplier = EXCLUDED.multiplier'
        )
    return (
        'INSERT INTO type_effectiveness (attack_type_id, defend_type_id, multiplier) '
        'VALUES (%s,%s,%s) ON DUPLICATE KEY UPDATE multiplier=VALUES(multiplier)'
    )


def sql_insert_ignore_move() -> str:
    if is_postgres():
        return (
            'INSERT INTO moves (name, name_es, type_id, category, power, accuracy, pp) '
            'VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (name) DO NOTHING'
        )
    return (
        'INSERT IGNORE INTO moves (name, name_es, type_id, category, power, accuracy, pp) '
        'VALUES (%s,%s,%s,%s,%s,%s,%s)'
    )


def sql_upsert_pokemon() -> str:
    if is_postgres():
        return (
            'INSERT INTO pokemon (id, name, name_es, sprite_url, hp, attack, defense, '
            'sp_attack, sp_defense, speed, is_legendary, evo_family_id) '
            'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '
            'ON CONFLICT (id) DO UPDATE SET '
            'name_es=EXCLUDED.name_es, sprite_url=EXCLUDED.sprite_url, '
            'hp=EXCLUDED.hp, attack=EXCLUDED.attack, defense=EXCLUDED.defense, '
            'sp_attack=EXCLUDED.sp_attack, sp_defense=EXCLUDED.sp_defense, '
            'speed=EXCLUDED.speed, is_legendary=EXCLUDED.is_legendary, '
            'evo_family_id=EXCLUDED.evo_family_id'
        )
    return (
        'INSERT INTO pokemon (id, name, name_es, sprite_url, hp, attack, defense, '
        'sp_attack, sp_defense, speed, is_legendary, evo_family_id) '
        'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '
        'ON DUPLICATE KEY UPDATE name_es=VALUES(name_es), sprite_url=VALUES(sprite_url), '
        'hp=VALUES(hp), attack=VALUES(attack), defense=VALUES(defense), '
        'sp_attack=VALUES(sp_attack), sp_defense=VALUES(sp_defense), '
        'speed=VALUES(speed), is_legendary=VALUES(is_legendary), '
        'evo_family_id=VALUES(evo_family_id)'
    )


def sql_insert_ignore_pokemon_types() -> str:
    if is_postgres():
        return (
            'INSERT INTO pokemon_types (pokemon_id, type_id, slot) VALUES (%s,%s,%s) '
            'ON CONFLICT (pokemon_id, slot) DO NOTHING'
        )
    return 'INSERT IGNORE INTO pokemon_types (pokemon_id,type_id,slot) VALUES(%s,%s,%s)'


def sql_insert_ignore_pokemon_moves() -> str:
    if is_postgres():
        return (
            'INSERT INTO pokemon_moves (pokemon_id, move_id, learn_method, level) '
            'VALUES(%s,%s,%s,%s) ON CONFLICT (pokemon_id, move_id) DO NOTHING'
        )
    return (
        'INSERT IGNORE INTO pokemon_moves (pokemon_id,move_id,learn_method,level) '
        'VALUES(%s,%s,%s,%s)'
    )


def sql_upsert_game() -> str:
    if is_postgres():
        return (
            'INSERT INTO games (slug, name, region, gen) VALUES (%s,%s,%s,%s) '
            'ON CONFLICT (slug) DO UPDATE SET '
            'name=EXCLUDED.name, region=EXCLUDED.region, gen=EXCLUDED.gen'
        )
    return (
        'INSERT INTO games (slug, name, region, gen) VALUES (%s,%s,%s,%s) '
        'ON DUPLICATE KEY UPDATE name=VALUES(name), region=VALUES(region), gen=VALUES(gen)'
    )


def sql_upsert_trainer() -> str:
    if is_postgres():
        return (
            'INSERT INTO trainers (slug, name, name_es, trainer_class, game_id, gym_order, '
            'badge_name, specialty, location, sprite_url, team_by_starter) '
            'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '
            'ON CONFLICT (game_id, slug) DO UPDATE SET '
            'name=EXCLUDED.name, name_es=EXCLUDED.name_es, '
            'trainer_class=EXCLUDED.trainer_class, gym_order=EXCLUDED.gym_order, '
            'badge_name=EXCLUDED.badge_name, specialty=EXCLUDED.specialty, '
            'location=EXCLUDED.location, sprite_url=EXCLUDED.sprite_url, '
            'team_by_starter=EXCLUDED.team_by_starter'
        )
    return (
        'INSERT INTO trainers (slug, name, name_es, trainer_class, game_id, gym_order, '
        'badge_name, specialty, location, sprite_url, team_by_starter) '
        'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '
        'ON DUPLICATE KEY UPDATE name=VALUES(name), name_es=VALUES(name_es), '
        'trainer_class=VALUES(trainer_class), gym_order=VALUES(gym_order), '
        'badge_name=VALUES(badge_name), specialty=VALUES(specialty), '
        'location=VALUES(location), sprite_url=VALUES(sprite_url), '
        'team_by_starter=VALUES(team_by_starter)'
    )


def sql_insert_trainer_pokemon() -> str:
    return (
        'INSERT INTO trainer_pokemon (trainer_id, pokemon_id, level, slot) '
        'VALUES (%s,%s,%s,%s)'
    )


def sql_upsert_trainer_pokemon_move() -> str:
    if is_postgres():
        return (
            'INSERT INTO trainer_pokemon_moves (trainer_pokemon_id, move_id, slot) '
            'VALUES (%s,%s,%s) ON CONFLICT (trainer_pokemon_id, slot) '
            'DO UPDATE SET move_id = EXCLUDED.move_id'
        )
    return (
        'INSERT INTO trainer_pokemon_moves (trainer_pokemon_id, move_id, slot) '
        'VALUES (%s,%s,%s) ON DUPLICATE KEY UPDATE move_id=VALUES(move_id)'
    )


def reset_table_autoincrement(cur, table: str) -> None:
    if not re.match(r'^[a-zA-Z0-9_]+$', table):
        raise ValueError(f'Tabla inválida: {table}')
    cur.execute(f'SELECT COALESCE(MAX(id), 0) AS m FROM {table}')
    nxt = int(cur.fetchone()['m']) + 1
    if is_postgres():
        cur.execute(
            "SELECT setval(pg_get_serial_sequence(%s, 'id'), %s, false)",
            (table, nxt),
        )
    else:
        cur.execute(f'ALTER TABLE {table} AUTO_INCREMENT = %s', (nxt,))


def column_exists(cur, table: str, column: str) -> bool:
    if is_postgres():
        cur.execute(
            '''SELECT 1 FROM information_schema.columns
               WHERE table_schema = %s AND table_name = %s AND column_name = %s''',
            (schema_name(), table, column),
        )
    else:
        cur.execute(
            '''SELECT 1 FROM information_schema.COLUMNS
               WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s AND COLUMN_NAME=%s''',
            (schema_name(), table, column),
        )
    return cur.fetchone() is not None


def column_type(cur, table: str, column: str) -> str:
    if is_postgres():
        cur.execute(
            '''SELECT data_type FROM information_schema.columns
               WHERE table_schema = %s AND table_name = %s AND column_name = %s''',
            (schema_name(), table, column),
        )
    else:
        cur.execute(
            '''SELECT COLUMN_TYPE FROM information_schema.COLUMNS
               WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s AND COLUMN_NAME=%s''',
            (schema_name(), table, column),
        )
    row = cur.fetchone()
    if not row:
        return ''
    return (row.get('data_type') or row.get('COLUMN_TYPE') or '').lower()


def operational_error_type():
    if is_postgres():
        import psycopg2

        return psycopg2.Error
    import pymysql

    return pymysql.err.OperationalError
