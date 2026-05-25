"""
enrich_stats.py — Añade stats base e is_legendary a pokemon_db.json
====================================================================
Lee el JSON actual, descarga las stats que faltan desde PokeAPI,
y guarda el JSON enriquecido. NO toca los moves ni los tipos.

Uso:
    python3 enrich_stats.py                  # enriquece data/pokemon_db.json
    python3 enrich_stats.py --dry-run        # muestra los primeros 5 sin guardar
    python3 enrich_stats.py --from 500       # empieza desde el pokémon nº 500 (resume)

El script es reanudable: si ya tiene stats un pokémon, lo salta.
"""

import json, os, sys, time, argparse, urllib.request, urllib.error

JSON_PATH = os.path.join(os.path.dirname(__file__), 'data', 'pokemon_db.json')
POKEAPI   = 'https://pokeapi.co/api/v2'
DELAY     = 0.25   # segundos entre peticiones (respetar rate limit)


def fetch_json(url, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'PokeCounter/1.0'})
            with urllib.request.urlopen(req, timeout=10) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            print(f'\n  HTTP {e.code} en {url}, reintento {attempt+1}/{retries}...')
            time.sleep(2)
        except Exception as e:
            print(f'\n  Error en {url}: {e}, reintento {attempt+1}/{retries}...')
            time.sleep(2)
    return None


def get_stats(poke_data):
    """Extrae stats del objeto devuelto por /pokemon/<name>"""
    stats_map = {s['stat']['name']: s['base_stat'] for s in poke_data.get('stats', [])}
    return {
        'hp':         stats_map.get('hp', 0),
        'attack':     stats_map.get('attack', 0),
        'defense':    stats_map.get('defense', 0),
        'sp_attack':  stats_map.get('special-attack', 0),
        'sp_defense': stats_map.get('special-defense', 0),
        'speed':      stats_map.get('speed', 0),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true',
                        help='Muestra los primeros 5 pokémon sin guardar')
    parser.add_argument('--from', dest='start_id', type=int, default=0,
                        help='ID desde el que empezar (para reanudar)')
    args = parser.parse_args()

    if not os.path.exists(JSON_PATH):
        print(f'ERROR: no encuentro {JSON_PATH}')
        sys.exit(1)

    print(f'Leyendo {JSON_PATH}...')
    with open(JSON_PATH, encoding='utf-8') as f:
        db = json.load(f)

    pokemon_data = db.get('pokemon', {})
    total = len(pokemon_data)
    print(f'  {total} pokémon en el JSON.')

    # Ordenar por ID para procesar en orden y poder reanudar
    sorted_pokemon = sorted(pokemon_data.items(), key=lambda x: x[1]['id'])

    done = 0
    skipped = 0
    errors = 0
    dry_count = 0

    for name, pdata in sorted_pokemon:
        pid = pdata['id']

        # Saltar pokémon anteriores al --from
        if pid < args.start_id:
            skipped += 1
            continue

        # Si ya tiene stats, saltar (reanudable)
        if pdata.get('hp', 0) != 0:
            skipped += 1
            done += 1
            continue

        # Dry run: solo mostrar los primeros 5
        if args.dry_run:
            print(f'  [{pid}] {name} → descargando stats...')
            data = fetch_json(f'{POKEAPI}/pokemon/{pid}')
            if data:
                stats = get_stats(data)
                print(f'       stats: {stats}')
            dry_count += 1
            if dry_count >= 5:
                print('\nDry-run completado (5 pokémon). Ejecuta sin --dry-run para guardar.')
                return
            continue

        # Descargar datos del pokémon
        data = fetch_json(f'{POKEAPI}/pokemon/{pid}')
        if not data:
            print(f'\n  ⚠ No se encontró pokémon {pid} ({name}), saltando...')
            errors += 1
            done += 1
            continue

        stats = get_stats(data)

        # is_legendary: viene de /pokemon-species/<id>
        species_data = fetch_json(f'{POKEAPI}/pokemon-species/{pid}')
        is_legendary = 0
        if species_data:
            is_legendary = int(
                species_data.get('is_legendary', False) or
                species_data.get('is_mythical', False)
            )

        # Enriquecer el dict en memoria
        pdata.update(stats)
        pdata['is_legendary'] = is_legendary

        done += 1
        pct = done / (total - skipped + done) * 100 if total > 0 else 0
        print(f'\r  [{pid:4d}] {name:<20s} HP:{stats["hp"]:3d} ATK:{stats["attack"]:3d} '
              f'SPD:{stats["speed"]:3d} leg:{is_legendary}  '
              f'({done}/{total})  ', end='', flush=True)

        # Guardar cada 50 pokémon por si se interrumpe
        if done % 50 == 0:
            with open(JSON_PATH, 'w', encoding='utf-8') as f:
                json.dump(db, f, ensure_ascii=False, separators=(',', ':'))
            print(f'\n  💾 Guardado parcial ({done} procesados)...', flush=True)

        time.sleep(DELAY)

    # Guardado final
    if not args.dry_run:
        print(f'\nGuardando {JSON_PATH}...')
        with open(JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, separators=(',', ':'))
        print(f'''
✅ Enriquecimiento completado:
   Procesados:  {done}
   Ya tenían stats (saltados): {skipped}
   Errores:     {errors}

Ahora reimporta la DB:
   docker exec pokeweb_api python import_db.py --reset
''')


if __name__ == '__main__':
    main()
