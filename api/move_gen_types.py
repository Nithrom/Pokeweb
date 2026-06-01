"""Tipos de movimiento históricos por generación del juego."""

from __future__ import annotations

# through_gen: si game_gen <= N; from_gen: si game_gen >= N
MOVE_TYPE_THRESHOLDS: dict[str, list[dict]] = {
    'bite': [
        {'through_gen': 1, 'type': 'normal'},
        {'from_gen': 2, 'type': 'dark'},
    ],
    'gust': [
        {'through_gen': 1, 'type': 'normal'},
        {'from_gen': 2, 'type': 'flying'},
    ],
    'karate-chop': [
        {'through_gen': 1, 'type': 'normal'},
        {'from_gen': 2, 'type': 'fighting'},
    ],
    'sand-attack': [
        {'through_gen': 1, 'type': 'normal'},
        {'from_gen': 2, 'type': 'ground'},
    ],
    'charm': [
        {'through_gen': 5, 'type': 'normal'},
        {'from_gen': 6, 'type': 'fairy'},
    ],
    'moonlight': [
        {'through_gen': 5, 'type': 'normal'},
        {'from_gen': 6, 'type': 'fairy'},
    ],
    'sweet-kiss': [
        {'through_gen': 5, 'type': 'normal'},
        {'from_gen': 6, 'type': 'fairy'},
    ],
    'curse': [
        {'through_gen': 4, 'type': 'unknown'},
        {'from_gen': 5, 'type': 'ghost'},
    ],
}


def resolve_move_type(move_slug: str, game_gen: int, catalog_type: str) -> str:
    slug = (move_slug or '').lower()
    gen = int(game_gen or 0)
    fallback = catalog_type or 'normal'
    rules = MOVE_TYPE_THRESHOLDS.get(slug)
    if not rules or gen < 1:
        return fallback

    resolved = fallback
    for r in rules:
        if r.get('through_gen') is not None and gen <= r['through_gen']:
            return r['type']
        if r.get('from_gen') is not None and gen >= r['from_gen']:
            resolved = r['type']
    return resolved
