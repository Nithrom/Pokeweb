"""
import_db.py — Importa pokemon_db.json a MariaDB
=================================================
Instrucciones:
  1. Copia tu pokemon_db.json a la carpeta Pokeweb-api/
     cp ../Pokeweb/data/pokemon_db.json ./api/pokemon_db.json

  2. Con los contenedores corriendo (docker compose up -d):
     docker exec pokeweb_api python import_db.py

  Si ya hay datos y quieres reimportar desde cero:
     docker exec pokeweb_api python import_db.py --reset
"""

import json, os, sys, time, argparse
import pymysql

DB_CONFIG = {
    'host':        os.environ.get('DB_HOST', 'mariadb'),
    'port':        int(os.environ.get('DB_PORT', 3306)),
    'user':        os.environ.get('DB_USER', 'pokeweb_user'),
    'password':    os.environ.get('DB_PASS', 'pokeweb_pass'),
    'database':    os.environ.get('DB_NAME', 'pokeweb'),
    'charset':     'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}

JSON_PATH = os.path.join(os.path.dirname(__file__), 'pokemon_db.json')

TIPOS_ES = {
    'normal':'Normal','fighting':'Lucha','flying':'Volador','poison':'Veneno',
    'ground':'Tierra','rock':'Roca','bug':'Bicho','ghost':'Fantasma',
    'steel':'Acero','fire':'Fuego','water':'Agua','grass':'Planta',
    'electric':'Eléctrico','psychic':'Psíquico','ice':'Hielo',
    'dragon':'Dragón','dark':'Siniestro','fairy':'Hada'
}

EFF = {
    'normal':   {'normal':1,'fighting':1,'flying':1,'poison':1,'ground':1,'rock':0.5,'bug':1,'ghost':0,'steel':0.5,'fire':1,'water':1,'grass':1,'electric':1,'psychic':1,'ice':1,'dragon':1,'dark':1,'fairy':1},
    'fighting': {'normal':2,'fighting':1,'flying':0.5,'poison':0.5,'ground':1,'rock':2,'bug':0.5,'ghost':0,'steel':2,'fire':1,'water':1,'grass':1,'electric':1,'psychic':0.5,'ice':2,'dragon':1,'dark':2,'fairy':0.5},
    'flying':   {'normal':1,'fighting':2,'flying':1,'poison':1,'ground':1,'rock':0.5,'bug':2,'ghost':1,'steel':0.5,'fire':1,'water':1,'grass':2,'electric':0.5,'psychic':1,'ice':1,'dragon':1,'dark':1,'fairy':1},
    'poison':   {'normal':1,'fighting':1,'flying':1,'poison':0.5,'ground':0.5,'rock':0.5,'bug':1,'ghost':0.5,'steel':0,'fire':1,'water':1,'grass':2,'electric':1,'psychic':1,'ice':1,'dragon':1,'dark':1,'fairy':2},
    'ground':   {'normal':1,'fighting':1,'flying':0,'poison':2,'ground':1,'rock':2,'bug':0.5,'ghost':1,'steel':2,'fire':2,'water':1,'grass':0.5,'electric':2,'psychic':1,'ice':1,'dragon':1,'dark':1,'fairy':1},
    'rock':     {'normal':1,'fighting':0.5,'flying':2,'poison':1,'ground':0.5,'rock':1,'bug':2,'ghost':1,'steel':0.5,'fire':2,'water':1,'grass':1,'electric':1,'psychic':1,'ice':2,'dragon':1,'dark':1,'fairy':1},
    'bug':      {'normal':1,'fighting':0.5,'flying':0.5,'poison':0.5,'ground':1,'rock':1,'bug':1,'ghost':0.5,'steel':0.5,'fire':0.5,'water':1,'grass':2,'electric':1,'psychic':2,'ice':1,'dragon':1,'dark':2,'fairy':0.5},
    'ghost':    {'normal':0,'fighting':1,'flying':1,'poison':1,'ground':1,'rock':1,'bug':1,'ghost':2,'steel':1,'fire':1,'water':1,'grass':1,'electric':1,'psychic':2,'ice':1,'dragon':1,'dark':0.5,'fairy':1},
    'steel':    {'normal':1,'fighting':1,'flying':1,'poison':1,'ground':1,'rock':2,'bug':1,'ghost':1,'steel':0.5,'fire':0.5,'water':0.5,'grass':1,'electric':0.5,'psychic':1,'ice':2,'dragon':1,'dark':1,'fairy':2},
    'fire':     {'normal':1,'fighting':1,'flying':1,'poison':1,'ground':1,'rock':0.5,'bug':2,'ghost':1,'steel':2,'fire':0.5,'water':0.5,'grass':2,'electric':1,'psychic':1,'ice':2,'dragon':0.5,'dark':1,'fairy':1},
    'water':    {'normal':1,'fighting':1,'flying':1,'poison':1,'ground':2,'rock':2,'bug':1,'ghost':1,'steel':1,'fire':2,'water':0.5,'grass':0.5,'electric':1,'psychic':1,'ice':1,'dragon':0.5,'dark':1,'fairy':1},
    'grass':    {'normal':1,'fighting':1,'flying':0.5,'poison':0.5,'ground':2,'rock':2,'bug':0.5,'ghost':1,'steel':0.5,'fire':0.5,'water':2,'grass':0.5,'electric':1,'psychic':1,'ice':1,'dragon':0.5,'dark':1,'fairy':1},
    'electric': {'normal':1,'fighting':1,'flying':2,'poison':1,'ground':0,'rock':1,'bug':1,'ghost':1,'steel':1,'fire':1,'water':2,'grass':0.5,'electric':0.5,'psychic':1,'ice':1,'dragon':0.5,'dark':1,'fairy':1},
    'psychic':  {'normal':1,'fighting':2,'flying':1,'poison':2,'ground':1,'rock':1,'bug':1,'ghost':1,'steel':0.5,'fire':1,'water':1,'grass':1,'electric':1,'psychic':0.5,'ice':1,'dragon':1,'dark':0,'fairy':1},
    'ice':      {'normal':1,'fighting':1,'flying':2,'poison':1,'ground':2,'rock':1,'bug':1,'ghost':1,'steel':0.5,'fire':0.5,'water':0.5,'grass':2,'electric':1,'psychic':1,'ice':0.5,'dragon':2,'dark':1,'fairy':1},
    'dragon':   {'normal':1,'fighting':1,'flying':1,'poison':1,'ground':1,'rock':1,'bug':1,'ghost':1,'steel':0.5,'fire':1,'water':1,'grass':1,'electric':1,'psychic':1,'ice':1,'dragon':2,'dark':1,'fairy':0},
    'dark':     {'normal':1,'fighting':0.5,'flying':1,'poison':1,'ground':1,'rock':1,'bug':1,'ghost':2,'steel':1,'fire':1,'water':1,'grass':1,'electric':1,'psychic':2,'ice':1,'dragon':1,'dark':0.5,'fairy':0.5},
    'fairy':    {'normal':1,'fighting':2,'flying':1,'poison':0.5,'ground':1,'rock':1,'bug':1,'ghost':1,'steel':0.5,'fire':0.5,'water':1,'grass':1,'electric':1,'psychic':1,'ice':1,'dragon':2,'dark':2,'fairy':1},
}

EVO_FAMILY_IDS = {
    1,4,7,10,13,16,19,21,23,25,27,29,32,35,37,39,41,43,46,48,50,52,54,56,58,
    60,63,66,69,72,74,77,79,81,83,84,86,88,90,92,95,96,98,100,102,104,106,107,
    108,109,111,113,114,115,116,118,120,122,123,124,125,126,127,128,129,131,132,
    133,137,138,140,142,143,144,145,146,147,150,151,152,155,158,161,163,165,167,
    169,170,172,173,174,175,177,179,183,185,187,190,191,193,194,196,197,198,200,
    201,202,203,204,206,207,209,211,213,214,215,216,218,220,222,223,225,226,227,
    228,231,233,234,235,236,238,239,240,241,242,243,244,245,246,249,250,251,252,
    255,258,261,263,265,270,273,276,278,280,283,285,287,290,293,296,298,299,300,
    302,303,304,306,307,309,311,312,313,314,315,316,318,320,322,324,325,327,328,
    331,333,335,336,337,338,339,341,343,345,347,349,351,352,353,355,357,358,359,
    360,361,363,366,369,370,371,374,377,378,379,380,381,382,383,384,385,386,387,
    390,393,396,399,401,403,406,408,410,412,415,417,418,420,422,424,425,427,429,
    430,431,433,434,436,438,439,440,441,442,443,446,447,449,451,453,455,456,458,
    459,460,461,462,463,464,465,466,467,468,469,470,471,472,473,474,475,476,477,
    478,479,480,481,482,483,484,485,486,487,488,489,491,492,493,494,495,498,501,
    504,506,509,511,513,515,517,519,522,524,527,529,531,532,535,538,539,540,543,
    546,548,550,551,554,556,557,559,561,562,564,566,568,570,572,574,577,580,582,
    585,587,588,590,592,594,595,597,599,602,605,607,610,613,615,616,618,619,621,
    622,624,626,627,629,631,632,633,636,638,639,640,641,642,643,644,645,646,647,
    648,649,650,653,656,659,662,665,668,671,672,674,676,677,679,682,684,686,688,
    690,692,694,696,698,700,701,702,703,704,707,708,710,712,714,716,717,718,719,
    720,721,722,725,728,731,734,736,739,741,742,744,746,747,749,751,753,755,757,
    759,761,764,765,766,767,769,771,772,774,775,776,777,778,779,780,781,782,785,
    786,787,788,789,791,792,793,800,801,802,803,806,807,808,810,813,816,819,821,
    824,826,827,829,831,833,835,837,840,842,843,845,846,847,848,850,852,854,856,
    858,859,862,863,864,865,866,867,868,870,871,872,874,875,876,877,878,880,881,
    882,883,884,885,888,889,890,891,892,893,894,895,896,897,898,899,900,901,902,
    903,904,905,906,909,912,915,918,921,922,923,924,925,926,927,928,929,930,931,
    932,933,934,935,936,937,938,939,940,941,942,943,944,945,946,947,948,949,950,
    951,952,953,954,955,956,957,958,959,960,961,962,963,964,965,966,967,968,969,
    970,971,972,973,974,975,976,977,978,979,980,981,982,983,984,985,986,987,988,
    989,990,991,992,993,994,995,996,997,998,999,1000,1001,1002,1003,1004,1005,
    1006,1007,1008,1009,1010,1017,1020,1021,1022,1023,1024,1025
}


def wait_for_db(max_tries=20):
    print('Esperando conexión a MariaDB', end='', flush=True)
    for i in range(max_tries):
        try:
            conn = pymysql.connect(**DB_CONFIG)
            conn.close()
            print(' ✓')
            return
        except Exception:
            print('.', end='', flush=True)
            time.sleep(3)
    print('\nERROR: no se pudo conectar a la base de datos.')
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reset', action='store_true',
                        help='Borra todos los datos antes de importar')
    args = parser.parse_args()

    if not os.path.exists(JSON_PATH):
        print(f'ERROR: no encuentro {JSON_PATH}')
        print('Copia pokemon_db.json a Pokeweb-api/ y vuelve a ejecutar.')
        sys.exit(1)

    print(f'Leyendo {JSON_PATH}...')
    with open(JSON_PATH, encoding='utf-8') as f:
        db_json = json.load(f)

    pokemon_data = db_json.get('pokemon', {})
    moves_data   = db_json.get('moves', {})
    print(f'  {len(pokemon_data)} pokémon, {len(moves_data)} movimientos en el JSON.')

    wait_for_db()
    conn = pymysql.connect(**DB_CONFIG)
    cur  = conn.cursor()

    if args.reset:
        print('Borrando datos anteriores...')
        for t in ['trainer_pokemon_moves','trainer_pokemon','trainers','games',
                  'user_team_pokemon_moves','user_team_pokemon','user_teams',
                  'pokemon_moves','pokemon_types','pokemon',
                  'type_effectiveness','moves','types']:
            cur.execute(f'DELETE FROM {t}')
        conn.commit()
        print('  Tablas vaciadas.')

    # ── 1. Tipos ─────────────────────────────────────────────────────────────
    print('\n[1/5] Tipos...', end=' ')
    for name_en, name_es in TIPOS_ES.items():
        cur.execute('INSERT IGNORE INTO types (name_en, name_es) VALUES (%s,%s)',
                    (name_en, name_es))
    conn.commit()
    cur.execute('SELECT id, name_en FROM types')
    type_id_map = {r['name_en']: r['id'] for r in cur.fetchall()}
    print(f'{len(type_id_map)} tipos ✓')

    # ── 2. Efectividades ──────────────────────────────────────────────────────
    print('[2/5] Efectividades...', end=' ')
    rows = []
    for atk, defenses in EFF.items():
        aid = type_id_map.get(atk)
        if not aid: continue
        for deftype, mult in defenses.items():
            did = type_id_map.get(deftype)
            if not did: continue
            rows.append((aid, did, int(mult * 100)))
    cur.executemany(
        '''INSERT INTO type_effectiveness (attack_type_id, defend_type_id, multiplier)
           VALUES (%s,%s,%s) ON DUPLICATE KEY UPDATE multiplier=VALUES(multiplier)''', rows)
    conn.commit()
    print(f'{len(rows)} combinaciones ✓')

    # ── 3. Movimientos ────────────────────────────────────────────────────────
    print('[3/5] Movimientos...', end=' ', flush=True)
    move_rows = []
    for name, det in moves_data.items():
        tid = type_id_map.get(det.get('type','normal'), type_id_map['normal'])
        cat = det.get('category','status')
        if cat not in ('physical','special','status'): cat = 'status'
        name_es = name.replace('-',' ').title()
        move_rows.append((name, name_es, tid, cat,
                          det.get('power'), det.get('accuracy'), det.get('pp')))
    # batch de 500
    for i in range(0, len(move_rows), 500):
        cur.executemany(
            '''INSERT IGNORE INTO moves (name, name_es, type_id, category, power, accuracy, pp)
               VALUES (%s,%s,%s,%s,%s,%s,%s)''', move_rows[i:i+500])
    conn.commit()
    cur.execute('SELECT id, name FROM moves')
    move_id_map = {r['name']: r['id'] for r in cur.fetchall()}
    print(f'{len(move_id_map)} movimientos ✓')

    # ── 4. Pokémon + moves ────────────────────────────────────────────────────
    print('[4/5] Pokémon y movimientos...')
    total = len(pokemon_data)
    done  = 0

    for name, pdata in sorted(pokemon_data.items(), key=lambda x: x[1]['id']):
        pid    = pdata['id']
        name_es = name.replace('-',' ').title()
        sprite  = pdata.get('sprite','')
        evo_fam = pid if pid in EVO_FAMILY_IDS else None

        # Stats: soporte para estructura plana {hp, attack, ...}
        # o array PokeAPI [{stat:{name:...}, base_stat:...}, ...]
        raw_stats = pdata.get('stats')
        if isinstance(raw_stats, list):
            # Formato PokeAPI
            stats_map = {s['stat']['name']: s['base_stat'] for s in raw_stats}
            hp         = stats_map.get('hp', 0)
            attack     = stats_map.get('attack', 0)
            defense    = stats_map.get('defense', 0)
            sp_attack  = stats_map.get('special-attack', 0)
            sp_defense = stats_map.get('special-defense', 0)
            speed      = stats_map.get('speed', 0)
        else:
            # Formato plano (campos directos en pdata)
            hp         = pdata.get('hp', 0)
            attack     = pdata.get('attack', 0)
            defense    = pdata.get('defense', 0)
            sp_attack  = pdata.get('sp_attack', pdata.get('special_attack', pdata.get('spatk', 0)))
            sp_defense = pdata.get('sp_defense', pdata.get('special_defense', pdata.get('spdef', 0)))
            speed      = pdata.get('speed', 0)

        # is_legendary: puede estar en pdata directamente o en pdata['species']
        is_legendary = int(bool(
            pdata.get('is_legendary') or
            pdata.get('isLegendary') or
            pdata.get('legendary') or
            pdata.get('species', {}).get('is_legendary', False)
        ))

        cur.execute(
            '''INSERT INTO pokemon
               (id, name, name_es, sprite_url, hp, attack, defense,
                sp_attack, sp_defense, speed, is_legendary, evo_family_id)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
               ON DUPLICATE KEY UPDATE
                 sprite_url=VALUES(sprite_url),
                 hp=VALUES(hp), attack=VALUES(attack), defense=VALUES(defense),
                 sp_attack=VALUES(sp_attack), sp_defense=VALUES(sp_defense),
                 speed=VALUES(speed), is_legendary=VALUES(is_legendary),
                 evo_family_id=VALUES(evo_family_id)''',
            (pid, name, name_es, sprite,
             hp, attack, defense, sp_attack, sp_defense, speed,
             is_legendary, evo_fam))

        # tipos
        for slot, type_en in enumerate(pdata.get('types',[]), 1):
            tid = type_id_map.get(type_en)
            if tid:
                cur.execute(
                    'INSERT IGNORE INTO pokemon_types (pokemon_id,type_id,slot) VALUES(%s,%s,%s)',
                    (pid, tid, slot))

        # moves
        pm_rows = []
        for m in pdata.get('moves',[]):
            mid = move_id_map.get(m['name'])
            if not mid:
                # move no estaba en moves_data, intentar usar detail incrustado
                det = m.get('detail',{})
                if det:
                    tid2 = type_id_map.get(det.get('type','normal'), type_id_map['normal'])
                    cat2 = det.get('category','status')
                    if cat2 not in ('physical','special','status'): cat2='status'
                    cur.execute(
                        '''INSERT IGNORE INTO moves (name,name_es,type_id,category,power,accuracy,pp)
                           VALUES(%s,%s,%s,%s,%s,%s,%s)''',
                        (m['name'], m['name'].replace('-',' ').title(),
                         tid2, cat2, det.get('power'), det.get('accuracy'), det.get('pp')))
                    cur.execute('SELECT id FROM moves WHERE name=%s', (m['name'],))
                    row = cur.fetchone()
                    if row:
                        mid = row['id']
                        move_id_map[m['name']] = mid
            if not mid: continue
            method = 'level-up' if m.get('byLevel') else 'machine'
            lvl    = m.get('level') or None
            if lvl == 0: lvl = None
            pm_rows.append((pid, mid, method, lvl))

        if pm_rows:
            cur.executemany(
                '''INSERT IGNORE INTO pokemon_moves (pokemon_id,move_id,learn_method,level)
                   VALUES(%s,%s,%s,%s)''', pm_rows)

        done += 1
        if done % 50 == 0 or done == total:
            conn.commit()
            print(f'\r  {done}/{total} ({done/total*100:.0f}%)  ', end='', flush=True)

    conn.commit()
    print()

    # ── 5. Verificación ───────────────────────────────────────────────────────
    print('[5/5] Verificando...')
    def count(table):
        cur.execute(f'SELECT COUNT(*) AS n FROM {table}')
        return cur.fetchone()['n']

    print(f'''
✅ Importación completada:
   pokemon:           {count("pokemon")}
   moves:             {count("moves")}
   pokemon_moves:     {count("pokemon_moves")}
   type_effectiveness:{count("type_effectiveness")}

Prueba rápida:
  http://localhost:5000/health
  http://localhost:5000/pokemon/rayquaza
  http://localhost:5000/pokemon/rayquaza/moves
''')
    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
