"""
Pokeweb API — Flask + MariaDB
Endpoints disponibles:
  GET  /pokemon              → lista todos los pokémon
  GET  /pokemon/<name>       → datos completos de un pokémon
  GET  /pokemon/<name>/moves → movimientos de un pokémon
  GET  /type/<name>          → pokémon de ese tipo
  GET  /type/<t1>/<t2>       → pokémon de doble tipo
  GET  /effectiveness        → tabla completa de efectividades
  GET  /games                → lista de juegos/versiones
  GET  /trainers?game_id=X   → entrenadores de un juego
  GET  /trainer/<id>         → equipo completo de un entrenador

  POST /teams                → crear equipo de usuario
  GET  /teams/<id>           → obtener equipo
  PUT  /teams/<id>           → actualizar equipo
  DEL  /teams/<id>           → borrar equipo
"""

import os
import pymysql
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # permite llamadas desde el frontend en localhost

# ── Conexión ──────────────────────────────────────
def get_db():
    return pymysql.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        port=int(os.environ.get('DB_PORT', 3306)),
        user=os.environ.get('DB_USER', 'pokeweb_user'),
        password=os.environ.get('DB_PASS', 'pokeweb_pass'),
        database=os.environ.get('DB_NAME', 'pokeweb'),
        cursorclass=pymysql.cursors.DictCursor,
        charset='utf8mb4'
    )

def query(sql, params=None):
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute(sql, params or ())
            return cur.fetchall()
    finally:
        db.close()

def query_one(sql, params=None):
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute(sql, params or ())
            return cur.fetchone()
    finally:
        db.close()

def execute(sql, params=None):
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute(sql, params or ())
            db.commit()
            return cur.lastrowid
    finally:
        db.close()

# ── Pokémon ───────────────────────────────────────
@app.route('/pokemon')
def list_pokemon():
    rows = query("""
        SELECT p.id, p.name, p.name_es, p.sprite_url,
               GROUP_CONCAT(t.name_en ORDER BY pt.slot) AS types_en,
               GROUP_CONCAT(t.name_es ORDER BY pt.slot) AS types_es
        FROM pokemon p
        JOIN pokemon_types pt ON pt.pokemon_id = p.id
        JOIN types t ON t.id = pt.type_id
        GROUP BY p.id
        ORDER BY p.id
    """)
    for r in rows:
        r['types_en'] = r['types_en'].split(',') if r['types_en'] else []
        r['types_es'] = r['types_es'].split(',') if r['types_es'] else []
    return jsonify(rows)

@app.route('/pokemon/<name>')
def get_pokemon(name):
    p = query_one("""
        SELECT p.*, GROUP_CONCAT(t.name_en ORDER BY pt.slot) AS types_en,
               GROUP_CONCAT(t.name_es ORDER BY pt.slot) AS types_es
        FROM pokemon p
        JOIN pokemon_types pt ON pt.pokemon_id = p.id
        JOIN types t ON t.id = pt.type_id
        WHERE p.name = %s
        GROUP BY p.id
    """, (name,))
    if not p:
        return jsonify({'error': 'Not found'}), 404
    p['types_en'] = p['types_en'].split(',') if p['types_en'] else []
    p['types_es'] = p['types_es'].split(',') if p['types_es'] else []
    return jsonify(p)

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

# ── Tipos ─────────────────────────────────────────
@app.route('/type/<type_name>')
def pokemon_by_type(type_name):
    rows = query("""
        SELECT p.id, p.name, p.name_es, p.sprite_url,
               GROUP_CONCAT(t2.name_en ORDER BY pt2.slot) AS types_en,
               GROUP_CONCAT(t2.name_es ORDER BY pt2.slot) AS types_es
        FROM pokemon p
        JOIN pokemon_types pt  ON pt.pokemon_id  = p.id
        JOIN types t           ON t.id           = pt.type_id  AND t.name_en = %s
        JOIN pokemon_types pt2 ON pt2.pokemon_id = p.id
        JOIN types t2          ON t2.id          = pt2.type_id
        WHERE p.evo_family_id = p.id OR p.evo_family_id IS NULL
        GROUP BY p.id
        ORDER BY p.id
    """, (type_name,))
    for r in rows:
        r['types_en'] = r['types_en'].split(',') if r['types_en'] else []
        r['types_es'] = r['types_es'].split(',') if r['types_es'] else []
    return jsonify(rows)

