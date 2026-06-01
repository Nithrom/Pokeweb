"""
Pokeweb API — Flask + MariaDB o PostgreSQL (Supabase)
Endpoints:
  GET  /health, /stats
  GET  /pokemon, /pokemon/<name>, /pokemon/<name>/moves
  GET  /type/<name>, /type/<t1>/<t2>, /effectiveness
  GET  /games
  GET  /trainers?game_id=1 | ?game_slug=red-blue
  GET  /trainer/<id>
  GET  /trainers/<game_slug>/<trainer_slug>   — equipo completo (como trainers_db.json)
  POST /teams, GET/DELETE /teams/<id>
"""
import json as _json
import os
import re

from flask import Flask, jsonify, request
from flask_cors import CORS

import db
from move_gen_types import resolve_move_type

app = Flask(__name__)
CORS(app)

query = db.query
query_one = db.query_one
execute = db.execute


def jsonify_cached(data, max_age: int):
    resp = jsonify(data)
    resp.headers['Cache-Control'] = f'public, max-age={max_age}'
    return resp


def split_types(row, key_en='types_en', key_es='types_es'):
    if key_en in row and row[key_en]:
        row[key_en] = row[key_en].split(',')
    if key_es in row and row.get(key_es):
        row[key_es] = row[key_es].split(',')
    return row


def trainer_team_rows(trainer_id: int, game_gen: int = 0) -> list:
    rows = query(f"""
        SELECT tp.id, tp.slot, tp.level,
               p.id AS pokemon_id, p.name, p.name_es, p.sprite_url,
               pt_agg.types_en, pt_agg.types_es,
               m.name AS move_name, m.name_es AS move_name_es,
               t.name_en AS move_type_en, t.name_es AS move_type_es,
               m.category AS move_category, m.power AS move_power,
               m.accuracy AS move_accuracy, m.pp AS move_pp,
               tpm.slot AS move_slot
        FROM trainer_pokemon tp
        JOIN pokemon p ON p.id = tp.pokemon_id
        {db.types_agg_join()}
        LEFT JOIN trainer_pokemon_moves tpm ON tpm.trainer_pokemon_id = tp.id
        LEFT JOIN moves m ON m.id = tpm.move_id
        LEFT JOIN types t ON t.id = m.type_id
        WHERE tp.trainer_id = %s
        ORDER BY tp.slot, tpm.slot
    """, (trainer_id,))
    team: list[dict] = []
    by_tp_id: dict[int, dict] = {}
    for row in rows:
        tp_id = row['id']
        if tp_id not in by_tp_id:
            member = {
                'id': tp_id,
                'slot': row['slot'],
                'level': row['level'],
                'pokemon_id': row['pokemon_id'],
                'name': row['name'],
                'name_es': row['name_es'],
                'sprite_url': row['sprite_url'],
                'types_en': row['types_en'],
                'types_es': row['types_es'],
                'moves': [],
            }
            by_tp_id[tp_id] = member
            team.append(member)
        if row.get('move_name'):
            by_tp_id[tp_id]['moves'].append({
                'name': row['move_name'],
                'name_es': row['move_name_es'],
                'type_en': resolve_move_type(
                    row['move_name'], game_gen, row.get('move_type_en') or 'normal',
                ),
                'type_es': row.get('move_type_es'),
                'category': row['move_category'],
                'power': row['move_power'],
                'accuracy': row['move_accuracy'],
                'pp': row['move_pp'],
            })
    for member in team:
        split_types(member)
        del member['id']
    return team


def _parse_team_by_starter(raw) -> dict | None:
    if not raw:
        return None
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        try:
            return _json.loads(raw)
        except _json.JSONDecodeError:
            return None
    return None


DUAL_REGION_GYM_GAMES = frozenset({'gold-silver', 'crystal', 'heartgold-soulsilver'})
KANTO_GYM_ORDER_MIN = 9


def gym_leader_region(tr: dict) -> str | None:
    if tr.get('trainer_class') != 'gym':
        return None
    slug = tr.get('game_slug') or ''
    if slug not in DUAL_REGION_GYM_GAMES:
        return None
    order = tr.get('gym_order') or 0
    if order >= KANTO_GYM_ORDER_MIN:
        return 'kanto'
    if order >= 1:
        return 'johto'
    return None


def trainer_to_json(tr: dict, include_team: bool = False) -> dict:
    region = gym_leader_region(tr)
    out = {
        'id': tr['id'],
        'slug': tr.get('slug'),
        'name': tr['name'],
        'name_es': tr.get('name_es') or tr['name'],
        'type': tr.get('trainer_class'),
        'order': tr.get('gym_order'),
        'location': tr.get('location') or '',
        'badge': tr.get('badge_name') or '',
        'specialty': tr.get('specialty') or '',
        'sprite': tr.get('sprite_url'),
        'game_id': tr.get('game_id'),
        'game_slug': tr.get('game_slug'),
    }
    if region:
        out['region'] = region
    tbs = _parse_team_by_starter(tr.get('team_by_starter'))
    if tbs:
        out['teamByStarter'] = tbs
    if include_team:
        game_gen = int(tr.get('game_gen') or tr.get('gen') or 0)
        out['team'] = trainer_team_rows(tr['id'], game_gen)
    return out


