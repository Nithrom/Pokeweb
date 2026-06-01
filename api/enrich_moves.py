#!/usr/bin/env python3
"""
Rellena movimientos reales en data/trainers_db.json desde Bulbapedia.

Uso:
  python enrich_moves.py                 # todos los entrenadores
  python enrich_moves.py --solo-faltantes  # solo quienes no tienen movimientos
  python enrich_moves.py platinum scarlet-violet  # solo esos juegos
"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'data', 'trainers_db.json')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_trainers import normalize_trainer_poke_name
from bulbapedia_teams import clear_caches, enrich_trainers_db, print_enrich_progress


def parse_args():
    p = argparse.ArgumentParser(description='Enriquecer movimientos desde Bulbapedia')
    p.add_argument(
        '--solo-faltantes',
        action='store_true',
        help='Solo entrenadores con algún Pokémon sin movimientos en el JSON',
    )
    p.add_argument(
        'slugs',
        nargs='*',
        help='Slugs de juego opcionales (ej. platinum scarlet-violet)',
    )
    return p.parse_args()


def main():
    args = parse_args()
    with open(OUT, encoding='utf-8') as f:
        data = json.load(f)

    trainers_db = data.get('trainers', {})
    if args.slugs:
        trainers_db = {k: v for k, v in trainers_db.items() if k in args.slugs}
        if not trainers_db:
            print('Ningún slug coincide:', ', '.join(args.slugs))
            sys.exit(1)

    clear_caches()
    mode = 'solo faltantes' if args.solo_faltantes else 'todos'
    print(f'Enriqueciendo movimientos ({mode}) en {OUT}...')
    if args.slugs:
        print('  Juegos:', ', '.join(trainers_db.keys()))

    n_up, n_skip = enrich_trainers_db(
        trainers_db,
        normalize_trainer_poke_name,
        on_progress=print_enrich_progress,
        only_missing_moves=args.solo_faltantes,
    )
    print()
    print(f'Listo: {n_up} actualizados, {n_skip} sin datos Bulbapedia.')

    full = data.get('trainers', {})
    for slug, trainers in trainers_db.items():
        full[slug] = trainers

    data['trainers'] = full
    if 'meta' in data:
        data['meta']['source'] = 'pokemondb.net, bulbapedia.bulbagarden.net'

    tmp = OUT + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, OUT)
    print(f'Guardado: {OUT}')


if __name__ == '__main__':
    main()
