"""Tipo de movimiento según generación del juego (histórico de Pokémon)."""
from __future__ import annotations

# slug → [(gen_min, gen_max|None), type_en]
MOVE_GEN_TYPE_RULES: dict[str, list[tuple[tuple[int, int | None], str]]] = {
    'bite': [((1, 1), 'normal'), ((2, None), 'dark')],
    'gust': [((1, 1), 'normal'), ((2, None), 'flying')],
    'karate-chop': [((1, 1), 'normal'), ((2, None), 'fighting')],
    'sand-attack': [((1, 1), 'normal'), ((2, None), 'ground')],
    'curse': [((2, 4), 'unknown'), ((5, None), 'ghost')],
    'charm': [((2, 5), 'normal'), ((6, None), 'fairy')],
    'moonlight': [((2, 5), 'normal'), ((6, None), 'fairy')],
    'sweet-kiss': [((2, 5), 'normal'), ((6, None), 'fairy')],
}

_ALIASES = {
    'karate chop': 'karate-chop',
    'sand attack': 'sand-attack',
    'sweet kiss': 'sweet-kiss',
}


def _normalize_move_slug(name: str) -> str:
    if not name:
        return ''
    key = name.strip().lower().replace('_', '-')
    return _ALIASES.get(key, key.replace(' ', '-'))


def resolve_move_type(move_name: str, game_gen: int, default_type: str = 'normal') -> str:
    if not game_gen or game_gen < 1:
        return default_type or 'normal'
    slug = _normalize_move_slug(move_name)
    rules = MOVE_GEN_TYPE_RULES.get(slug)
    if not rules:
        return default_type or 'normal'
    for (gen_min, gen_max), type_en in rules:
        if game_gen < gen_min:
            continue
        if gen_max is not None and game_gen > gen_max:
            continue
        return type_en
    return default_type or 'normal'
