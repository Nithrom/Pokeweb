"""
Crea tablas en Supabase ejecutando sql/init.postgres.sql.
Uso (api/.env con DATABASE_URL):
  python setup_supabase_schema.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import db

ROOT = Path(__file__).resolve().parent.parent
SQL_PATH = ROOT / 'sql' / 'init.postgres.sql'


def main() -> None:
    if not db.is_postgres():
        print('ERROR: define DATABASE_URL en api/.env (PostgreSQL / Supabase).')
        sys.exit(1)
    if not SQL_PATH.is_file():
        print(f'ERROR: no existe {SQL_PATH}')
        sys.exit(1)

    sql = SQL_PATH.read_text(encoding='utf-8')
    conn = db.connect()
    try:
        with db.cursor(conn) as cur:
            cur.execute(sql)
        conn.commit()
        print(f'OK: esquema aplicado desde {SQL_PATH.name}')
    finally:
        conn.close()


if __name__ == '__main__':
    main()
