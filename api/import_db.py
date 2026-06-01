"""
import_db.py — Importa pokemon_db.json y trainers_db.json a MariaDB
====================================================================
Uso local (MariaDB en tu PC):
  set DB_HOST=127.0.0.1
  set DB_USER=pokeweb_user
  set DB_PASS=pokeweb_pass
  python import_db.py --reset

Docker:
  docker exec pokeweb_api python import_db.py --reset

Opciones:
  --reset          Vacía tablas ANTES de importar (¡borra datos existentes!)
  --only pokemon   Solo pokémon, movimientos y tipos
  --only trainers  Solo juegos y entrenadores (requiere pokémon ya importados).
                   Con --reset NO borra la tabla pokemon (solo entrenadores).

Recuperar todo desde cero (local):
  python import_db.py --reset

Si ves 0 Pokémon en la web pero el import terminó bien:
  python import_db.py --only pokemon --reset
  Reinicia Flask / docker compose restart api
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import unicodedata

import pymysql

# ── Rutas ─────────────────────────────────────────────────────────────────────
API_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(API_DIR)
DATA_DIR = os.environ.get('DATA_DIR', os.path.join(ROOT_DIR, 'data'))


def _first_existing(*paths: str) -> str | None:
    for p in paths:
        if p and os.path.isfile(p):
            return p
    return None


def pokemon_json_path() -> str | None:
    return _first_existing(
        os.path.join(API_DIR, 'pokemon_db.json'),
        os.path.join(DATA_DIR, 'pokemon_db.json'),
    )


def trainers_json_path() -> str | None:
    return _first_existing(
        os.path.join(API_DIR, 'trainers_db.json'),
        os.path.join(DATA_DIR, 'trainers_db.json'),
    )


# ── BD ────────────────────────────────────────────────────────────────────────
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', '127.0.0.1'),
    'port': int(os.environ.get('DB_PORT', 3306)),
    'user': os.environ.get('DB_USER', 'pokeweb_user'),
    'password': os.environ.get('DB_PASS', 'pokeweb_pass'),
    'database': os.environ.get('DB_NAME', 'pokeweb'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}

TIPOS_ES = {
    'normal': 'Normal', 'fighting': 'Lucha', 'flying': 'Volador', 'poison': 'Veneno',
    'ground': 'Tierra', 'rock': 'Roca', 'bug': 'Bicho', 'ghost': 'Fantasma',
    'steel': 'Acero', 'fire': 'Fuego', 'water': 'Agua', 'grass': 'Planta',
    'electric': 'Eléctrico', 'psychic': 'Psíquico', 'ice': 'Hielo',
    'dragon': 'Dragón', 'dark': 'Siniestro', 'fairy': 'Hada',
}

EFF = {
    'normal': {'normal': 1, 'fighting': 1, 'flying': 1, 'poison': 1, 'ground': 1, 'rock': 0.5, 'bug': 1, 'ghost': 0, 'steel': 0.5, 'fire': 1, 'water': 1, 'grass': 1, 'electric': 1, 'psychic': 1, 'ice': 1, 'dragon': 1, 'dark': 1, 'fairy': 1},
    'fighting': {'normal': 2, 'fighting': 1, 'flying': 0.5, 'poison': 0.5, 'ground': 1, 'rock': 2, 'bug': 0.5, 'ghost': 0, 'steel': 2, 'fire': 1, 'water': 1, 'grass': 1, 'electric': 1, 'psychic': 0.5, 'ice': 2, 'dragon': 1, 'dark': 2, 'fairy': 0.5},
    'flying': {'normal': 1, 'fighting': 2, 'flying': 1, 'poison': 1, 'ground': 1, 'rock': 0.5, 'bug': 2, 'ghost': 1, 'steel': 0.5, 'fire': 1, 'water': 1, 'grass': 2, 'electric': 0.5, 'psychic': 1, 'ice': 1, 'dragon': 1, 'dark': 1, 'fairy': 1},
    'poison': {'normal': 1, 'fighting': 1, 'flying': 1, 'poison': 0.5, 'ground': 0.5, 'rock': 0.5, 'bug': 1, 'ghost': 0.5, 'steel': 0, 'fire': 1, 'water': 1, 'grass': 2, 'electric': 1, 'psychic': 1, 'ice': 1, 'dragon': 1, 'dark': 1, 'fairy': 2},
    'ground': {'normal': 1, 'fighting': 1, 'flying': 0, 'poison': 2, 'ground': 1, 'rock': 2, 'bug': 0.5, 'ghost': 1, 'steel': 2, 'fire': 2, 'water': 1, 'grass': 0.5, 'electric': 2, 'psychic': 1, 'ice': 1, 'dragon': 1, 'dark': 1, 'fairy': 1},
    'rock': {'normal': 1, 'fighting': 0.5, 'flying': 2, 'poison': 1, 'ground': 0.5, 'rock': 1, 'bug': 2, 'ghost': 1, 'steel': 0.5, 'fire': 2, 'water': 1, 'grass': 1, 'electric': 1, 'psychic': 1, 'ice': 2, 'dragon': 1, 'dark': 1, 'fairy': 1},
    'bug': {'normal': 1, 'fighting': 0.5, 'flying': 0.5, 'poison': 0.5, 'ground': 1, 'rock': 1, 'bug': 1, 'ghost': 0.5, 'steel': 0.5, 'fire': 0.5, 'water': 1, 'grass': 2, 'electric': 1, 'psychic': 2, 'ice': 1, 'dragon': 1, 'dark': 2, 'fairy': 0.5},
    'ghost': {'normal': 0, 'fighting': 1, 'flying': 1, 'poison': 1, 'ground': 1, 'rock': 1, 'bug': 1, 'ghost': 2, 'steel': 1, 'fire': 1, 'water': 1, 'grass': 1, 'electric': 1, 'psychic': 2, 'ice': 1, 'dragon': 1, 'dark': 0.5, 'fairy': 1},
    'steel': {'normal': 1, 'fighting': 1, 'flying': 1, 'poison': 1, 'ground': 1, 'rock': 2, 'bug': 1, 'ghost': 1, 'steel': 0.5, 'fire': 0.5, 'water': 0.5, 'grass': 1, 'electric': 0.5, 'psychic': 1, 'ice': 2, 'dragon': 1, 'dark': 1, 'fairy': 2},
    'fire': {'normal': 1, 'fighting': 1, 'flying': 1, 'poison': 1, 'ground': 1, 'rock': 0.5, 'bug': 2, 'ghost': 1, 'steel': 2, 'fire': 0.5, 'water': 0.5, 'grass': 2, 'electric': 1, 'psychic': 1, 'ice': 2, 'dragon': 0.5, 'dark': 1, 'fairy': 1},
    'water': {'normal': 1, 'fighting': 1, 'flying': 1, 'poison': 1, 'ground': 2, 'rock': 2, 'bug': 1, 'ghost': 1, 'steel': 1, 'fire': 2, 'water': 0.5, 'grass': 0.5, 'electric': 1, 'psychic': 1, 'ice': 1, 'dragon': 0.5, 'dark': 1, 'fairy': 1},
    'grass': {'normal': 1, 'fighting': 1, 'flying': 0.5, 'poison': 0.5, 'ground': 2, 'rock': 2, 'bug': 0.5, 'ghost': 1, 'steel': 0.5, 'fire': 0.5, 'water': 2, 'grass': 0.5, 'electric': 1, 'psychic': 1, 'ice': 1, 'dragon': 0.5, 'dark': 1, 'fairy': 1},
    'electric': {'normal': 1, 'fighting': 1, 'flying': 2, 'poison': 1, 'ground': 0, 'rock': 1, 'bug': 1, 'ghost': 1, 'steel': 1, 'fire': 1, 'water': 2, 'grass': 0.5, 'electric': 0.5, 'psychic': 1, 'ice': 1, 'dragon': 0.5, 'dark': 1, 'fairy': 1},
    'psychic': {'normal': 1, 'fighting': 2, 'flying': 1, 'poison': 2, 'ground': 1, 'rock': 1, 'bug': 1, 'ghost': 1, 'steel': 0.5, 'fire': 1, 'water': 1, 'grass': 1, 'electric': 1, 'psychic': 0.5, 'ice': 1, 'dragon': 1, 'dark': 0, 'fairy': 1},
    'ice': {'normal': 1, 'fighting': 1, 'flying': 2, 'poison': 1, 'ground': 2, 'rock': 1, 'bug': 1, 'ghost': 1, 'steel': 0.5, 'fire': 0.5, 'water': 0.5, 'grass': 2, 'electric': 1, 'psychic': 1, 'ice': 0.5, 'dragon': 2, 'dark': 1, 'fairy': 1},
    'dragon': {'normal': 1, 'fighting': 1, 'flying': 1, 'poison': 1, 'ground': 1, 'rock': 1, 'bug': 1, 'ghost': 1, 'steel': 0.5, 'fire': 1, 'water': 1, 'grass': 1, 'electric': 1, 'psychic': 1, 'ice': 1, 'dragon': 2, 'dark': 1, 'fairy': 0},
    'dark': {'normal': 1, 'fighting': 0.5, 'flying': 1, 'poison': 1, 'ground': 1, 'rock': 1, 'bug': 1, 'ghost': 2, 'steel': 1, 'fire': 1, 'water': 1, 'grass': 1, 'electric': 1, 'psychic': 2, 'ice': 1, 'dragon': 1, 'dark': 0.5, 'fairy': 0.5},
    'fairy': {'normal': 1, 'fighting': 2, 'flying': 1, 'poison': 0.5, 'ground': 1, 'rock': 1, 'bug': 1, 'ghost': 1, 'steel': 0.5, 'fire': 0.5, 'water': 1, 'grass': 1, 'electric': 1, 'psychic': 1, 'ice': 1, 'dragon': 2, 'dark': 2, 'fairy': 1},
}

EVO_FAMILY_IDS = {
    1, 4, 7, 10, 13, 16, 19, 21, 23, 25, 27, 29, 32, 35, 37, 39, 41, 43, 46, 48, 50, 52, 54, 56, 58,
    60, 63, 66, 69, 72, 74, 77, 79, 81, 83, 84, 86, 88, 90, 92, 95, 96, 98, 100, 102, 104, 106, 107,
    108, 109, 111, 113, 114, 115, 116, 118, 120, 122, 123, 124, 125, 126, 127, 128, 129, 131, 132,
    133, 137, 138, 140, 142, 143, 144, 145, 146, 147, 150, 151, 152, 155, 158, 161, 163, 165, 167,
    169, 170, 172, 173, 174, 175, 177, 179, 183, 185, 187, 190, 191, 193, 194, 196, 197, 198, 200,
    201, 202, 203, 204, 206, 207, 209, 211, 213, 214, 215, 216, 218, 220, 222, 223, 225, 226, 227,
    228, 231, 233, 234, 235, 236, 238, 239, 240, 241, 242, 243, 244, 245, 246, 249, 250, 251, 252,
    255, 258, 261, 263, 265, 270, 273, 276, 278, 280, 283, 285, 287, 290, 293, 296, 298, 299, 300,
    302, 303, 304, 306, 307, 309, 311, 312, 313, 314, 315, 316, 318, 320, 322, 324, 325, 327, 328,
    331, 333, 335, 336, 337, 338, 339, 341, 343, 345, 347, 349, 351, 352, 353, 355, 357, 358, 359,
    360, 361, 363, 366, 369, 370, 371, 374, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387,
    390, 393, 396, 399, 401, 403, 406, 408, 410, 412, 415, 417, 418, 420, 422, 424, 425, 427, 429,
    430, 431, 433, 434, 436, 438, 439, 440, 441, 442, 443, 446, 447, 449, 451, 453, 455, 456, 458,
    459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477,
    478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 491, 492, 493, 494, 495, 498, 501,
    504, 506, 509, 511, 513, 515, 517, 519, 522, 524, 527, 529, 531, 532, 535, 538, 539, 540, 543,
    546, 548, 550, 551, 554, 556, 557, 559, 561, 562, 564, 566, 568, 570, 572, 574, 577, 580, 582,
    585, 587, 588, 590, 592, 594, 595, 597, 599, 602, 605, 607, 610, 613, 615, 616, 618, 619, 621,
    622, 624, 626, 627, 629, 631, 632, 633, 636, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647,
    648, 649, 650, 653, 656, 659, 662, 665, 668, 671, 672, 674, 676, 677, 679, 682, 684, 686, 688,
    690, 692, 694, 696, 698, 700, 701, 702, 703, 704, 707, 708, 710, 712, 714, 716, 717, 718, 719,
    720, 721, 722, 725, 728, 731, 734, 736, 739, 741, 742, 744, 746, 747, 749, 751, 753, 755, 757,
    759, 761, 764, 765, 766, 767, 769, 771, 772, 774, 775, 776, 777, 778, 779, 780, 781, 782, 785,
    786, 787, 788, 789, 791, 792, 793, 800, 801, 802, 803, 806, 807, 808, 810, 813, 816, 819, 821,
    824, 826, 827, 829, 831, 833, 835, 837, 840, 842, 843, 845, 846, 847, 848, 850, 852, 854, 856,
    858, 859, 862, 863, 864, 865, 866, 867, 868, 870, 871, 872, 874, 875, 876, 877, 878, 880, 881,
    882, 883, 884, 885, 888, 889, 890, 891, 892, 893, 894, 895, 896, 897, 898, 899, 900, 901, 902,
    903, 904, 905, 906, 909, 912, 915, 918, 921, 922, 923, 924, 925, 926, 927, 928, 929, 930, 931,
    932, 933, 934, 935, 936, 937, 938, 939, 940, 941, 942, 943, 944, 945, 946, 947, 948, 949, 950,
    951, 952, 953, 954, 955, 956, 957, 958, 959, 960, 961, 962, 963, 964, 965, 966, 967, 968, 969,
    970, 971, 972, 973, 974, 975, 976, 977, 978, 979, 980, 981, 982, 983, 984, 985, 986, 987, 988,
    989, 990, 991, 992, 993, 994, 995, 996, 997, 998, 999, 1000, 1001, 1002, 1003, 1004, 1005,
    1006, 1007, 1008, 1009, 1010, 1017, 1020, 1021, 1022, 1023, 1024, 1025,
}

# Nombres genéricos en trainers_db → forma en pokemon_db
MOVE_SLUG_ALIASES = {
    'thundershock': 'thunder-shock',
    'thunderpunch': 'thunder-punch',
    'poisonpowder': 'poison-powder',
    'sonicboom': 'sonic-boom',
    'doubleslap': 'double-slap',
    'doublekick': 'double-kick',
    'selfdestruct': 'self-destruct',
    'smokescreen': 'smoke-screen',
    'bubblebeam': 'bubble-beam',
    'hijumpkick': 'high-jump-kick',
    'hi-jump-kick': 'high-jump-kick',
    'pinmissile': 'pin-missile',
    'sonicboom': 'sonic-boom',
    'thundershock': 'thunder-shock',
    'dynamicpunch': 'dynamic-punch',
    'dragonbreath': 'dragon-breath',
    'smokescreen': 'smoke-screen',
    'sandattack': 'sand-attack',
    'faintattack': 'feint-attack',
    'ancientpower': 'ancient-power',
    'stringshot': 'string-shot',
    'doubleslap': 'double-slap',
}

POKEMON_ALIASES = {
    'jellicent': 'jellicent-male',
    'aegislash': 'aegislash-shield',
    'mimikyu': 'mimikyu-disguised',
    'meowstic': 'meowstic-male',
    'pyroar': 'pyroar-male',
    'gourgeist': 'gourgeist-average',
    'oricorio': 'oricorio-baile',
    'toxtricity': 'toxtricity-amped',
    'oinkologne': 'oinkologne-male',
    'dudunsparce': 'dudunsparce-two-segment',
}

RESET_ALL = [
    'trainer_pokemon_moves', 'trainer_pokemon', 'trainers', 'games',
    'user_team_pokemon_moves', 'user_team_pokemon', 'user_teams',
    'pokemon_moves', 'pokemon_types', 'pokemon',
    'type_effectiveness', 'moves', 'types',
]
RESET_POKEMON = ['pokemon_moves', 'pokemon_types', 'pokemon', 'type_effectiveness', 'moves', 'types']
RESET_TRAINERS = ['trainer_pokemon_moves', 'trainer_pokemon', 'trainers', 'games']


def slugify(text: str) -> str:
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^a-zA-Z0-9]+', '-', text.lower()).strip('-')
    return text or 'trainer'


def trainer_slug(tr: dict, game_slug: str | None = None) -> str:
    """Único por juego: specialty + rol + orden (evita pisar Hala kahuna vs elite4)."""
    parts = [
        slugify((tr.get('specialty') or '').strip() or tr.get('name', 'trainer')),
        slugify(tr.get('type') or 'other'),
        str(tr.get('order') or 0),
    ]
    base = '-'.join(p for p in parts if p)[:80]
    if game_slug:
        return f'{slugify(game_slug)}-{base}'[:80]
    return base


def column_exists(cur, table: str, column: str) -> bool:
    cur.execute(
        '''SELECT 1 FROM information_schema.COLUMNS
           WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s AND COLUMN_NAME=%s''',
        (DB_CONFIG['database'], table, column),
    )
    return cur.fetchone() is not None


def column_type(cur, table: str, column: str) -> str:
    cur.execute(
        '''SELECT COLUMN_TYPE FROM information_schema.COLUMNS
           WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s AND COLUMN_NAME=%s''',
        (DB_CONFIG['database'], table, column),
    )
    row = cur.fetchone()
    return (row.get('COLUMN_TYPE') or '').lower() if row else ''


def reset_table_autoincrement(cur, table: str) -> None:
    """Tras DELETE, MariaDB no baja AUTO_INCREMENT; el siguiente INSERT puede fallar."""
    if not re.match(r'^[a-zA-Z0-9_]+$', table):
        raise ValueError(f'Tabla inválida: {table}')
    cur.execute(f'SELECT COALESCE(MAX(id), 0) AS m FROM {table}')
    nxt = int(cur.fetchone()['m']) + 1
    cur.execute(f'ALTER TABLE {table} AUTO_INCREMENT = %s', (nxt,))


def dedupe_games_by_slug(cur, conn) -> int:
    """Fusiona filas duplicadas en games (misma slug) y reasigna trainers.game_id."""
    cur.execute('SELECT id, slug FROM games ORDER BY id')
    rows = cur.fetchall()
    keep_by_slug: dict[str, int] = {}
    removed = 0
    for row in rows:
        slug = (row.get('slug') or '').strip()
        gid = row['id']
        if not slug:
            continue
        if slug not in keep_by_slug:
            keep_by_slug[slug] = gid
            continue
        keep_id = keep_by_slug[slug]
        cur.execute('UPDATE trainers SET game_id=%s WHERE game_id=%s', (keep_id, gid))
        cur.execute('DELETE FROM games WHERE id=%s', (gid,))
        removed += 1
    if removed:
        conn.commit()
    return removed


def _trainers_game_fk_name(cur) -> str | None:
    cur.execute(
        '''SELECT CONSTRAINT_NAME FROM information_schema.KEY_COLUMN_USAGE
           WHERE TABLE_SCHEMA=%s AND TABLE_NAME='trainers'
             AND COLUMN_NAME='game_id' AND REFERENCED_TABLE_NAME='games'
           LIMIT 1''',
        (DB_CONFIG['database'],),
    )
    row = cur.fetchone()
    return row['CONSTRAINT_NAME'] if row else None


def ensure_games_schema(cur, conn) -> None:
    """games.id era TINYINT (máx. 255); importes repetidos agotaban AUTO_INCREMENT."""
    games_id_type = column_type(cur, 'games', 'id')
    if 'tinyint' in games_id_type:
        fk = _trainers_game_fk_name(cur)
        cur.execute('SET FOREIGN_KEY_CHECKS=0')
        if fk:
            cur.execute(f'ALTER TABLE trainers DROP FOREIGN KEY `{fk}`')
        cur.execute(
            'ALTER TABLE games MODIFY id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT'
        )
        cur.execute(
            'ALTER TABLE trainers MODIFY game_id SMALLINT UNSIGNED NOT NULL'
        )
        if fk:
            cur.execute(
                f'ALTER TABLE trainers ADD CONSTRAINT `{fk}` '
                'FOREIGN KEY (game_id) REFERENCES games(id)'
            )
        cur.execute('SET FOREIGN_KEY_CHECKS=1')
        conn.commit()
        print('[esquema] games.id ampliado a SMALLINT', end=' ', flush=True)

    removed = dedupe_games_by_slug(cur, conn)
    if removed:
        print(f'[esquema] {removed} juegos duplicados fusionados', end=' ', flush=True)

    reset_table_autoincrement(cur, 'games')
    conn.commit()


def ensure_schema(cur, conn) -> None:
    """Aplica cambios de sql/init.sql v2 en bases antiguas."""
    print('[esquema] Comprobando columnas...', end=' ', flush=True)

    if not column_exists(cur, 'games', 'slug'):
        cur.execute('ALTER TABLE games ADD COLUMN slug VARCHAR(40) NULL AFTER id')
        conn.commit()

    if column_exists(cur, 'games', 'slug'):
        cur.execute('SELECT id, name FROM games WHERE slug IS NULL OR slug = ""')
        for row in cur.fetchall():
            cur.execute(
                'UPDATE games SET slug=%s WHERE id=%s',
                (slugify(row['name']), row['id']),
            )
        conn.commit()
        try:
            cur.execute('ALTER TABLE games MODIFY slug VARCHAR(40) NOT NULL')
            cur.execute('ALTER TABLE games ADD UNIQUE KEY uq_games_slug (slug)')
        except pymysql.err.OperationalError:
            pass
        conn.commit()

    if column_exists(cur, 'trainers', 'trainer_class'):
        cur.execute(
            "SELECT COLUMN_TYPE FROM information_schema.COLUMNS "
            "WHERE TABLE_SCHEMA=%s AND TABLE_NAME='trainers' AND COLUMN_NAME='trainer_class'",
            (DB_CONFIG['database'],),
        )
        row = cur.fetchone()
        if row and 'enum' in (row.get('COLUMN_TYPE') or '').lower():
            cur.execute('ALTER TABLE trainers MODIFY trainer_class VARCHAR(20) NOT NULL')
            conn.commit()

    for col, ddl in (
        ('slug', 'ALTER TABLE trainers ADD COLUMN slug VARCHAR(80) NULL AFTER id'),
        ('specialty', 'ALTER TABLE trainers ADD COLUMN specialty VARCHAR(40) NULL'),
        ('location', 'ALTER TABLE trainers ADD COLUMN location VARCHAR(60) NULL'),
    ):
        if not column_exists(cur, 'trainers', col):
            cur.execute(ddl)
            conn.commit()

    if not column_exists(cur, 'trainers', 'team_by_starter'):
        cur.execute('ALTER TABLE trainers ADD COLUMN team_by_starter JSON NULL')
        conn.commit()

    if column_exists(cur, 'trainers', 'slug'):
        cur.execute('SELECT id, name, specialty, gym_order, trainer_class FROM trainers WHERE slug IS NULL OR slug = ""')
        for row in cur.fetchall():
            fake = {
                'name': row['name'],
                'specialty': row.get('specialty'),
                'order': row.get('gym_order'),
                'type': row.get('trainer_class'),
            }
            cur.execute('UPDATE trainers SET slug=%s WHERE id=%s', (trainer_slug(fake), row['id']))
        conn.commit()
        try:
            cur.execute('ALTER TABLE trainers ADD UNIQUE KEY uq_trainer_game_slug (game_id, slug)')
        except pymysql.err.OperationalError:
            pass
        conn.commit()

    ensure_games_schema(cur, conn)
    print('OK')


def wait_for_db(max_tries: int = 20) -> None:
    print(f'Conectando a MariaDB ({DB_CONFIG["host"]})...', end='', flush=True)
    for _ in range(max_tries):
        try:
            conn = pymysql.connect(**DB_CONFIG)
            conn.close()
            print(' OK')
            return
        except Exception:
            print('.', end='', flush=True)
            time.sleep(2)
    print('\nERROR: no se pudo conectar. Revisa DB_HOST, usuario y contraseña.')
    sys.exit(1)


def reset_tables(cur, conn, scope: str = 'all') -> None:
    if scope == 'pokemon':
        tables = RESET_POKEMON
        print('AVISO: --reset --only pokemon → se borran pokémon, movimientos y tipos.')
    elif scope == 'trainers':
        tables = RESET_TRAINERS
        print('AVISO: --reset --only trainers → NO se borra pokemon (solo entrenadores/juegos).')
    else:
        tables = RESET_ALL
        print('AVISO: --reset (import completo) → se borra TODA la base (pokémon + entrenadores).')
    print(f'Borrando datos ({scope})...')
    for table in tables:
        if not re.match(r'^[a-zA-Z0-9_]+$', table):
            raise ValueError(f'Tabla inválida: {table}')
        cur.execute(f'DELETE FROM {table}')
    for table in ('trainer_pokemon', 'trainers', 'games'):
        if table in tables:
            reset_table_autoincrement(cur, table)
    conn.commit()
    print('  Tablas vaciadas.')


def import_types_and_effectiveness(cur, conn) -> dict[str, int]:
    print('\n[tipos] Insertando...')
    for name_en, name_es in TIPOS_ES.items():
        cur.execute(
            'INSERT IGNORE INTO types (name_en, name_es) VALUES (%s,%s)',
            (name_en, name_es),
        )
    conn.commit()
    cur.execute('SELECT id, name_en FROM types')
    type_id_map = {r['name_en']: r['id'] for r in cur.fetchall()}

    rows = []
    for atk, defenses in EFF.items():
        aid = type_id_map.get(atk)
        if not aid:
            continue
        for deftype, mult in defenses.items():
            did = type_id_map.get(deftype)
            if did:
                rows.append((aid, did, int(mult * 100)))
    cur.executemany(
        '''INSERT INTO type_effectiveness (attack_type_id, defend_type_id, multiplier)
           VALUES (%s,%s,%s) ON DUPLICATE KEY UPDATE multiplier=VALUES(multiplier)''',
        rows,
    )
    conn.commit()
    print(f'  {len(type_id_map)} tipos, {len(rows)} efectividades')
    return type_id_map


def ensure_move(cur, conn, move_id_map: dict, type_id_map: dict,
                name: str, det: dict | None = None) -> int | None:
    if name in move_id_map:
        return move_id_map[name]
    det = det or {}
    tid = type_id_map.get(det.get('type', 'normal'), type_id_map['normal'])
    cat = det.get('category', 'status')
    if cat not in ('physical', 'special', 'status'):
        cat = 'status'
    name_es = det.get('name_es') or name.replace('-', ' ').title()
    cur.execute(
        '''INSERT IGNORE INTO moves (name, name_es, type_id, category, power, accuracy, pp)
           VALUES (%s,%s,%s,%s,%s,%s,%s)''',
        (name, name_es, tid, cat, det.get('power'), det.get('accuracy'), det.get('pp')),
    )
    conn.commit()
    cur.execute('SELECT id FROM moves WHERE name=%s', (name,))
    row = cur.fetchone()
    if row:
        move_id_map[name] = row['id']
        return row['id']
    return None


def import_moves(cur, conn, moves_data: dict, type_id_map: dict) -> dict[str, int]:
    print('[movimientos] Insertando...', end=' ', flush=True)
    move_rows = []
    for name, det in moves_data.items():
        tid = type_id_map.get(det.get('type', 'normal'), type_id_map['normal'])
        cat = det.get('category', 'status')
        if cat not in ('physical', 'special', 'status'):
            cat = 'status'
        name_es = det.get('name_es') or name.replace('-', ' ').title()
        move_rows.append((
            name, name_es, tid, cat,
            det.get('power'), det.get('accuracy'), det.get('pp'),
        ))
    for i in range(0, len(move_rows), 500):
        cur.executemany(
            '''INSERT IGNORE INTO moves (name, name_es, type_id, category, power, accuracy, pp)
               VALUES (%s,%s,%s,%s,%s,%s,%s)''',
            move_rows[i:i + 500],
        )
    conn.commit()
    cur.execute('SELECT id, name FROM moves')
    move_id_map = {r['name']: r['id'] for r in cur.fetchall()}
    print(f'{len(move_id_map)} movimientos')
    return move_id_map


def import_pokemon(cur, conn, pokemon_data: dict, type_id_map: dict,
                   move_id_map: dict, moves_data: dict) -> dict[str, int]:
    print('[pokemon] Insertando...')
    total = len(pokemon_data)
    done = 0
    name_to_id: dict[str, int] = {}

    for name, pdata in sorted(pokemon_data.items(), key=lambda x: x[1]['id']):
        pid = pdata['id']
        name_to_id[name] = pid
        name_es = pdata.get('name_es') or name.replace('-', ' ').title()
        sprite = pdata.get('sprite') or pdata.get('sprites', {}).get('official_artwork', '')

        raw_stats = pdata.get('stats')
        if isinstance(raw_stats, list):
            stats_map = {s['stat']['name']: s['base_stat'] for s in raw_stats}
            hp = stats_map.get('hp', 0)
            attack = stats_map.get('attack', 0)
            defense = stats_map.get('defense', 0)
            sp_attack = stats_map.get('special-attack', 0)
            sp_defense = stats_map.get('special-defense', 0)
            speed = stats_map.get('speed', 0)
        else:
            hp = pdata.get('hp', 0)
            attack = pdata.get('attack', 0)
            defense = pdata.get('defense', 0)
            sp_attack = pdata.get('sp_attack', pdata.get('special_attack', pdata.get('spatk', 0)))
            sp_defense = pdata.get('sp_defense', pdata.get('special_defense', pdata.get('spdef', 0)))
            speed = pdata.get('speed', 0)

        is_legendary = int(bool(
            pdata.get('is_legendary') or pdata.get('isLegendary')
            or pdata.get('legendary')
            or pdata.get('species', {}).get('is_legendary', False)
        ))
        evo_fam = pid if pid in EVO_FAMILY_IDS else None

        cur.execute(
            '''INSERT INTO pokemon
               (id, name, name_es, sprite_url, hp, attack, defense,
                sp_attack, sp_defense, speed, is_legendary, evo_family_id)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
               ON DUPLICATE KEY UPDATE
                 name_es=VALUES(name_es), sprite_url=VALUES(sprite_url),
                 hp=VALUES(hp), attack=VALUES(attack), defense=VALUES(defense),
                 sp_attack=VALUES(sp_attack), sp_defense=VALUES(sp_defense),
                 speed=VALUES(speed), is_legendary=VALUES(is_legendary),
                 evo_family_id=VALUES(evo_family_id)''',
            (pid, name, name_es, sprite,
             hp, attack, defense, sp_attack, sp_defense, speed,
             is_legendary, evo_fam),
        )

        for slot, type_en in enumerate(pdata.get('types', []), 1):
            tid = type_id_map.get(type_en)
            if tid:
                cur.execute(
                    'INSERT IGNORE INTO pokemon_types (pokemon_id,type_id,slot) VALUES(%s,%s,%s)',
                    (pid, tid, slot),
                )

        pm_rows = []
        for m in pdata.get('moves', []):
            mid = move_id_map.get(m['name'])
            if not mid:
                det = m.get('detail') or moves_data.get(m['name'])
                mid = ensure_move(cur, conn, move_id_map, type_id_map, m['name'], det)
            if not mid:
                continue
            method = 'level-up' if m.get('byLevel') else 'machine'
            lvl = m.get('level') or None
            if lvl == 0:
                lvl = None
            pm_rows.append((pid, mid, method, lvl))

        if pm_rows:
            cur.executemany(
                '''INSERT IGNORE INTO pokemon_moves (pokemon_id,move_id,learn_method,level)
                   VALUES(%s,%s,%s,%s)''',
                pm_rows,
            )

        done += 1
        if done % 100 == 0 or done == total:
            conn.commit()
            print(f'\r  {done}/{total} ({done * 100 // total}%)  ', end='', flush=True)

    conn.commit()
    print()
    return name_to_id


def normalize_move_slug(name: str) -> str:
    key = name.lower().replace(' ', '').replace('_', '-')
    return MOVE_SLUG_ALIASES.get(key, MOVE_SLUG_ALIASES.get(name, name))


def resolve_pokemon_id(name: str, name_to_id: dict[str, int]) -> int | None:
    key = POKEMON_ALIASES.get(name, name)
    return name_to_id.get(key)


def clear_trainer_team(cur, trainer_id: int) -> None:
    """Vacía el equipo de un entrenador (mantiene la fila en trainers)."""
    cur.execute(
        'DELETE FROM trainer_pokemon_moves WHERE trainer_pokemon_id IN '
        '(SELECT id FROM trainer_pokemon WHERE trainer_id=%s)',
        (trainer_id,),
    )
    cur.execute('DELETE FROM trainer_pokemon WHERE trainer_id=%s', (trainer_id,))


def delete_trainer_row(cur, trainer_id: int) -> None:
    """Borra un entrenador y su equipo (sin CASCADE en el esquema)."""
    clear_trainer_team(cur, trainer_id)
    cur.execute('DELETE FROM trainers WHERE id=%s', (trainer_id,))


def import_trainers(cur, conn, trainers_db: dict, name_to_id: dict[str, int],
                    move_id_map: dict, type_id_map: dict, moves_data: dict) -> None:
    print('[entrenadores] Insertando juegos y equipos...')
    ensure_games_schema(cur, conn)
    games_meta = {g['slug']: g for g in trainers_db.get('games', [])}
    game_id_by_slug: dict[str, int] = {}

    for slug, meta in games_meta.items():
        cur.execute(
            '''INSERT INTO games (slug, name, region, gen)
               VALUES (%s,%s,%s,%s)
               ON DUPLICATE KEY UPDATE name=VALUES(name), region=VALUES(region), gen=VALUES(gen)''',
            (slug, meta['name'], meta.get('region', ''), meta.get('gen', 0)),
        )
    conn.commit()
    cur.execute('SELECT id, slug FROM games')
    for row in cur.fetchall():
        game_id_by_slug[row['slug']] = row['id']

    missing_mons: set[str] = set()
    missing_moves: set[str] = set()
    trainers_imported = 0

    for game_slug, trainer_list in trainers_db.get('trainers', {}).items():
        game_id = game_id_by_slug.get(game_slug)
        if not game_id:
            print(f'  AVISO: juego sin meta: {game_slug}')
            continue

        new_slugs: list[str] = []

        for tr in trainer_list:
            tslug = trainer_slug(tr, game_slug)
            new_slugs.append(tslug)
            tclass = tr.get('type') or 'other'
            name = tr.get('name', '')
            name_es = name
            order = tr.get('order')
            badge = (tr.get('badge') or '').strip() or None
            specialty = tr.get('specialty') or None
            location = tr.get('location') or None
            sprite = tr.get('sprite')
            tbs = dict(tr.get('teamByStarter') or {})
            tbe = tr.get('teamByEeveelution') or {}
            if tbe:
                tbs.update(tbe)
            tbs_json = json.dumps(tbs, ensure_ascii=False) if tbs else None

            cur.execute(
                '''INSERT INTO trainers
                   (slug, name, name_es, trainer_class, game_id, gym_order,
                    badge_name, specialty, location, sprite_url, team_by_starter)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                   ON DUPLICATE KEY UPDATE
                     name=VALUES(name), name_es=VALUES(name_es),
                     trainer_class=VALUES(trainer_class), gym_order=VALUES(gym_order),
                     badge_name=VALUES(badge_name), specialty=VALUES(specialty),
                     location=VALUES(location), sprite_url=VALUES(sprite_url),
                     team_by_starter=VALUES(team_by_starter)''',
                (tslug, name, name_es, tclass, game_id, order,
                 badge, specialty, location, sprite, tbs_json),
            )
            cur.execute(
                'SELECT id FROM trainers WHERE game_id=%s AND slug=%s',
                (game_id, tslug),
            )
            row = cur.fetchone()
            if not row:
                continue
            trainer_id = row['id']

            clear_trainer_team(cur, trainer_id)

            for slot, mon in enumerate(tr.get('team') or [], 1):
                pname = mon.get('name', '')
                pid = resolve_pokemon_id(pname, name_to_id)
                if not pid:
                    missing_mons.add(pname)
                    continue
                level = mon.get('level') or 50
                cur.execute(
                    '''INSERT INTO trainer_pokemon (trainer_id, pokemon_id, level, slot)
                       VALUES (%s,%s,%s,%s)''',
                    (trainer_id, pid, level, slot),
                )
                tp_id = cur.lastrowid

                for mslot, mv in enumerate(mon.get('moves') or [], 1):
                    mname = normalize_move_slug(mv.get('name') or '')
                    if not mname:
                        continue
                    mid = move_id_map.get(mname)
                    if not mid:
                        det = moves_data.get(mname, {})
                        if not det and mv.get('name_display'):
                            det = {'name_es': mv['name_display']}
                        mid = ensure_move(cur, conn, move_id_map, type_id_map, mname, det)
                    if not mid:
                        missing_moves.add(mname)
                        continue
                    cur.execute(
                        '''INSERT INTO trainer_pokemon_moves (trainer_pokemon_id, move_id, slot)
                           VALUES (%s,%s,%s)
                           ON DUPLICATE KEY UPDATE move_id=VALUES(move_id)''',
                        (tp_id, mid, mslot),
                    )

            trainers_imported += 1

        # Filas antiguas (p. ej. slug sin prefijo de juego tras cambiar trainer_slug)
        cur.execute('SELECT id, slug FROM trainers WHERE game_id=%s', (game_id,))
        keep = set(new_slugs)
        removed = 0
        for row in cur.fetchall():
            if row['slug'] not in keep:
                delete_trainer_row(cur, row['id'])
                removed += 1
        if removed:
            print(f'  {game_slug}: eliminados {removed} entrenadores obsoletos')

        conn.commit()

    print(f'  {trainers_imported} entrenadores importados')
    if missing_mons:
        print(f'  AVISO: {len(missing_mons)} especies sin pokédex: {sorted(missing_mons)[:12]}...')
    if missing_moves:
        print(f'  AVISO: {len(missing_moves)} movimientos no resueltos: {sorted(missing_moves)[:12]}...')


def print_stats(cur) -> None:
    def count(table: str) -> int:
        if not re.match(r'^[a-zA-Z0-9_]+$', table):
            raise ValueError('tabla inválida')
        cur.execute(f'SELECT COUNT(*) AS n FROM {table}')
        return cur.fetchone()['n']

    print('\n=== Resumen en MariaDB ===')
    for t in ('types', 'pokemon', 'moves', 'pokemon_moves', 'games', 'trainers',
              'trainer_pokemon', 'trainer_pokemon_moves'):
        print(f'  {t:24} {count(t)}')


def main() -> None:
    parser = argparse.ArgumentParser(description='Importar Pokeweb JSON → MariaDB')
    parser.add_argument('--reset', action='store_true', help='Vaciar tablas antes de importar')
    parser.add_argument('--only', choices=('pokemon', 'trainers', 'all'), default='all')
    args = parser.parse_args()

    poke_path = pokemon_json_path()
    train_path = trainers_json_path()

    if args.only in ('pokemon', 'all') and not poke_path:
        print('ERROR: no encuentro pokemon_db.json en api/ ni data/')
        sys.exit(1)
    if args.only in ('trainers', 'all') and not train_path:
        print('ERROR: no encuentro trainers_db.json en api/ ni data/')
        sys.exit(1)

    wait_for_db()
    conn = pymysql.connect(**DB_CONFIG)
    cur = conn.cursor()
    ensure_schema(cur, conn)

    if args.reset:
        reset_tables(cur, conn, scope=args.only)

    pokemon_data = {}
    moves_data = {}
    trainers_db = {}
    name_to_id: dict[str, int] = {}

    if args.only in ('pokemon', 'all'):
        print(f'Leyendo {poke_path}...')
        with open(poke_path, encoding='utf-8') as f:
            db_json = json.load(f)
        pokemon_data = db_json.get('pokemon', {})
        moves_data = db_json.get('moves', {})
        print(f'  {len(pokemon_data)} pokémon, {len(moves_data)} movimientos')

        type_id_map = import_types_and_effectiveness(cur, conn)
        move_id_map = import_moves(cur, conn, moves_data, type_id_map)
        name_to_id = import_pokemon(cur, conn, pokemon_data, type_id_map, move_id_map, moves_data)

    if args.only in ('trainers', 'all'):
        if not name_to_id:
            cur.execute('SELECT id, name FROM pokemon')
            name_to_id = {r['name']: r['id'] for r in cur.fetchall()}
        cur.execute('SELECT id, name FROM moves')
        move_id_map = {r['name']: r['id'] for r in cur.fetchall()}
        cur.execute('SELECT id, name_en FROM types')
        type_id_map = {r['name_en']: r['id'] for r in cur.fetchall()}

        print(f'Leyendo {train_path}...')
        with open(train_path, encoding='utf-8') as f:
            trainers_db = json.load(f)
        if poke_path and not moves_data:
            with open(poke_path, encoding='utf-8') as f:
                moves_data = json.load(f).get('moves', {})

        import_trainers(cur, conn, trainers_db, name_to_id, move_id_map, type_id_map, moves_data)

    print_stats(cur)

    cur.execute('SELECT COUNT(*) AS n FROM pokemon')
    n_poke = cur.fetchone()['n']
    if args.only in ('pokemon', 'all') and n_poke == 0:
        print('\nERROR: tabla pokemon vacía tras el import. Revisa pokemon_db.json y vuelve a ejecutar:')
        print('  python import_db.py --only pokemon --reset')
        sys.exit(1)
    if args.only in ('trainers', 'all') and n_poke == 0:
        print('\nAVISO: hay 0 pokémon en MariaDB. Importa primero:')
        print('  python import_db.py --only pokemon --reset')

    print('\nPrueba: http://127.0.0.1:5000/health')
    print('        http://127.0.0.1:5000/stats')
    print('        http://127.0.0.1:5000/trainers?game_slug=red-blue')

    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