# ── Meta ──────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return jsonify({
        'status': 'API online',
        'endpoints': [
            '/health', '/stats', '/games', '/pokemon', '/trainers',
            '/trainers/<game_slug>/<trainer_slug>',
        ],
    })


@app.route('/health')
def health():
    hint = db.missing_database_config_hint()
    if hint:
        return jsonify({
            'status': 'error',
            'db': 'not_configured',
            'detail': hint,
            'backend': db.get_backend(),
        }), 500
    try:
        query_one('SELECT 1')
        return jsonify({'status': 'ok', 'db': 'connected', 'backend': db.get_backend(), 'label': db.db_label()})
    except Exception as e:
        return jsonify({
            'status': 'error',
            'db': 'connection_failed',
            'detail': str(e),
            'backend': db.get_backend(),
            'label': db.db_label(),
        }), 500


@app.route('/stats')
def stats():
    try:
        tables = (
            'pokemon', 'moves', 'pokemon_moves', 'games', 'trainers',
            'trainer_pokemon', 'trainer_pokemon_moves',
        )
        counts = {}
        for t in tables:
            if not re.match(r'^[a-zA-Z0-9_]+$', t):
                continue
            counts[t] = query_one(f'SELECT COUNT(*) AS n FROM {t}')['n']
        return jsonify(counts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── Pokémon ───────────────────────────────────────────────────────────────────
@app.route('/pokemon')
def list_pokemon():
    rows = query(f"""
        SELECT p.id, p.name, p.name_es, p.sprite_url,
               {db.group_concat('t.name_en', 'pt.slot')} AS types_en,
               {db.group_concat('t.name_es', 'pt.slot')} AS types_es
        FROM pokemon p
        JOIN pokemon_types pt ON pt.pokemon_id = p.id
        JOIN types t ON t.id = pt.type_id
        GROUP BY p.id
        ORDER BY p.id
    """)
    return jsonify([split_types(r) for r in rows])


@app.route('/pokemon/<name>')
def get_pokemon(name):
    p = query_one(f"""
        SELECT p.*, {db.group_concat('t.name_en', 'pt.slot')} AS types_en,
               {db.group_concat('t.name_es', 'pt.slot')} AS types_es
        FROM pokemon p
        JOIN pokemon_types pt ON pt.pokemon_id = p.id
        JOIN types t ON t.id = pt.type_id
        WHERE p.name = %s
        GROUP BY p.id
    """, (name,))
    if not p:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(split_types(p))


@app.route('/pokemon/<name>/moves')
def get_pokemon_moves(name):
    rows = query("""
        SELECT m.name, m.name_es, t.name_en AS type_en, t.name_es AS type_es,
               m.category, m.power, m.accuracy, m.pp,
               pm.learn_method, pm.level
        FROM pokemon_moves pm
        JOIN pokemon p  ON p.id  = pm.pokemon_id
        JOIN moves m    ON m.id  = pm.move_id
        JOIN types t    ON t.id  = m.type_id
        WHERE p.name = %s
        ORDER BY pm.learn_method, pm.level, m.name
    """, (name,))
    return jsonify(rows)


# ── Tipos ─────────────────────────────────────────────────────────────────────
@app.route('/type/<type_name>')
def pokemon_by_type(type_name):
    rows = query(f"""
        SELECT p.id, p.name, p.name_es, p.sprite_url,
               {db.group_concat('t2.name_en', 'pt2.slot')} AS types_en,
               {db.group_concat('t2.name_es', 'pt2.slot')} AS types_es
        FROM pokemon p
        JOIN pokemon_types pt  ON pt.pokemon_id  = p.id
        JOIN types t           ON t.id           = pt.type_id  AND t.name_en = %s
        JOIN pokemon_types pt2 ON pt2.pokemon_id = p.id
        JOIN types t2          ON t2.id          = pt2.type_id
        WHERE p.evo_family_id = p.id OR p.evo_family_id IS NULL
        GROUP BY p.id
        ORDER BY p.id
    """, (type_name,))
    return jsonify([split_types(r) for r in rows])


@app.route('/type/<t1>/<t2>')
def pokemon_by_dual_type(t1, t2):
    rows = query(f"""
        SELECT p.id, p.name, p.name_es, p.sprite_url,
               {db.group_concat('t.name_en', 'pt.slot')} AS types_en
        FROM pokemon p
        JOIN pokemon_types pt1 ON pt1.pokemon_id = p.id
        JOIN types ty1 ON ty1.id = pt1.type_id AND ty1.name_en = %s
        JOIN pokemon_types pt2 ON pt2.pokemon_id = p.id
        JOIN types ty2 ON ty2.id = pt2.type_id AND ty2.name_en = %s
        JOIN pokemon_types pt ON pt.pokemon_id = p.id
        JOIN types t ON t.id = pt.type_id
        GROUP BY p.id ORDER BY p.id
    """, (t1, t2))
    for r in rows:
        split_types(r)
    return jsonify(rows)


@app.route('/effectiveness')
def effectiveness():
    rows = query("""
        SELECT ta.name_en AS attack, td.name_en AS defend, e.multiplier
        FROM type_effectiveness e
        JOIN types ta ON ta.id = e.attack_type_id
        JOIN types td ON td.id = e.defend_type_id
    """)
    return jsonify(rows)


# ── Juegos y entrenadores ───────────────────────────────────────────────────────
@app.route('/games')
def list_games():
    return jsonify_cached(
        query('SELECT id, slug, name, region, gen FROM games ORDER BY gen, id'),
        max_age=3600,
    )


TRAINER_LIST_ORDER = """
    ORDER BY
      CASE tr.trainer_class
        WHEN 'gym' THEN 0
        WHEN 'kahuna' THEN 0
        WHEN 'elite4' THEN 1
        WHEN 'champion' THEN 2
        WHEN 'captain' THEN 3
        ELSE 4
      END,
      tr.gym_order,
      tr.id
"""


@app.route('/trainers')
def list_trainers():
    game_id = request.args.get('game_id')
    game_slug = request.args.get('game_slug')
    include_team = request.args.get('include_team') in ('1', 'true', 'yes')
    if game_slug:
        rows = query(f"""
            SELECT tr.*, g.slug AS game_slug, g.gen AS game_gen
            FROM trainers tr
            JOIN games g ON g.id = tr.game_id
            WHERE g.slug = %s
            {TRAINER_LIST_ORDER}
        """, (game_slug,))
    elif game_id:
        rows = query(f"""
            SELECT tr.*, g.slug AS game_slug, g.gen AS game_gen
            FROM trainers tr
            JOIN games g ON g.id = tr.game_id
            WHERE tr.game_id = %s
            {TRAINER_LIST_ORDER}
        """, (game_id,))
    else:
        rows = query(f"""
            SELECT tr.*, g.slug AS game_slug, g.gen AS game_gen
            FROM trainers tr
            JOIN games g ON g.id = tr.game_id
            ORDER BY g.gen, g.id,
              CASE tr.trainer_class
                WHEN 'gym' THEN 0
                WHEN 'kahuna' THEN 0
                WHEN 'elite4' THEN 1
                WHEN 'champion' THEN 2
                WHEN 'captain' THEN 3
                ELSE 4
              END,
              tr.gym_order,
              tr.id
        """)
    out = [trainer_to_json(r, include_team=include_team) for r in rows]
    if (game_slug or game_id) and not include_team:
        return jsonify_cached(out, max_age=300)
    return jsonify(out)


@app.route('/db/pokemon')
def db_pokemon():
    """Exporta {pokemon, moves} como pokemon_db.json (para teams.js / app.js)."""
    type_rows = query('SELECT id, name_en FROM types')
    type_en = {r['id']: r['name_en'] for r in type_rows}

    moves_out = {}
    for m in query('SELECT name, name_es, type_id, category, power, accuracy, pp FROM moves'):
        moves_out[m['name']] = {
            'name_es': m['name_es'],
            'type': type_en.get(m['type_id'], 'normal'),
            'category': m['category'],
            'power': m['power'],
            'pp': m['pp'],
            'accuracy': m['accuracy'],
            'priority': 0,
        }

    pokemon_out = {}
    for p in query(f"""
        SELECT p.id, p.name, p.name_es, p.sprite_url, p.hp, p.attack, p.defense,
               p.sp_attack, p.sp_defense, p.speed, p.is_legendary,
               {db.group_concat('t.name_en', 'pt.slot')} AS types_en
        FROM pokemon p
        LEFT JOIN pokemon_types pt ON pt.pokemon_id = p.id
        LEFT JOIN types t ON t.id = pt.type_id
        GROUP BY p.id
        ORDER BY p.id
    """):
        types_list = p['types_en'].split(',') if p.get('types_en') else []
        pokemon_out[p['name']] = {
            'id': p['id'],
            'name_es': p['name_es'],
            'types': types_list,
            'sprite': p['sprite_url'] or '',
            'hp': p['hp'],
            'attack': p['attack'],
            'defense': p['defense'],
            'sp_attack': p['sp_attack'],
            'sp_defense': p['sp_defense'],
            'speed': p['speed'],
            'is_legendary': bool(p['is_legendary']),
            'moves': [],
            'evolves_from': None,
        }

    learn_rows = query("""
        SELECT p.name AS pokemon_name, m.name AS move_name,
               pm.learn_method, pm.level,
               m.name_es, m.type_id, m.category, m.power, m.accuracy, m.pp
        FROM pokemon_moves pm
        JOIN pokemon p ON p.id = pm.pokemon_id
        JOIN moves m ON m.id = pm.move_id
        ORDER BY p.id, pm.learn_method, pm.level, m.name
    """)
    for row in learn_rows:
        poke = pokemon_out.get(row['pokemon_name'])
        if not poke:
            continue
        # Sin duplicar detail por movimiento (el cliente usa DB.moves[name])
        poke['moves'].append({
            'name': row['move_name'],
            'byLevel': row['learn_method'] == 'level-up',
            'level': row['level'] or 0,
        })

    return jsonify({'pokemon': pokemon_out, 'moves': moves_out})


@app.route('/trainer/<int:trainer_id>')
def get_trainer(trainer_id):
    tr = query_one("""
        SELECT tr.*, g.slug AS game_slug, g.gen AS game_gen
        FROM trainers tr
        JOIN games g ON g.id = tr.game_id
        WHERE tr.id = %s
    """, (trainer_id,))
    if not tr:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(trainer_to_json(tr, include_team=True))


@app.route('/trainers/<game_slug>/<trainer_slug>')
def get_trainer_by_slug(game_slug, trainer_slug):
    tr = query_one("""
        SELECT tr.*, g.slug AS game_slug, g.gen AS game_gen
        FROM trainers tr
        JOIN games g ON g.id = tr.game_id
        WHERE g.slug = %s AND tr.slug = %s
    """, (game_slug, trainer_slug))
    if not tr:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(trainer_to_json(tr, include_team=True))


@app.route('/trainers/<game_slug>')
def list_trainers_for_game(game_slug):
    """Todos los entrenadores de un juego con equipo (payload grande)."""
    rows = query("""
        SELECT tr.*, g.slug AS game_slug, g.gen AS game_gen
        FROM trainers tr
        JOIN games g ON g.id = tr.game_id
        WHERE g.slug = %s
        ORDER BY tr.gym_order, tr.id
    """, (game_slug,))
    return jsonify([trainer_to_json(r, include_team=True) for r in rows])


# ── Equipos de usuario ────────────────────────────────────────────────────────
@app.route('/teams', methods=['POST'])
def create_team():
    data = request.json or {}
    name = data.get('name', 'Mi equipo')
    conn = db.connect()
    try:
        with db.cursor(conn) as cur:
            team_id = db.insert_returning_id(
                cur, 'INSERT INTO user_teams (name) VALUES (%s)', (name,),
            )
            for slot, member in enumerate(data.get('pokemon', []), 1):
                tp_id = db.insert_returning_id(
                    cur,
                    'INSERT INTO user_team_pokemon (team_id, pokemon_id, slot) VALUES (%s,%s,%s)',
                    (team_id, member['pokemon_id'], slot),
                )
                for mslot, move_id in enumerate(member.get('move_ids', []), 1):
                    cur.execute(
                        'INSERT INTO user_team_pokemon_moves (team_pokemon_id, move_id, slot) VALUES (%s,%s,%s)',
                        (tp_id, move_id, mslot),
                    )
            conn.commit()
    finally:
        db.release_conn(conn)
    return jsonify({'id': team_id}), 201


@app.route('/teams/<int:team_id>')
def get_team(team_id):
    team = query_one('SELECT * FROM user_teams WHERE id=%s', (team_id,))
    if not team:
        return jsonify({'error': 'Not found'}), 404
    members = query(f"""
        SELECT utp.id, utp.slot, p.name, p.name_es, p.sprite_url,
               pt_agg.types_en
        FROM user_team_pokemon utp
        JOIN pokemon p ON p.id = utp.pokemon_id
        {db.types_agg_join()}
        WHERE utp.team_id = %s
        ORDER BY utp.slot
    """, (team_id,))
    for m in members:
        split_types(m)
        m['moves'] = query("""
            SELECT mv.name, mv.name_es, t.name_en AS type_en,
                   mv.category, mv.power, mv.accuracy
            FROM user_team_pokemon_moves utm
            JOIN moves mv ON mv.id = utm.move_id
            JOIN types t ON t.id = mv.type_id
            WHERE utm.team_pokemon_id = %s ORDER BY utm.slot
        """, (m['id'],))
        del m['id']
    team['members'] = members
    return jsonify(team)


@app.route('/teams/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    execute('DELETE FROM user_teams WHERE id=%s', (team_id,))
    return jsonify({'ok': True})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.environ.get('FLASK_DEBUG') == '1')