@app.route('/type/<t1>/<t2>')
def pokemon_by_dual_type(t1, t2):
    rows = query("""
        SELECT p.id, p.name, p.name_es, p.sprite_url,
               GROUP_CONCAT(t.name_en ORDER BY pt.slot) AS types_en
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
        r['types_en'] = r['types_en'].split(',') if r['types_en'] else []
    return jsonify(rows)

@app.route('/effectiveness')
def effectiveness():
    rows = query("""
        SELECT ta.name_en AS attack, td.name_en AS defend,
               e.multiplier
        FROM type_effectiveness e
        JOIN types ta ON ta.id = e.attack_type_id
        JOIN types td ON td.id = e.defend_type_id
    """)
    return jsonify(rows)

# ── Entrenadores ──────────────────────────────────
@app.route('/games')
def list_games():
    return jsonify(query("SELECT * FROM games ORDER BY gen, id"))

@app.route('/trainers')
def list_trainers():
    game_id = request.args.get('game_id')
    if game_id:
        rows = query("SELECT * FROM trainers WHERE game_id=%s ORDER BY gym_order, id", (game_id,))
    else:
        rows = query("SELECT * FROM trainers ORDER BY game_id, gym_order, id")
    return jsonify(rows)

@app.route('/trainer/<int:trainer_id>')
def get_trainer(trainer_id):
    trainer = query_one("SELECT * FROM trainers WHERE id=%s", (trainer_id,))
    if not trainer:
        return jsonify({'error': 'Not found'}), 404
    team = query("""
        SELECT tp.id, tp.slot, tp.level,
               p.name, p.name_es, p.sprite_url,
               GROUP_CONCAT(t.name_en ORDER BY pt.slot) AS types_en
        FROM trainer_pokemon tp
        JOIN pokemon p ON p.id = tp.pokemon_id
        JOIN pokemon_types pt ON pt.pokemon_id = p.id
        JOIN types t ON t.id = pt.type_id
        WHERE tp.trainer_id = %s
        GROUP BY tp.id ORDER BY tp.slot
    """, (trainer_id,))
    for member in team:
        member['types_en'] = member['types_en'].split(',') if member['types_en'] else []
        member['moves'] = query("""
            SELECT m.name, m.name_es, t.name_en AS type_en,
                   m.category, m.power, m.accuracy, tpm.slot
            FROM trainer_pokemon_moves tpm
            JOIN moves m ON m.id = tpm.move_id
            JOIN types t ON t.id = m.type_id
            WHERE tpm.trainer_pokemon_id = %s
            ORDER BY tpm.slot
        """, (member['id'],))
    trainer['team'] = team
    return jsonify(trainer)

# ── Equipos de usuario ────────────────────────────
@app.route('/teams', methods=['POST'])
def create_team():
    data = request.json
    name = data.get('name', 'Mi equipo')
    team_id = execute("INSERT INTO user_teams (name) VALUES (%s)", (name,))
    for slot, member in enumerate(data.get('pokemon', []), 1):
        tp_id = execute(
            "INSERT INTO user_team_pokemon (team_id, pokemon_id, slot) VALUES (%s,%s,%s)",
            (team_id, member['pokemon_id'], slot)
        )
        for mslot, move_id in enumerate(member.get('move_ids', []), 1):
            execute(
                "INSERT INTO user_team_pokemon_moves VALUES (%s,%s,%s)",
                (tp_id, move_id, mslot)
            )
    return jsonify({'id': team_id}), 201

@app.route('/teams/<int:team_id>')
def get_team(team_id):
    team = query_one("SELECT * FROM user_teams WHERE id=%s", (team_id,))
    if not team:
        return jsonify({'error': 'Not found'}), 404
    members = query("""
        SELECT utp.id, utp.slot, p.name, p.name_es, p.sprite_url,
               GROUP_CONCAT(t.name_en ORDER BY pt.slot) AS types_en
        FROM user_team_pokemon utp
        JOIN pokemon p ON p.id = utp.pokemon_id
        JOIN pokemon_types pt ON pt.pokemon_id = p.id
        JOIN types t ON t.id = pt.type_id
        WHERE utp.team_id = %s
        GROUP BY utp.id ORDER BY utp.slot
    """, (team_id,))
    for m in members:
        m['types_en'] = m['types_en'].split(',') if m['types_en'] else []
        m['moves'] = query("""
            SELECT mv.name, mv.name_es, t.name_en AS type_en,
                   mv.category, mv.power, mv.accuracy
            FROM user_team_pokemon_moves utm
            JOIN moves mv ON mv.id = utm.move_id
            JOIN types t ON t.id = mv.type_id
            WHERE utm.team_pokemon_id = %s ORDER BY utm.slot
        """, (m['id'],))
    team['members'] = members
    return jsonify(team)

@app.route('/teams/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    execute("DELETE FROM user_teams WHERE id=%s", (team_id,))
    return jsonify({'ok': True})

# ── Health check ──────────────────────────────────
@app.route('/health')
def health():
    try:
        query_one("SELECT 1")
        return jsonify({'status': 'ok', 'db': 'connected'})
    except Exception as e:
        return jsonify({'status': 'error', 'detail': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
