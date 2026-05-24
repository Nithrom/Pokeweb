"""
build_db.py — Genera data/pokemon_db.json con datos de los 1025 pokémon.
Ejecutar UNA SOLA VEZ. Tarda ~20-30 min (peticiones a PokeAPI con pausa).
El JSON resultante se sirve como archivo estático junto al HTML.

Uso: python3 build_db.py
Salida: Pokeweb/data/pokemon_db.json
"""

import json, time, sys, os, requests
from concurrent.futures import ThreadPoolExecutor, as_completed

SESSION = requests.Session()
SESSION.headers.update({'User-Agent': 'PokeCounter/1.0'})

BASE = 'https://pokeapi.co/api/v2'
OUT_DIR = os.path.join(os.path.dirname(__file__), 'Pokeweb', 'data')
OUT_FILE = os.path.join(OUT_DIR, 'pokemon_db.json')
os.makedirs(OUT_DIR, exist_ok=True)

TOTAL = 1025
MOVE_WORKERS = 12   # peticiones paralelas para moves
POKE_WORKERS = 6    # peticiones paralelas para pokémon


def fetch(url, retries=3):
    for i in range(retries):
        try:
            r = SESSION.get(url, timeout=10)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            if i == retries - 1:
                raise
            time.sleep(1.5 * (i + 1))


def get_move_detail(move_name, url):
    try:
        d = fetch(url)
        return move_name, {
            'type': d['type']['name'],
            'category': d['damage_class']['name'] if d.get('damage_class') else 'status',
            'power': d.get('power'),
            'pp': d.get('pp'),
            'accuracy': d.get('accuracy'),
        }
    except Exception:
        return move_name, {'type': 'normal', 'category': 'status', 'power': None, 'pp': None, 'accuracy': None}


def get_pokemon(entry):
    name = entry['name']
    try:
        d = fetch(f"{BASE}/pokemon/{name}")

        # Sprite
        sprite = (d['sprites'].get('other', {}).get('official-artwork', {}).get('front_default')
                  or d['sprites'].get('front_default'))

        # Tipos
        types = [t['type']['name'] for t in d['types']]

        # Movimientos: recopilar todos con su URL y nivel (si aplica)
        level_set = {}
        for m in d['moves']:
            mn = m['move']['name']
            for vd in m['version_group_details']:
                if vd['move_learn_method']['name'] == 'level-up':
                    if mn not in level_set:
                        level_set[mn] = {'url': m['move']['url'], 'level': vd['level_learned_at']}
                    break

        # Moves por nivel ordenados, luego el resto
        lvl_moves = sorted(
            [{'name': n, 'url': v['url'], 'level': v['level'], 'byLevel': True}
             for n, v in level_set.items()],
            key=lambda x: (x['level'], x['name'])
        )
        other_moves = sorted(
            [{'name': m['move']['name'], 'url': m['move']['url'], 'level': None, 'byLevel': False}
             for m in d['moves'] if m['move']['name'] not in level_set],
            key=lambda x: x['name']
        )
        all_moves = lvl_moves + other_moves

        return name, {'id': d['id'], 'types': types, 'sprite': sprite, 'moves': all_moves}
    except Exception as e:
        print(f"  ERROR {name}: {e}")
        return name, None


def main():
    print("📥 Cargando lista de pokémon...")
    data = fetch(f"{BASE}/pokemon?limit={TOTAL}")
    entries = data['results']
    print(f"  {len(entries)} pokémon encontrados.")

    # ── FASE 1: datos básicos de cada pokémon ──
    print(f"\n⚡ Fase 1: datos de pokémon ({POKE_WORKERS} en paralelo)...")
    pokemon_db = {}
    done = 0
    with ThreadPoolExecutor(max_workers=POKE_WORKERS) as ex:
        futures = {ex.submit(get_pokemon, e): e['name'] for e in entries}
        for f in as_completed(futures):
            name, result = f.result()
            done += 1
            if result:
                pokemon_db[name] = result
            pct = done / len(entries) * 100
            print(f"\r  {done}/{len(entries)} ({pct:.1f}%) — {name}{'  ' * 20}", end='', flush=True)
    print(f"\n  ✓ {len(pokemon_db)} pokémon cargados.")

    # ── FASE 2: detalles de moves únicos ──
    print("\n⚡ Fase 2: detalles de movimientos únicos...")
    move_urls = {}
    for pdata in pokemon_db.values():
        for m in pdata['moves']:
            move_urls[m['name']] = m['url']
    print(f"  {len(move_urls)} movimientos únicos encontrados.")

    move_details = {}
    done = 0
    total_moves = len(move_urls)
    items = list(move_urls.items())

    with ThreadPoolExecutor(max_workers=MOVE_WORKERS) as ex:
        futures = {ex.submit(get_move_detail, mn, url): mn for mn, url in items}
        for f in as_completed(futures):
            mn, detail = f.result()
            move_details[mn] = detail
            done += 1
            pct = done / total_moves * 100
            print(f"\r  {done}/{total_moves} ({pct:.1f}%) — {mn}{'  ' * 20}", end='', flush=True)
    print(f"\n  ✓ {len(move_details)} movimientos procesados.")

    # ── FASE 3: incrustar detalles en cada pokémon ──
    print("\n🔧 Fase 3: combinando datos...")
    for pdata in pokemon_db.values():
        for m in pdata['moves']:
            detail = move_details.get(m['name'], {})
            m['detail'] = detail
            del m['url']  # no necesitamos la URL en el cliente

    # ── GUARDAR ──
    print(f"\n💾 Guardando en {OUT_FILE}...")
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        json.dump({'pokemon': pokemon_db, 'moves': move_details}, f, separators=(',', ':'), ensure_ascii=False)

    size_mb = os.path.getsize(OUT_FILE) / 1024 / 1024
    print(f"✅ ¡Listo! {size_mb:.1f} MB — {len(pokemon_db)} pokémon, {len(move_details)} movimientos.")
    print(f"   Coloca Pokeweb/data/pokemon_db.json junto al index.html y abre la web.")


if __name__ == '__main__':
    main()
